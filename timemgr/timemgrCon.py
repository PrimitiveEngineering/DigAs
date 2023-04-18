from timemgr.calenderAPI import CalenderAPI
from timemgr.time import Time
from core.util import Speech2TextUtil
import schedule
import yaml
import os
from beautiful_date import *


class TimemgrCon:
    __instance = None
    __t2s = None
    __s2t = None

    __calendar = None

    __username = "Debug"
    __reminder_time = 15  # In minutes

    # singleton pattern
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, t2s, s2t, schedule_util):
        """
        Timemanager Service
        :param t2s: Text2Speech Service
        :param s2t: Speech2Text Service
        :param schedule_util: Schedule Utility Service
        """

        self.__t2s = t2s
        self.__s2t = s2t

        self.__calendar = CalenderAPI()

        self.get_config()
        schedule_util.load_config_registrator(self.get_config)
        schedule_util.meeting_guard_socket(self.__calendar.get_events_24h_list)
        self.create_jobs(self.__reminder_time)

    def get_config(self):
        """
        Reading the config file and writing parameters to class attributes
        expected:
            global.username -> string
            time.remindertime -> int
        :return:
        """

        with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config.yaml')), "r") as file:
            yaml_config = yaml.safe_load(file)

        self.__username = yaml_config["global"]["username"]
        self.__reminder_time = yaml_config["time"]["reminder_time"]

    def create_jobs(self, reminder_time):
        events = self.__calendar.get_events_24h()
        for event in events:
            event_start = event.start - reminder_time * minutes
            # print(event_start)
            job_time = Time.change_time_format(event_start.strftime("%Y/%m/%d %H:%M:%S"))
            schedule.every().day.at(job_time).do(self.start_timemanager_routine, event_id=event.event_id). \
                tag("meeting")

    def start_timemanager_routine(self, event_id=None):
        """
        Runs the timemanager routine
        :return: none
        """

        if event_id is None:
            return

        self.__t2s.trigger(
            self.build_timemanager_starting_announcement(
                self.__username,
                self.__reminder_time),
            True)

        user_input, termination_desire = Speech2TextUtil().user_input_func(self.__s2t, self.__t2s)

        if termination_desire:
            self.__t2s.trigger("Terminating", False)
            return

        response_type = self.get_response_type(user_input)
        self.run_user_choice(response_type, self.__calendar.get_event_id(event_id))

        return schedule.CancelJob

    def get_response_type(self, user_input):
        """
        Response type decider
        :param user_input: s2t user input as text
        :return: response_type
        """

        if Speech2TextUtil().contains_word(user_input, ["not", "dont", "don't", "already", "no"]):
            response_type = "no"
        else:
            response_type = "yes"

        return response_type

    def run_user_choice(self, response_type, event):
        """
        Runs the user choice
        :param response_type: The requested choice
        :param event: google calendar event
        """

        if response_type == "no":
            self.__t2s.trigger(
                self.build_no_info_announcement(
                ),
                True)

        else:
            self.__t2s.trigger(
                self.build_more_info_announcement(
                    event.summary,
                    event.location,
                    event.description
                ),
                True)

    def build_timemanager_starting_announcement(self, name, reminder_time):
        """
        The t2s text for starting the timemanager-functionality
        :param name:
        :param reminder_time:
        :return:
        """

        return f"Hey <say-as interpret-as=\"name\" format= \"undefined\">{name}</say-as>. " \
               f"You have an event coming up in {reminder_time} minutes. " \
               f"Would you like me to tell you more?"

    def build_no_info_announcement(self):
        """
        The t2s text for the short announcement
        :return:
        """

        return f"Ok, i hope you have a nice event."

    def build_more_info_announcement(self, event_name, event_location, event_description):
        """
        The t2s text for the elaborate announcement
        :param event_name:
        :param event_location:
        :param event_description:
        :return:
        """

        text = f"The Event is {event_name}."
        if event_location is not None:
            text = text[:-1]
            text += f" and you planned to go to {event_location}."
        if event_description is not None:
            text += f" Your description reads: {event_description}"

        return text
