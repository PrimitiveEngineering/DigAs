from joke.jokeApi import JokeApi
from joke.fortuneCookieService import FortuneCookieService
from joke.quoteApi import QuoteApi
from core.util import Speech2TextUtil
import schedule
import yaml
import numpy as np
import os


# from datetime import datetime


class JokeCon:
    __instance = None
    __t2s = None
    __s2t = None

    __username = "Debug"
    __times_start = ["10:15", "17:30", "20:30"]
    __blacklist = []

    # singleton pattern
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, t2s, s2t):
        """
        joke Service
        :param t2s: Text2Speech Service
        :param s2t: Speech2Text Service
        """

        self.__t2s = t2s
        self.__s2t = s2t
        schedule.every().day.at("00:00").do(self.start_joke_routine).tag("joke_routine")
        self.get_config()

        # Schedule a job for the next minute DEBUG
        # now = datetime.now()
        # nowplus1 = now.strftime("%H") + ":" + str(int(now.strftime("%M")) + 1)
        # print(nowplus1)
        # schedule.every().day.at(nowplus1).do(self.start_joke_routine).tag("joke_routine")

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
        self.__times_start = yaml_config["joke"]["times"]
        self.__blacklist = yaml_config["joke"]["blacklist"]

        # Reset time of alarm
        if not np.array_equiv(old_times, self.__times_start):
            schedule.clear("joke_routine")
            for time_start in self.__times_start:
                schedule.every().day.at(time_start).do(self.start_joke_routine).tag("joke_routine")

    def start_joke_routine(self):
        """
        Runs the joke routine
        :return: none
        """

        self.get_config()

        self.__t2s.trigger(
            self.build_joke_starting_announcement(
                self.__username),
            True)

        user_input, termination_desire = Speech2TextUtil().user_input_func(self.__s2t, self.__t2s)

        if termination_desire:
            self.__t2s.trigger("Terminating", False)
            return

        response_type = self.get_response_type(user_input)
        self.run_user_choice(response_type)

    def get_response_type(self, user_input):
        """
        Response type decider
        :param user_input: s2t user input as text
        :return: response_type
        """

        if any(element in user_input for element in ["quote", "famous"]):
            response_type = "quote"
        elif any(element in user_input for element in ["fortune", "cookie"]):
            response_type = "fortune_cookie"
        else:
            response_type = "joke"

        return response_type

    def run_user_choice(self, response_type):
        """
        Runs the user requested api
        :param response_type: The requested choice
        """

        if response_type == "quote":
            quoteAPI = QuoteApi()
            quote, author = quoteAPI.quote_api_request()

            self.__t2s.trigger(
                self.build_quote_announcement(
                    quote,
                    author),
                True)

        elif response_type == "fortune_cookie":
            fortune_cookieApi = FortuneCookieService()
            reading = fortune_cookieApi.fortune_cookie_service_request()

            self.__t2s.trigger(
                self.build_fortune_cookie_announcement(
                    reading),
                True)

        else:
            jokeAPI = JokeApi()
            if len(self.__blacklist) == 0:
                joke = jokeAPI.joke_api_request()
            else:
                joke = jokeAPI.joke_api_request(self.__blacklist)

            self.__t2s.trigger(
                self.build_joke_announcement(
                    joke),
                True)

    def build_joke_starting_announcement(self, name):
        """
        The t2s text for starting the joke-functionality
        :param name:
        :return:
        """

        return f"Hey <say-as interpret-as=\"name\" format= \"undefined\">{name}</say-as>. " \
               f"Would you like to hear a joke to lighten the mood? " \
               f"Or an inspiring quote or a fortune cookie reading? "

    def build_quote_announcement(self, quote, author):
        """
        The t2s text for the quote announcement
        :param author:
        :param quote:
        :return:
        """

        return f"The quote i got for you is by <say-as interpret-as=\"name\" format= \"undefined\">{author}</say-as>. " \
               f"It goes as follows: " \
               f"<break strength=\"strong\" />{quote}"

    def build_joke_announcement(self, joke):
        """
        The t2s text for the joke announcement
        :param joke:
        :return:
        """

        return f"The joke i got for you is: " \
               f"<break strength=\"strong\" />{joke}"

    def build_fortune_cookie_announcement(self, reading):
        """
        The t2s text for the fortune cookie reading
        :param reading:
        :return:
        """

        return f"Your fortune cookie reads: " \
               f"<break strength=\"strong\" />{reading}"
