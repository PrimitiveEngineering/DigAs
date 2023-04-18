import os
import yaml

import schedule
from datetime import datetime, timedelta


class ScheduleUtil:
    __instance = None
    meeting_shift_min = 5
    job_shift_min = 2
    config_functions = []
    calender_function = None

    # singleton pattern
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        self.get_config()
        self.config_functions.append(self.get_config)
        schedule.every().minute.do(self.meeting_guard).tag("utility")
        schedule.every().minute.do(self.load_config).tag("utility")

    def get_config(self):
        """
        Reading the config file and writing parameters to class attributes
        expected:
            schedule.guard_min
        :return:
        """
        with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config.yaml')), "r") as file:
            yaml_config = yaml.safe_load(file)
            self.meeting_shift_min = yaml_config["schedule"]["meeting_shift_min"]
            self.meeting_shift_min = yaml_config["schedule"]["job_shift_min"]

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

        meetings = self.clean_timezones(self.calender_function())

        self.check_jobs_meeting(schedule.get_jobs(), meetings, self.meeting_shift_min)
        self.check_jobs(schedule.get_jobs(), self.job_shift_min)

    def clean_timezones(self, meetings):
        formatted_meetings = []
        for meeting in meetings:
            formatted_meet_times = []
            for meet_time in meeting:
                formatted_meet_times.append(meet_time.replace(tzinfo=None))
            formatted_meetings.append(formatted_meet_times)

        return formatted_meetings

    def check_jobs_meeting(self, jobs, meetings, meeting_shift_min):
        """
        Checks meeting collision for all jobs.
        :param jobs: schedule.get_jobs()
        :param meetings: meetings from calenderApiService
        :param meeting_shift_min: amount of minutes shifted after the meeting
        :return: None
        """

        for job in jobs:
            # Jobs with these tags are ignored
            tags_ignore = ["meeting", "utility"]
            if any(tag in job.tags for tag in tags_ignore):
                continue

            while self.check_meeting_overlap(job, meetings, meeting_shift_min):
                pass  # do again

    def check_meeting_overlap(self, job, meetings, meeting_shift_min):
        """
        Checks if one job overlaps with a meeting.
        :param job: one job of schedule.get_jobs()
        :param meetings: meetings from calenderApiService
        :param meeting_shift_min: amount of minutes shifted after the meeting
        :return: (boolean) if job collides with meeting
        """

        meeting_overlap = False
        for meeting in meetings:
            if meeting[0] <= job.next_run <= meeting[1]:
                job.next_run = meeting[1] + timedelta(minutes=meeting_shift_min)
                meeting_overlap = True

        return meeting_overlap

    def check_jobs(self, jobs, job_shift_min):
        # Format job time
        for job in jobs:
            # Hop over utility jobs
            if "utility" in job.tags:
                continue
            job.next_run = job.next_run.replace(second=0, microsecond=0)

        # create a job list without utility jobs
        jobs_without_utility = jobs.copy()
        for job in jobs:
            if "utility" in job.tags:
                jobs_without_utility.remove(job)

        # Check jobs from job list
        for job in jobs:
            # Hop over utility jobs
            if "utility" in job.tags:
                continue

            while self.check_job_overlap(job, jobs_without_utility, job_shift_min):
                pass

    def check_job_overlap(self, current_job, jobs_without_utility, job_shift_min):
        job_overlap = False
        for other_job in jobs_without_utility:
            if current_job == other_job:
                continue

            if current_job.next_run == other_job.next_run:
                current_job.next_run = current_job.next_run + timedelta(minutes=job_shift_min)
                job_overlap = True

        return job_overlap

    def print_job(self):
        jobs = schedule.get_jobs()
        for job in jobs:
            print(job.next_run)
