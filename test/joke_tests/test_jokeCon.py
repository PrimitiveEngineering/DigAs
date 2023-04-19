""" test_morningCon
    * all basic - tests for joke Controller are implemented here
    author:     inf20129@lehre.dhbw-stuttgart.de
    date:       05.04.2023
    version:    0.0.1
    license:    MIT
"""
import unittest
from joke.jokeCon import JokeCon
from core.speechToText import Speech2TextService
from core.textToSpeech import Text2SpeechService
from core.scheduleUtil import ScheduleUtil

t2s = Text2SpeechService("offline")
s2t = Speech2TextService("google")
schedule_util = ScheduleUtil()
JC = JokeCon(t2s, s2t, schedule_util)


class TestMorningCon(unittest.TestCase):

    def test_get_response_type(self):
        correct_data_one = "joke"
        correct_data_two = "quote"
        correct_data_three = "fortune_cookie"
        self.assertEqual(correct_data_one, JC.get_response_type("I would like to hear a joke"))
        self.assertEqual(correct_data_two, JC.get_response_type("I would love if you gave me an inspiring quote"))
        self.assertEqual(correct_data_three, JC.get_response_type("I would like if you would read me a fortune cookie"))

    def test_build_joke_starting_announcement(self):
        correct_data = f"Hey <say-as interpret-as=\"name\" format= \"undefined\">Bob</say-as>. " \
                       f"Would you like to hear a joke to lighten the mood? " \
                       f"Or an inspiring quote or a fortune cookie reading?"
        self.assertEqual(correct_data, JC.build_joke_starting_announcement("Bob"))

    def test_build_quote_announcement(self):
        correct_data = f"The quote i got for you is by <say-as interpret-as=\"name\" format= \"undefined\">Albert Einstein</say-as>." \
                       f" It goes as follows: " \
                       f"<break strength=\"strong\" />if she aint got the drip, she get no xxx"
        self.assertEqual(correct_data,
                         JC.build_quote_announcement("if she aint got the drip, she get no xxx", "Albert Einstein"))

    def test_build_joke_announcement(self):
        correct_data = f"The joke i got for you is: " \
                       f"<break strength=\"strong\" />Testing"
        self.assertEqual(correct_data, JC.build_joke_announcement("Testing"))

    def test_build_fortune_cookie_announcement(self):
        correct_data = f"Your fortune cookie reads: " \
                       f"<break strength=\"strong\" />If youre small now, dont worry - cause it wont make you grow"
        self.assertEqual(correct_data, JC.build_fortune_cookie_announcement(
            "If youre small now, dont worry - cause it wont make you grow"))
