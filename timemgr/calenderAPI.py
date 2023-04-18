from gcsa.event import Event
from gcsa.google_calendar import GoogleCalendar
from gcsa.recurrence import Recurrence, DAILY, SU, SA

from beautiful_date import *

class calenderAPI:

    def __init__(self):
        self.calendar = GoogleCalendar('primitiveengineeringdhbw@gmail.com',
                                  credentials_path='./client_secret_1007758535570-mbta1dpade6r2sdqs2lhlkcgft2qamma.apps.googleusercontent.com.json')

    def print_events(self):
        for event in self.calendar:
            print(event)

    def print_events(self, start, end):
        for event in self.calendar.get_events(start, end, order_by='startTime'):
            print(event)

    def create_event(self, name, start, end):
        event = Event(name, start, end)
        self.calendar.add_event(event)

    def get_events(self, start, end):
        return self.calendar.get_events(start, end, order_by='startTime')

    def get_events_now(self):
        return self.calendar.get_events(D.now(), order_by='startTime')