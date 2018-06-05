import inspect
import json
import unittest

import flask

import wildfire


class Calculator(object):
    """A simple calculator class."""

    def double(self, number):
        return 2 * number


class CoreTest(unittest.TestCase):
    """Test suite for all functionality of the wildfire.core module."""

    def test_wildfire_with_calculator(self):
        app = wildfire.core._create_wildfire_app(Calculator)
        client = app.test_client()

        response = client.post('/double',
                               data=json.dumps({'number': 2}),
                               content_type='application/json')
        json_response = json.loads(response.data)

        self.assertIs(4, json_response)

    def test_method_names_from_object(self):
        methods = wildfire.core.get_methods_from_object(Calculator)
        method_names = [m.__name__ for m in methods]

        self.assertListEqual(['double'], method_names)

    def test_build_partial_method(self):
        def test_method(self): pass
        test_object = object()

        partial_method = wildfire.core.build_partial_method(test_method,
                                                            test_object)

        self_param = inspect.signature(partial_method).parameters['self']
        self_param_value = self_param.default
        self.assertIs(test_object, self_param_value)

    def test_add_method_route_to_flask(self):
        def test_method():
            pass

        app = flask.Flask(__name__)

        wildfire.core.add_method_route_to_flask(test_method, app)

        self.assertIn('test_method', app.__dict__)

    def test_build_route(self):
        def test_method(test_string):
            return test_string

        app = flask.Flask(__name__)

        test_message = dict(data=json.dumps({'test_string': 'test string'}),
                            content_type='application/json')
        with app.test_request_context('/', **test_message):
            route_method = wildfire.core.build_route(test_method)

            response = route_method()

        json_response = json.loads(response.data)

        self.assertTrue('test string' == json_response)


if __name__ == '__main__':
    unittest.main()
