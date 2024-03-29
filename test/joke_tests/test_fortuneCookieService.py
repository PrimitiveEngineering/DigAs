""" test_fortuneCookieService
    * all basic-tests for fortuneCookie-Service are implemented here
    author:     inf20086@lehre.dhbw-stuttgart.de
    date:       04.04.2023
    version:    0.0.1
    license:    MIT
"""

import unittest
from joke.fortuneCookieService import FortuneCookieService

FCS = FortuneCookieService()


class TestFortuneCookieService(unittest.TestCase):
    def test_fortuneCookieServiceRequest_type(self):
        self.assertIsInstance(FCS.fortune_cookie_service_request(), str)

    def test_fortuneCookieServiceRequest_content(self):
        correct_string = "A beautiful, smart, and loving person will be coming into your life.\n"
        self.assertEqual(correct_string,FCS.fortune_cookie_service_request(joke_number=0))
