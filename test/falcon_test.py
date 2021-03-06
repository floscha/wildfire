import falcon
from falcon import testing
import wildfire

from _test_utils import Calculator


class FalconTest(testing.TestCase):
    def test_root_resource(self):
        self.app = wildfire.core._create_api(None)

        response = self.simulate_get('/')
        response_text = response.text

        self.assertEqual('This API is powered by Wildfire', response_text)

    def test_wildfire_with_calculator(self):
        self.app = wildfire.core._create_api(Calculator)

        response = self.simulate_post('/double', json={'number': 2})
        json_response = response.json

        self.assertIs(4, json_response)

    def test_add_method_route_to_api(self):
        def test_method():
            pass
        exptected_uri = '/test_method'

        api = falcon.API()

        wildfire.core.add_method_route_to_api(test_method, api)

        api_uris = [route.uri_template for route in api._router._roots]
        self.assertIn(exptected_uri, api_uris)

    def test_resource_returns_200_code(self):
        def test_method():
            pass
        expected_code = falcon.HTTP_200
        test_env = testing.create_environ()
        request = falcon.Request(test_env)
        response = falcon.Response()
        # response.status is 200 by default so set it to something else
        response.status = None

        resource = wildfire.core.build_resource_from_method(test_method)
        resource.on_post(request, response)

        self.assertEqual(expected_code, response.status)
