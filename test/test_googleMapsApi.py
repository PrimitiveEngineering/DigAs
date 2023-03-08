""" test_main
    * all basic-tests for Google-Maps-API are implemented here
    author:     inf20086@lehre.dhbw-stuttgart.de
    date:       06.03.2023
    version:    0.0.1
    license:    MIT
"""

from unittest import TestCase
from core.googleMapsApi import GoogleMapsApi

GMA = GoogleMapsApi()
class TestGoogleMapsApi(TestCase):

    # def test_parameterValid(self):
    #     stringToTest = GMA.parameterValid(GMA, "walking", "origin", "dest", "url")
    #     self.assertEqual(stringToTest, "url&mode=walking&origins=origin&destinations=dest")

    def test_travelModeValid(self):
        self.assertEqual(True, GMA.travelModeValid("walking"))

    def test_originIsString(self):
        self.assertEqual(True, GMA.originIsString("iFartInYourGeneralDirection"))

    def test_destinationIsString(self):
        self.assertEqual(True, GMA.destinationIsString("tisButAScratch"))
