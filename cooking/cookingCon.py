from cooking.foodApi import FoodApi
from cooking.musicApi import MusicApi
from cooking.randomSongPicker import RandomSongPicker
from core.util import Speech2TextUtil
import schedule
import yaml
import numpy as np
import os
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
        schedule.every().day.at("00:00").do(self.start_cooking_routine).tag("joke_routine")
        self.get_config()

    def get_config(self):
        """
        Reading the config file and writing parameters to class attributs
        excpected:
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
                schedule.every().day.at(time_start).do(self.start_joke_routine).tag("cooking_routine")

    def start_cooking_routine(self):
        """
        Runs the cooking routine
        :return: none
        """

        self.get_config()

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

    def get_recipe_type(self, user_input):
        """
        Response type decider
        :param user_input: s2t user input as text
        :return: response_type
        """

        if any(element in user_input for element in ["recipe", "random"]):
            recipe_type = "recipe"
        else:
            recipe_type = "ingredients"

        return recipe_type

    def build_cooking_starting_announcement(self, name):
        """
        The t2s text for starting the cooking-functionality
        :param name:
        :return:
        """

        return f"Hey <say-as interpret-as=\"name\" format= \"undefined\">{name}</say-as>. " \
               f"I can search for a random recipe" \
               f"Alternatively you can say ingredients to find a recipe with certain ingredients."

    def run_recipe_choice(self, recipe_type, user_input):
        """
        Runs the user requested api
        :param recipe_type: The requested choice
        :param user_input: The requested recipe if "recipe" was chosen
        """

        if recipe_type == "recipe":
            foodAPI = FoodApi()
            name, ingredients, steps = foodAPI.food_api_random_request()

            self.__t2s.trigger(
                self.build_recipe_announcement(
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

        text = f"The name of the recipe is {name}." \
               f"The ingredients for this recipe are the following."

        for ingred in ingredients:
            #CONTINUE HERE

        # return f"The quote i got for you is by <say-as interpret-as=\"name\" format= \"undefined\">{author}</say-as>. " \
        #        f"It goes as follows: " \
        #        f"<break strength=\"strong\" />{quote}"
