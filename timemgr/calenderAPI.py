from gcsa.event import Event
from gcsa.google_calendar import GoogleCalendar

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
                                       credentials_path='./google_secret.json')

    def print_events(self):
        for event in self.calendar:
            print(event.event_id)
            print(event)

    # def print_events(self, start, end):
    #     for event in self.calendar.get_events(start, end, order_by='startTime'):
    #         print(event)

    def create_event(self, name, start, end):
        event = Event(name, start, end)
        self.calendar.add_event(event)

    def get_event_id(self, event_id):
        return self.calendar.get_event(event_id)

    def get_events_24h(self):
        return list(self.calendar.get_events(D.now(), D.now() + 1 * days, order_by='startTime', single_events=True))

    def get_events_24h_list(self):
        times = []
        for event in self.calendar.get_events(D.now(), D.now() + 1 * days, order_by='startTime', single_events=True):
            times.append((event.start, event.end))
        return times

    def get_events(self, start, end):
        return list(self.calendar.get_events(start, end, order_by='startTime', single_events=True))

    def get_events_now(self):
        return list(self.calendar.get_events(D.now(), D.now() + 1 * minutes, order_by='startTime', single_events=True))

    def is_event_now(self):
        return len(list(
            self.calendar.get_events(D.now(), D.now() + 1 * minutes, order_by='startTime', single_events=True))) > 0
