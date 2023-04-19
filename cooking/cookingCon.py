import os

import numpy as np
import schedule
import yaml

from cooking.foodApi import FoodApi
from cooking.musicApi import MusicApi
from cooking.randomSongPicker import RandomSongPicker
from core.util import Speech2TextUtil


class CookingCon:
    __instance = None
    __t2s = None
    __s2t = None

    __username = "Debug"
    __times_start = ["18:00"]
    __artist = []

    # singleton pattern
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, t2s, s2t):
        """
        Cooking Service
        :param t2s: Text2Speech Service
        :param s2t: Speech2Text Service
        """

        self.__t2s = t2s
        self.__s2t = s2t
        self.music_api = MusicApi()
        self.random_song_picker = RandomSongPicker()
        self.food_api = FoodApi()
        schedule.every().day.at("00:00").do(self.start_cooking_routine).tag("cooking_routine")
        self.get_config()

    def get_config(self):
        """
        Reading the config file and writing parameters to class attributes
        expected:
            global.username -> string
            joke.times -> array
            joke.blacklist -> array
        :return:
        """

        old_times = self.__times_start

        with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config.yaml')), "r") as file:
            yaml_config = yaml.safe_load(file)

        self.__username = yaml_config["global"]["username"]
        self.__times_start = yaml_config["cooking"]["times"]
        self.__artist = yaml_config["cooking"]["artist"]

        # Reset time of alarm
        if not np.array_equiv(old_times, self.__times_start):
            schedule.clear("cooking_routine")
            for time_start in self.__times_start:
                schedule.every().day.at(time_start).do(self.start_cooking_routine).tag("cooking_routine")

    def start_cooking_routine(self):
        """
        Runs the cooking routine
        :return: none
        """

        self.get_config()

        # FoodApi
        self.__t2s.trigger(
            self.build_cooking_starting_announcement(
                self.__username),
            True)

        user_input, termination_desire = Speech2TextUtil().user_input_func(self.__s2t, self.__t2s)

        if termination_desire:
            self.__t2s.trigger("Terminating", False)
            return

        recipe_type = self.get_recipe_type(user_input)
        self.run_recipe_choice(recipe_type, user_input)

        # MusicApi
        self.__t2s.trigger(self.build_music_starting_announcement(), True)

        user_input, termination_desire = Speech2TextUtil().user_input_func(self.__s2t, self.__t2s)

        if termination_desire:
            self.__t2s.trigger("Terminating", False)
            return

        get_music_type = self.get_music_type(user_input)
        self.run_music_choice(get_music_type, user_input)

    def get_recipe_type(self, user_input):
        """
        Response type decider
        :param user_input: s2t user input as text
        :return: recipe_type
        """

        if any(element in user_input for element in ["no", "don't"]):
            recipe_type = "nothing"
        elif any(element in user_input for element in ["recipe", "random"]):
            recipe_type = "recipe"
        else:
            recipe_type = "ingredients"

        return recipe_type

    def get_music_type(self, user_input):
        """
        Response type decider
        :param user_input: s2t user input as text
        :return: music_type
        """

        if any(element in user_input for element in ["no", "don't"]):
            music_type = "nothing"
        elif any(element in user_input for element in ["random"]):
            music_type = "random"
        else:
            music_type = "request"

        return music_type

    def build_music_starting_announcement(self):
        """
        The t2s text for starting the cooking-functionality
        """

        return f"Do you want to listen to music? " \
               f"You can request a song or say random to randomly chose a song from an artist you like."

    def build_cooking_starting_announcement(self, name):
        """
        The t2s text for starting the cooking-functionality
        :param name:
        :return:
        """

        return f"Hey <say-as interpret-as=\"name\" format= \"undefined\">{name}</say-as>. " \
               f"Do you want to cook something?. " \
               f"If so i can search for a random recipe. " \
               f"Alternatively you can list ingredients so i can find a recipe with these ingredients. "

    def run_music_choice(self, music_type, user_input):
        """
        Runs the user requested api
        :param music_type: The requested choice
        :param user_input: The requested music
        """

        if music_type == "nothing":
            self.__t2s.trigger('Alright. ', True)
        elif music_type == "random":
            title, artist = self.random_song_picker.random_song_picker_request(self.__artist)
            self.__t2s.trigger(
                self.build_random_music_announcement(
                    title,
                    artist),
                True)
            self.music_api.play_requested_song(title, artist)
        else:
            self.__t2s.trigger(
                self.build_chosen_music_announcement(
                    user_input),
                True)
            self.music_api.play_requested_song(user_input)

    def build_chosen_music_announcement(self, title):
        """
        The t2s text for the recipe announcement
        :param title:
        :return:
        """

        return f"Playing {title}"

    def build_random_music_announcement(self, title, artist):
        """
        The t2s text for the recipe announcement
        :param title:
        :param artist:
        :return:
        """

        return f"The song is called {title} from <say-as interpret-as=\"name\" format= \"undefined\">{artist}" \
               "</say-as>"

    def run_recipe_choice(self, recipe_type, user_input):
        """
        Runs the user requested api
        :param recipe_type: The requested choice
        :param user_input: The requested recipe if "recipe" was chosen
        """

        if recipe_type == "nothing":
            self.__t2s.trigger('Alright. ', True)
        elif recipe_type == "recipe":
            name, ingredients, steps = self.food_api.food_api_random_request()

            self.__t2s.trigger(
                self.build_recipe_announcement(
                    name,
                    ingredients,
                    steps),
                True)
        else:
            name, ingredients, steps = self.food_api.food_api_find_by_ingredients_request(
                self.user_input_to_ingredient_list(user_input))
            self.__t2s.trigger(
                self.build_ingredients_announcement(
                    name,
                    ingredients,
                    steps),
                True)

    def build_recipe_announcement(self, name, ingredients, steps):
        """
        The t2s text for the recipe announcement
        :param name:
        :param ingredients:
        :param steps:
        :return:
        """

        text = f"The name of the recipe is {name}. " \
               f"The ingredients for this recipe are the following. "

        for key in ingredients:
            text += key + " " + ingredients[key] + ". "

        if not steps:
            text += f"This recipe does not include a step by step instruction. "
        else:
            text += f"The instructions for this recipe are the following. "

            for step in steps:
                text += step + ' '
                if '.' not in step:
                    text += f". "

        return text

    def build_ingredients_announcement(self, name, ingredients, steps):
        """
        The t2s text for the ingredient recipe announcement
        :param name:
        :param ingredients:
        :param steps:
        :return:
        """

        text = f"Here is a recipe with the wanted ingredients. "
        return text + self.build_recipe_announcement(name, ingredients, steps)

    def user_input_to_ingredient_list(self, user_input):
        return user_input.split()
