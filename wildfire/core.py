from functools import partial
import inspect
import json
from types import FunctionType

import falcon


def Wildfire(obj):
    """Wrap a Python object as an HTTP service and run that service.

    Args:
        obj (object): The object to be wrapped.
    """
    # Create an API object with routes for the object's methods.
    api = _create_api(obj)

    return api


def _create_api(obj):
    """Create a Falcon API with routes for the object's methods.

    Args:
        obj (object): The object to be wrapped.
    """
    # Initialize Falcon API.
    api = falcon.API()

    # Check wether the object is a function or a class type.
    if isinstance(obj, FunctionType):
        # If the object is a function, its route can be created right away.
        add_method_route_to_api(obj, api)
    else:
        # For a class, extract all its methods first.
        methods = get_methods_from_object(obj)
        # Create partials methods where 'self' is set to the object.
        if isinstance(obj, type):
            methods = [build_partial_method(m, obj) for m in methods]
        # Add routing method(s) to API.
        for method in methods:
            add_method_route_to_api(method, api)

    return api


def get_methods_from_object(obj):
    """Get all methods of an object.

    Args:
        obj (object): The object to get methods from.
    Returns:
        A list of all public methods from the given object.
    """
    # Get all method names from the object.
    method_names = [method_name for method_name in dir(obj)
                    if callable(getattr(obj, method_name))]
    # Get all methods, excluding those starting with '_' or '__'.
    methods = [getattr(obj, mn) for mn in method_names
               if not mn.startswith('_')]

    return methods


def build_partial_method(method, obj):
    """Create a partial method where 'self' is set to the given object.

    Args:
        method (callable): The method used for creating the partial method.
        obj (object):
    Returns:
        A functools.partial object.
    """
    # If the method has no 'self' parameter, then no partial method is needed.
    method_parameters = inspect.signature(method).parameters.keys()
    if 'self' not in method_parameters:
        return method

    method_name = method.__name__

    # Create partial method and set 'self' parameter and name property.
    partial_method = partial(method, self=obj)
    partial_method.__name__ = method_name

    return partial_method


def add_method_route_to_api(method, api):
    """Wrap a partial method into a routing function.

    Args:
        method (functools.partial): Partial method to wrap. Needs to have a
            value for '__name__'.
        api (falcon.API): Falcon API to add to routing method to.
    """
    method_name = method.__name__
    resource = build_resource_from_method(method)
    api.add_route(f'/{method_name}', resource)


def build_resource_from_method(method):
    class QuoteResource:
        def on_post(self, req, resp):
            # Extract fields from JSON request.
            json_args = json.load(req.stream)

            # Check if the JSON payload contains all arguments of the function.
            # If not, exit with 422 (Unprocessable Entity) response.
            # Valid exceptions are the 'self' and default parameters.
            # TODO Handle parameters that do not exist in the method signature.
            func_args = inspect.signature(method).parameters.items()
            for arg_name, arg in func_args:
                if arg_name not in json_args:
                    if arg_name == 'self':
                        continue
                    if not isinstance(arg.default, inspect._empty):
                        continue
                    resp.body = (f"Arguments for method {method.__name__!r}"
                                 + " missing")
                    resp.status = falcon.HTTP_422
                    return

            # Call function with parameters from JSON request.
            res = method(**json_args)

            resp.media = res
            resp.status = falcon.HTTP_200

    initialized_resource = QuoteResource()
    return initialized_resource
