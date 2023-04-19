""" test_scheduleUtil
    * all basic-tests for scheduleUtil are implemented here
    author:     inf20086@lehre.dhbw-stuttgart.de
    date:       19.04.2023
    version:    0.0.1
    license:    MIT
"""
import unittest, schedule

from core.scheduleUtil import ScheduleUtil
from timemgr.calenderAPI import CalenderAPI
from datetime import datetime, timedelta
import pytz

SU = ScheduleUtil()
CAPI = CalenderAPI()
job = schedule.get_jobs()


class TestScheduleUtil(unittest.TestCase):
    def test_get_config(self):
        SU.get_config()
        self.assertTrue(True)

    def test_load_config_registrator(self):
        SU.load_config_registrator([])
        self.assertTrue(True)

    def test_load_config(self):
        SU.load_config()
        self.assertTrue(True)

    def test_meeting_guard_socket(self):
        SU.meeting_guard_socket(CAPI.get_events_24h_list())
        self.assertTrue(True)

    def test_meeting_guard(self):
        SU.meeting_guard()
        self.assertTrue(True)

    def test_clean_timezones(self):
        date_one = [[datetime(2011, 8, 15, 8, 15, 12, 0, pytz.UTC)]]
        date_two = [[datetime(2011, 8, 15, 8, 15, 12, 0)]]
        self.assertEqual(date_two, SU.clean_timezones(date_one))

    def test_check_jobs_meeting(self):
        date = [[datetime(2011, 8, 15, 8, 15, 12, 0)]]
        SU.check_jobs_meeting(job, date, 5)
        self.assertTrue(True)

    def test_check_meeting_overlap(self):
        date = [[datetime.now(), datetime.now() + timedelta(minutes=1)]]
        SU.check_meeting_overlap(job[0], date, 5)
        self.assertTrue(True)

    def test_check_jobs(self):
        SU.check_jobs(job, 5)
        self.assertTrue(True)

    def test_check_job_overlap(self):
        SU.check_job_overlap(job[0], job, 5)
        self.assertTrue(True)
