""" test_calenderAPI
    * all basic-tests for time.py are implemented here
    author:     inf20086@lehre.dhbw-stuttgart.de
    date:       19.04.2023
    version:    0.0.1
    license:    MIT
"""
import unittest
from datetime import datetime, timedelta

from timemgr.calenderAPI import CalenderAPI

CAPI = CalenderAPI()

test_date_one = datetime.now()
test_date_two = datetime.now() + timedelta(minutes=1)


class TestCalenderAPI(unittest.TestCase):

    def test_create_event(self):
        CAPI.create_event("TEST", test_date_one, test_date_two)
        self.assertTrue(True)

    def test_print_events(self):
        CAPI.print_events()

        self.assertTrue(True)

    def test_get_events_24h(self):
        test_list = CAPI.get_events_24h()
        self.assertIsNot(test_list, [])

    def test_get_events_24h_list(self):
        test_list = CAPI.get_events_24h_list()
        self.assertIsNot(test_list, [])

    def test_get_events(self):
        test_list = CAPI.get_events(test_date_one, test_date_two)
        self.assertIsNot(test_list, [])

    def test_get_events_now(self):
        test_list = CAPI.get_events_now()
        self.assertIsNot(test_list, [])

    def test_is_event_now(self):
        test_var = CAPI.is_event_now()
        self.assertIsNot(test_var, None)
