""" test_googleMapsApi
    * all basic-tests for Google-Maps-API are implemented here
    author:     inf20086@lehre.dhbw-stuttgart.de
    date:       22.03.2023
    version:    0.0.1
    license:    MIT
"""

from unittest import TestCase
from morning.googleMapsApi import GoogleMapsApi
from datetime import datetime, timedelta
import json, os

GMA = GoogleMapsApi()


class TestGoogleMapsApi(TestCase):

    def test_parameterValid(self):
        string_correct = "url&mode=transit&arrival_time=1704021753&origins=origin&destinations=dest"
        datetime_str = '12/31/23 11:22:33'
        datetime_object = datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S')

        string_to_test = GMA.parameter_valid("transit", "origin", "dest", datetime_object, "url")

        self.assertEqual(string_correct, string_to_test)

    def test_travelModeValid(self):
        self.assertEqual(True, GMA.travel_mode_valid("walking"))

    def test_originIsString(self):
        self.assertEqual(True, GMA.origin_is_string("iFartInYourGeneralDirection"))

    def test_destinationIsString(self):
        self.assertEqual(True, GMA.destination_is_string("tisButAScratch"))

    def test_getDuration(self):
        f = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'testResponse.json'), "r", encoding='utf8')
        data = json.load(f)
        f.close()
        correct_string = "1 hour 56 minutes"
        self.assertEqual(correct_string, GMA.get_duration(data))

    def test_getDistance(self):
        f = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'testResponse.json'), "r", encoding='utf8')
        data = json.load(f)
        f.close()
        correct_string = "69.1 kilometer"
        self.assertEqual(correct_string, GMA.get_distance(data))

    def test_getDurationValue(self):
        f = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'testResponse.json'), "r", encoding='utf8')
        data = json.load(f)
        f.close()
        correct_string = 6969
        self.assertEqual(correct_string, GMA.get_duration_value(data))

    def test_getDistanceValue(self):
        f = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'testResponse.json'), "r", encoding='utf8')
        data = json.load(f)
        f.close()
        correct_string = 42069
        self.assertEqual(correct_string, GMA.get_distance_value(data))

    def test_googleMapsApiRequest(self):
        correct_string = ('33.0 kilometer', '1 hour 30 minutes')
        tom_date = datetime.now() + timedelta(1)
        tom_day = tom_date.day
        tom_month = tom_date.month
        tom_year = tom_date.year

        self.assertEqual(correct_string, GMA.google_maps_api_request("Filderstadt", "Stuttgart", 'transit',
                                                                     arrival_time=datetime(tom_year, tom_month, tom_day,
                                                                                           3)))
