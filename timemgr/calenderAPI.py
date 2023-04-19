from gcsa.event import Event
from gcsa.google_calendar import GoogleCalendar
import os

from beautiful_date import *


class CalenderAPI:
    __instance = None

    # singleton pattern
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        self.calendar = GoogleCalendar('primitiveengineeringdhbw@gmail.com',
                                       credentials_path=os.path.abspath(os.path.join(os.path.dirname(__file__), '..',
                                                                                     'google_secret.json')))

    def print_events(self):
        """
        prints events in the calendar with the default function
        :return:
        """
        for event in self.calendar:
            print(event.event_id)
            print(event)


    def create_event(self, name, start, end):
        """
        creates a new event in the calendar
        :param name:
        :param start:
        :param end:
        :return:
        """
        event = Event(name, start, end)
        self.calendar.add_event(event)

    def get_event_id(self, event_id):
        """
        returns an event specified by its id
        :param event_id:
        :return: event
        """
        return self.calendar.get_event(event_id)

    def get_events_24h(self):
        """
        returns a list of events in the next 24 hours
        :return: events
        """
        return list(self.calendar.get_events(D.now(), D.now() + 1 * days, order_by='startTime', single_events=True))

    def get_events_24h_list(self):
        """
        returns a list of tupels containing (startime, endtime) from the events in the next 24 hours
        :return: events
        """
        times = []
        for event in self.calendar.get_events(D.now(), D.now() + 1 * days, order_by='startTime', single_events=True):
            times.append((event.start, event.end))
        return times

    def get_events(self, start, end):
        """
        returns a list of events in the specified timeframe
        :param start:
        :param end:
        :return: events
        """
        return list(self.calendar.get_events(start, end, order_by='startTime', single_events=True))

    def get_events_now(self):
        """
        returns a list of events happening right now
        :return: events
        """
        return list(self.calendar.get_events(D.now(), D.now() + 1 * minutes, order_by='startTime', single_events=True))

    def is_event_now(self):
        """
        returns True or False depending on if there is an event happening right now
        :return: bool
        """
        return len(list(
            self.calendar.get_events(D.now(), D.now() + 1 * minutes, order_by='startTime', single_events=True))) > 0
