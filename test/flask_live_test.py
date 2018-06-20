import unittest

from flask.ext.testing import LiveServerTestCase
import requests
import wildfire


class FlaskLiveTest(LiveServerTestCase):
    @staticmethod
    def create_app():
        def test_method():
            return 'test_string'

        app = wildfire.core._create_wildfire_app(test_method)

        return app

    def test_flask_application_is_up_and_running(self):
        test_url = '%s/%s' % (self.get_server_url(), 'test_method')
        response = requests.post(test_url, json={})

        self.assertEqual(200, response.status_code)


if __name__ == '__main__':
    unittest.main()
