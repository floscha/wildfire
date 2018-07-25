from falcon import testing
import wildfire

from _test_utils import Calculator


class FalconTest(testing.TestCase):

    def test_wildfire_with_calculator(self):
        self.app = wildfire.core._create_api(Calculator)

        response = self.simulate_post('/double',
                                      json={'number': 2})
        json_response = response.json

        self.assertIs(4, json_response)
