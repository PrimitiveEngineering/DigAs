""" test_fortuneCookieService
    * all basic-tests for fortune cookie service are implemented here
    author:     inf20086@lehre.dhbw-stuttgart.de
    date:       24.03.2023
    version:    0.0.1
    license:    MIT
"""
from unittest import TestCase
from joke.fortuneCookieService import FortuneCookieService

FCS = FortuneCookieService()


class TestFortuneCookieService(TestCase):

    def test_fortune_cookie_service_request(self):
        result = "yes"
        self.assertIsInstance(FCS.fortuneCookieServiceRequest(),str)