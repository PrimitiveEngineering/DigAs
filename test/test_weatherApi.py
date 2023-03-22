""" test_weatherApi
    * all basic-tests for weatherApi are implemented here
    author:     inf20086@lehre.dhbw-stuttgart.de
    date:       22.03.2023
    version:    0.0.1
    license:    MIT
"""

from unittest import TestCase
from morning.weatherApi import OpenWeather
from unittest.mock import patch

OW = OpenWeather()


class TestWeatherApi(TestCase):

    def test_get_weather_valid_city(self):
        mock_response = {"cod": 200, "weather": [{"description": "sunny"}],
                         "main": {"temp": 300, "feels_like": 295, "temp_max": 305}}
        with patch("requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = mock_response

            result = OW.get_weather("Los Santos")

            self.assertEqual(result, {'description': 'sunny', 'feels_like': 21.9, 'max_temp': 31.9, 'temp': 26.9})

    def test_kelvin_to_celsius(self):
        correct_value = 0
        self.assertEqual(correct_value, OW.kelvin_to_celsius(273.15))
