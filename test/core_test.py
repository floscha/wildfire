import inspect
import unittest

import flask

import wildfire


class Calculator(object):
    """A simple calculator class."""

    def double(self, number):
        return 2 * number


class CoreTest(unittest.TestCase):
    """Test suite for all functionality of the wildfire.core module."""

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
        # test_method.__name__ = 'test_method'
        app = flask.Flask(__name__)

        wildfire.core.add_method_route_to_flask(test_method, app)

        self.assertIn('test_method', app.__dict__)


if __name__ == '__main__':
    unittest.main()
