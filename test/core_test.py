import unittest

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


if __name__ == '__main__':
    unittest.main()
