""" test_time
    * all basic-tests for time.py are implemented here
    author:     inf20086@lehre.dhbw-stuttgart.de
    date:       17.04.2023
    version:    0.0.1
    license:    MIT
"""

import unittest
import datetime
from timemgr.time import Time

T = Time()


class TestTime(unittest.TestCase):
    def test_get_current_time_default(self):
        expected_time = datetime.datetime.now().strftime("%H:%M")
        self.assertEqual(expected_time, T.get_current_time())

    def test_get_current_time_custom(self):
        expected_time = datetime.datetime.now().strftime("%I:%M %p")
        self.assertEqual(expected_time, T.get_current_time("%I:%M %p"))

    def test_get_current_date(self):
        expected_date = datetime.datetime.now().strftime("%Y/%m/%d")
        self.assertEqual(expected_date, T.get_current_date())

    def test_get_current_date_time(self):
        expected_date_time = datetime.datetime.now().strftime("%Y/%m/%d %H:%M")
        self.assertEqual(expected_date_time, T.get_current_date_time())

    def test_change_date_format_t2s(self):
        date = '2022-03-15'
        date_format = '%Y-%m-%d'
        expected_result = '2022/03/15'
        self.assertEqual(T.change_date_format_t2s(date, date_format), expected_result)

    def test_change_date_time_format_t2s(self):
        date_time = '2022-03-15 08:45:30'
        date_time_format = '%Y-%m-%d %H:%M:%S'
        expected_result = '2022/03/15 08:45'
        self.assertEqual(T.change_date_time_format_t2s(date_time, date_time_format), expected_result)

    def test_split_date_time(self):
        date_time = '2022/03/15 08:45'
        expected_date = '2022/03/15'
        expected_time = '08:45'
        self.assertEqual(T.split_date_time(date_time), (expected_date, expected_time))
