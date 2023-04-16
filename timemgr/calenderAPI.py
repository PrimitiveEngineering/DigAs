from gcsa.event import Event
from gcsa.google_calendar import GoogleCalendar
from gcsa.recurrence import Recurrence, DAILY, SU, SA

from beautiful_date import Jan, Apr


calendar = GoogleCalendar('primitiveengineeringdhbw@gmail.com',credentials_path='./client_secret_1007758535570-mbta1dpade6r2sdqs2lhlkcgft2qamma.apps.googleusercontent.com.json')
event = Event(
    'Breakfast',
    start=(1 / Jan / 2023)[9:00],
    recurrence=[
        Recurrence.rule(freq=DAILY),
        Recurrence.exclude_rule(by_week_day=[SU, SA]),
        Recurrence.exclude_times([
            (19 / Apr / 2023)[9:00],
            (22 / Apr / 2023)[9:00]
        ])
    ],
    minutes_before_email_reminder=50
)

calendar.add_event(event)

for event in calendar:
    print(event)