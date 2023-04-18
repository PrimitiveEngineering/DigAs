import os
import yaml

import schedule
from datetime import datetime, timedelta


class ScheduleJobUtil:
    @staticmethod
    def run_job_once(function):
        function()
        return schedule.CancelJob


class ScheduleUtil:
    __instance = None
    guard_min = 5
    config_functions = []
    calender_function = None

    # singleton pattern
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        self.config_functions.append(self.get_config())
        schedule.every().minute.do(self.meeting_guard).tag("utility")
        schedule.every(2).minutes.do(self.load_config()).tag("utility")

    def get_config(self):
        """
        Reading the config file and writing parameters to class attributes
        expected:
            schedule.guard_min
        :return:
        """
        with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config.yaml')), "r") as file:
            yaml_config = yaml.safe_load(file)
            self.guard_min = yaml_config["schedule"]["guard_min"]

    def load_config_registrator(self, config_function):
        """
        Register the passed function for continuous config update
        :param config_function: (function)
        :return:
        """
        if config_function not in self.config_functions:
            self.config_functions.append(config_function)

    def load_config(self):
        """
        The schedule job function to call out all registered config_function
        :return:
        """
        for config_function in self.config_functions:
            config_function()

    def meeting_guard_socket(self, calender_function):
        """
        Registrator function for the calenderApiService function
        :param calender_function:
        :return:
        """
        self.calender_function = calender_function

    def meeting_guard(self):
        """
        Iterates over all schedules jobs and if a meeting overlaps with a job it gets moved
        :return:
        """
        if self.calender_function is None:
            return

        meetings = self.calender_function()

        self.check_jobs(schedule.get_jobs(), meetings, self.guard_min)

    def check_jobs(self, jobs, meetings, minute_shifter):
        """
        Checks meeting collision for all jobs.
        :param jobs: schedule.get_jobs()
        :param meetings: meetings from calenderApiService
        :param minute_shifter: amount of minutes shifted after the meeting
        :return: None
        """

        for job in jobs:
            # Jobs with these tags are ignored
            tags_ignore = ["meeting", "utility"]
            if any(tag in jobs.tags for tag in tags_ignore):
                break

            while self.check_meeting_overlap(job, meetings, minute_shifter):
                pass  # do again

    def check_meeting_overlap(self, job, meetings, minute_shifter):
        """
        Checks if one job overlaps with a meeting.
        :param job: one job of schedule.get_jobs()
        :param meetings: meetings from calenderApiService
        :param minute_shifter: amount of minutes shifted after the meeting
        :return: (boolean) if job collides with meeting
        """

        meeting_overlap = False
        for meeting in meetings:
            if meeting[0] < job.next_run < meeting[1]:
                job.next_run = meeting[1] + timedelta(minutes=minute_shifter)
                meeting_overlap = True

        return meeting_overlap
