from morning.weatherApi import OpenWeather
from morning.googleMapsApi import GoogleMapsApi
from core.speechToTextUtil import Speech2TextUtil
import schedule
import yaml
import os


class MorningCon:
    __instance = None
    __t2s = None
    __s2t = None

    __username = "Richard"
    __time_alarm = "10:00"
    __city = "Stuttgart"
    __origin = "Gropiusplatz 9 Stuttgart"
    __destination = "DHBW Fakultät Technik Stuttgart"

    # singleton pattern
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, t2s, s2t, schedule_util):
        """
        Morning Service
        :param t2s: Text2Speech Service
        :param s2t: Speech2Text Service
        :param schedule_util: Schedule Utility Service
        """

        self.__t2s = t2s
        self.__s2t = s2t
        schedule.every().day.at(self.__time_alarm).do(self.start_morning_routine).tag("morning_routine")
        self.get_config()
        schedule_util.load_config_registrator(self.get_config)

    def get_config(self):
        """
        Reading the config file and writing parameters to class attributs
        excpected:
            global.username -> string
            morning.alarm -> string
            morning.city -> string
            morning.origin -> string
            morning.destination -> string
        :return:
        """

        old_time_alarm = self.__time_alarm
        with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config.yaml')), "r") as file:
            yaml_config = yaml.safe_load(file)

        self.__username = yaml_config["global"]["username"]
        self.__time_alarm = yaml_config["morning"]["alarm"]
        self.__city = yaml_config["morning"]["city"]
        self.__origin = yaml_config["morning"]["origin"]
        self.__destination = yaml_config["morning"]["destination"]

        # Reset time of alarm
        if old_time_alarm != self.__time_alarm:
            schedule.clear("morning_routine")
            schedule.every().day.at(self.__time_alarm).do(self.start_morning_routine).tag("morning_routine")

    def start_morning_routine(self):
        """
        Runs the morning routine
        :return:
        """

        self.get_config()

        weather = OpenWeather().get_weather(self.__city)

        self.__t2s.trigger(
            self.build_weather_announcement(
                self.__username,
                self.__time_alarm,
                weather["description"],
                weather["temp"],
                weather["feels_like"],
                weather["max_temp"]),
            True)

        user_input, termination_desire = Speech2TextUtil().user_input_func(self.__s2t, self.__t2s)

        if termination_desire:
            self.__t2s.trigger("Terminating", False)
            return

        travel_mode, travel_mode_announcement = self.get_travel_mode(user_input)

        duration = GoogleMapsApi().google_maps_api_request(
            self.__origin,
            self.__destination,
            travel_mode,
            None,
            True)[1]

        self.__t2s.trigger(
            self.build_travel_time_announcement(
                self.__origin,
                self.__destination,
                duration,
                travel_mode_announcement),
            True)

    def get_travel_mode(self, user_input):
        """
        Travel mode decider
        :param user_input: s2t user input as text
        :return: 2 values: travel_mode and travel_mode_announcement
        """

        if any(element in user_input for element in ["train", "subway", "metro", "tube"]):
            travel_mode = "transit"
            travel_mode_announcement = "by train"
        elif any(element in user_input for element in ["bicycle", "bike"]):
            travel_mode = "bicycling"
            travel_mode_announcement = "by bike"
        elif any(element in user_input for element in ["walk", "foot"]):
            travel_mode = "walking"
            travel_mode_announcement = "on foot"
        else:
            travel_mode = "driving"
            travel_mode_announcement = "by car"

        return (travel_mode, travel_mode_announcement)

    def build_weather_announcement(self, name, time, weather_desc, temp, temp_feels_like, temp_max):
        """
        The t2s text for the alarm and weather routine
        :param name:
        :param time:
        :param weather_desc:
        :param temp:
        :param temp_feels_like:
        :param temp_max:
        :return:
        """

        return f"Good morning <say-as interpret-as=\"name\" format= \"undefined\">{name}</say-as>. " \
               f"The current time is <say-as interpret-as=\"time\" format=\"undefined\">{time}</say-as>. " \
               f"The weather outside is {weather_desc}. The temperature right now is {temp} degrees " \
               f"and it feels like {temp_feels_like} degrees. " \
               f"Today's max temperature will be about {temp_max} degrees.<break strength=\"strong\" /> " \
               f"What means of transportation do you want to use to get to work?"

    def build_travel_time_announcement(self, origin, destination, duration, travel_mode_announcement):
        """
        The t2s text for the travel time routine
        :param origin:
        :param destination:
        :param duration:
        :param travel_mode_announcement:
        :return:
        """

        return f"The estimated travel time from <lang xml:lang=\"de-DE\">{origin}</lang> " \
               f"to your workplace <lang xml:lang=\"de-DE\">{destination}</lang> " \
               f"{travel_mode_announcement} will be about {duration}."
