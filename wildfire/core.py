from functools import partial
import inspect

from flask import Flask, request, jsonify


def Wildfire(obj, host='0.0.0.0'):
    """Wrap a Python object as an HTTP service and run that service.

    Args:
        obj (object): The object to be wrapped.
        host (str): An optional hostname for the service to listen on.
    """
    # Initialize Flask server.
    app = Flask(obj.__name__)

    # Get all methods from the object.
    methods = get_methods_from_object(obj)
    # Create partials objects where 'self' is set to the object.
    partial_methods = [build_partial_method(m, obj) for m in methods]

    # Add routing method(s) to Flask app.
    for method in partial_methods:
        add_method_route_to_flask(method, app)

    # Start the server.
    app.run(host=host)


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
    method_name = method.__name__

    # Create partial method and set 'self' parameter and name property.
    partial_method = partial(method, self=obj)
    partial_method.__name__ = method_name

    return partial_method


def add_method_route_to_flask(method, app):
    """Wrap a partial method into a Flask routing function.

    Args:
        method (functools.partial): Partial method to wrap. Needs to have a
            value for '__name__'.
        app (flask.Flask): Flask app to add to routing method to.
    """
    method_name = method.__name__

    # Add a new route for the method to the Flask app.
    route_decorator = app.route(f'/{method_name}', methods=['POST'])
    route = route_decorator(build_route(method))
    app.__dict__[method_name] = route


def build_route(method):
    """Wrap a method in a Flask route.

    Args:
        method (callable): The method to be wrapped.
    Returns:
        A Flask routing method.
    """
    def method_wrapper(*args, **kwargs):
        # Extract fields from JSON request.
        json_args = request.get_json()

        # Check is request contains all arguments of the function.
        # If not, exit with 422 (Unprocessable Entity) response.
        func_args = inspect.signature(method).parameters
        if not all(arg in json_args for arg in func_args if arg != 'self'):
            return f"Arguments for method {method.__name__!r} missing", 422

        # Call function with parameters from JSON request.
        res = method(**json_args)

        # Marshal JSON object from result.
        json_response = jsonify(res)

        return json_response
    return method_wrapper
