""" test_morningCon
    * all basic - tests for morning Controller are implemented here
    author:     inf20086@lehre.dhbw-stuttgart.de
    date:       05.04.2023
    version:    0.0.1
    license:    MIT
"""
import unittest
from morning.morningCon import MorningCon
from core.speechToText import Speech2TextService
from core.textToSpeech import Text2SpeechService

t2s = Text2SpeechService("offline")
s2t = Speech2TextService("google")
MC = MorningCon(t2s, s2t)


class TestMorningCon(unittest.TestCase):

    def test_get_travel_mode(self):
        correct_data_one = ("transit", "by train")
        correct_data_two = ("bicycling", "by bike")
        correct_data_three = ("walking", "on foot")
        correct_data_four = ("driving", "by car")
        self.assertEqual(correct_data_one, MC.get_travel_mode("train"))
        self.assertEqual(correct_data_one, MC.get_travel_mode("subway"))
        self.assertEqual(correct_data_one, MC.get_travel_mode("metro"))
        self.assertEqual(correct_data_one, MC.get_travel_mode("tube"))
        self.assertEqual(correct_data_two, MC.get_travel_mode("bicycle"))
        self.assertEqual(correct_data_two, MC.get_travel_mode("bike"))
        self.assertEqual(correct_data_three, MC.get_travel_mode("walk"))
        self.assertEqual(correct_data_three, MC.get_travel_mode("foot"))
        self.assertEqual(correct_data_four, MC.get_travel_mode("Wingardium Leviosa"))

    def test_build_weather_announcement(self):
        correct_string = f"Good morning <say-as interpret-as=\"name\" format= \"undefined\">NAME</say-as>. " \
                         f"The current time is <say-as interpret-as=\"time\" format=\"undefined\">TIME</say-as>. " \
                         f"The weather outside is WEATHER. The temperature right now is TEMP degrees " \
                         f"and it feels like TEMPFEELS degrees. " \
                         f"Today's max temperature will be about TEMPMAX degrees.<break strength=\"strong\" /> " \
                         f"What means of transportation do you want to use to get to work?"
        self.assertEqual(correct_string,
                         MC.build_weather_announcement("NAME", "TIME", "WEATHER", "TEMP", "TEMPFEELS", "TEMPMAX"))

    def test_build_travel_time_announcement(self):
        correct_string = f"The estimated travel time from <lang xml:lang=\"de-DE\">ORIGIN</lang> " \
                         f"to your workplace <lang xml:lang=\"de-DE\">DESTINATION</lang> " \
                         f"TRAVEL will be about DURATION."
        self.assertEqual(correct_string,
                         MC.build_travel_time_announcement("ORIGIN", "DESTINATION", "DURATION", "TRAVEL"))
