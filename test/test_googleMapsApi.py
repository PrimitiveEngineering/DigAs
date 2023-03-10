""" test_main
    * all basic-tests for Google-Maps-API are implemented here
    author:     inf20086@lehre.dhbw-stuttgart.de
    date:       06.03.2023
    version:    0.0.1
    license:    MIT
"""

from unittest import TestCase
from core.googleMapsApi import GoogleMapsApi
from datetime import datetime

GMA = GoogleMapsApi()


class TestGoogleMapsApi(TestCase):

    def test_parameterValid(self):
        stringCorrect = "url&mode=transit&arrival_time=1704021753&origins=origin&destinations=dest"
        datetime_str = '12/31/23 11:22:33'
        datetime_object = datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S')

        stringToTest = GMA.parameterValid("transit", "origin", "dest", datetime_object, "url")

        self.assertEqual(stringCorrect, stringToTest)


    def test_travelModeValid(self):
        self.assertEqual(True, GMA.travelModeValid("walking"))


    def test_originIsString(self):
        self.assertEqual(True, GMA.originIsString("iFartInYourGeneralDirection"))


    def test_destinationIsString(self):
        self.assertEqual(True, GMA.destinationIsString("tisButAScratch"))


    def test_selfTest(self):
        self.assertEqual(True, True)  # We love it!!!


'''
Anfrage:
print(gMaps.googleMapsApiRequest("Filderstadt", "Stuttgart", 'transit', arrivalTime=datetime(2023, 3, 12, 3)))

{
    "destination_addresses" : [ "Stuttgart, Germany" ],
    "origin_addresses" : [ "Filderstadt, Germany" ],
    "rows" : [
        {
            "elements" : [
            {
                "distance" : {
                    "text" : "22.9 km",
                    "value" : 22851
                },
                "duration" : {
                    "text" : "1 hour 9 mins",
                    "value" : 4113
                },
                "status" : "OK"
            }
            ]
        }
    ],
    "status" : "OK"
}

Output:
('22.9 kilometer', '1 stunde 9 minuten')


Für weitere Konfigs -> Class description
'''
