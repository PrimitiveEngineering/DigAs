""" test_timemgrCon
    * all basic-tests for time.py are implemented here
    author:     inf20086@lehre.dhbw-stuttgart.de
    date:       19.04.2023
    version:    0.0.1
    license:    MIT
"""
import unittest
from timemgr.timemgrCon import TimemgrCon
from core.speechToText import Speech2TextService
from core.textToSpeech import Text2SpeechService
from core.scheduleUtil import ScheduleUtil

t2s = Text2SpeechService("offline")
s2t = Speech2TextService("google")
schedule_util = ScheduleUtil()
TC = TimemgrCon(t2s, s2t, schedule_util)


class TestTimemgrCon(unittest.TestCase):
    def test_get_config(self):
        TC.get_config()
        self.assertTrue(True)

    def test_create_jobs(self):
        TC.create_jobs(1)
        self.assertTrue(True)

    def test_start_timemanager_routine_none(self):
        self.assertEqual(None, TC.start_timemanager_routine())

    def test_get_response_type_yes(self):
        correct_string = "yes"
        self.assertEqual(correct_string, TC.get_response_type("Dunkin Donuts"))

    def test_get_response_type_no(self):
        correct_string = "no"
        self.assertEqual(correct_string, TC.get_response_type("not"))
        self.assertEqual(correct_string, TC.get_response_type("dont"))
        self.assertEqual(correct_string, TC.get_response_type("don't"))
        self.assertEqual(correct_string, TC.get_response_type("already"))
        self.assertEqual(correct_string, TC.get_response_type("no"))

    def test_build_timemanager_starting_announcement(self):
        correct_string = f"Hey <say-as interpret-as=\"name\" format= \"undefined\">NAME</say-as>. " \
               f"You have an event coming up in REMTIME minutes. " \
               f"Would you like me to tell you more?"
        self.assertEqual(correct_string,TC.build_timemanager_starting_announcement("NAME","REMTIME"))

    def test_build_no_info_announcement(self):
        TC.build_no_info_announcement()
        self.assertTrue(True)

    def test_build_more_info_announcement(self):
        correct_string_one=f"The Event is EVENTNAME and you planned to go to EVENTLOC. Your description reads: EVENTDESC"
        self.assertEqual(correct_string_one,TC.build_more_info_announcement("EVENTNAME","EVENTLOC","EVENTDESC"))
