""" test_cooking_Con
    * all basic-tests for cooking-Controller are implemented here
    author:     inf20086@lehre.dhbw-stuttgart.de
    date:       18.04.2023
    version:    0.0.1
    license:    MIT
"""
import unittest
from cooking.cookingCon import CookingCon
from core.speechToText import Speech2TextService
from core.textToSpeech import Text2SpeechService

t2s = Text2SpeechService("offline")
s2t = Speech2TextService("google")
CC = CookingCon(t2s, s2t)


class TestCookingCon(unittest.TestCase):

    def test_get_config(self):
        CC.get_config()
        self.assertTrue(True)

    def test_get_recipe_type_nothing(self):
        correct_response = "nothing"
        self.assertEqual(correct_response, CC.get_recipe_type("no"))
        self.assertEqual(correct_response, CC.get_recipe_type("don't"))

    def test_get_recipe_type_recipe(self):
        correct_response = "recipe"
        self.assertEqual(correct_response, CC.get_recipe_type("recipe"))
        self.assertEqual(correct_response, CC.get_recipe_type("random"))

    def test_get_recipe_type_ingredients(self):
        correct_response = "ingredients"
        self.assertEqual(correct_response, CC.get_recipe_type("Order 66"))

    def test_get_music_type_nothing(self):
        correct_response = "nothing"
        self.assertEqual(correct_response, CC.get_music_type("no"))
        self.assertEqual(correct_response, CC.get_music_type("don't"))

    def test_get_music_type_random(self):
        correct_response = "random"
        self.assertEqual(correct_response, CC.get_music_type("random"))

    def test_get_music_type_request(self):
        correct_response = "request"
        self.assertEqual(correct_response, CC.get_music_type("Order 66"))

    def test_build_music_starting_announcement(self):
        correct_string = f"Do you want to listen to music? " \
                         f"You can request a song or say random to randomly chose a song from an artist you like."
        self.assertEqual(correct_string, CC.build_music_starting_announcement())

    def test_build_cooking_starting_announcement(self):
        correct_string = f"Hey <say-as interpret-as=\"name\" format= \"undefined\">NAME</say-as>. " \
                         f"Do you want to cook something?. " \
                         f"If so i can search for a random recipe. " \
                         f"Alternatively you can list ingredients so i can find a recipe with these ingredients. "
        self.assertEqual(correct_string, CC.build_cooking_starting_announcement("NAME"))

    def test_run_music_choice_nothing(self):
        CC.run_music_choice("nothing", "Days of Blue")
        self.assertTrue(True)

    def test_run_music_choice(self):
        CC.run_music_choice("random", "Days of Blue")
        self.assertTrue(True)

    def test_run_music_other(self):
        CC.run_music_choice("rock", "Days of Blue")
        self.assertTrue(True)

    def test_build_chosen_music_announcement(self):
        correct_string = f"Playing TITLE"
        self.assertEqual(correct_string, CC.build_chosen_music_announcement("TITLE"))

    def test_build_random_music_announcement(self):
        correct_string = f"The song is called TITLE from <say-as interpret-as=\"name\" format= \"undefined\">ARTIST" \
                         "</say-as>"
        self.assertEqual(correct_string, CC.build_random_music_announcement("TITLE", "ARTIST"))

    def test_run_recipe_choice_nothing(self):
        CC.run_recipe_choice("nothing", "MEAT")
        self.assertTrue(True)

    def test_run_recipe_choice_recipe(self):
        CC.run_recipe_choice("recipe", "MEAT")
        self.assertTrue(True)

    def test_run_recipe_choice_other(self):
        CC.run_recipe_choice("ORDER", "MEAT")
        self.assertTrue(True)
