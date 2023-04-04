from weatherApi import OpenWeather
from googleMapsApi import GoogleMapsApi
from core.util import Speech2TextUtil


class MorningCon:
    mock_name = "Richard"
    mock_time = "10:00"
    mock_city = "Stuttgart"
    mock_origin = "Gropiusplatz 9 Stuttgart"
    mock_meeting_place = "DHBW Fakultät Technik Stuttgart"

    def __init__(self, t2s, s2t):
        self.t2s = t2s
        self.s2t = s2t

    def start_morning_routine(self):
        weather = OpenWeather().get_weather(self.mock_city)

        self.t2s.trigger(
            self.build_weather_announcement(
                self.mock_name,
                self.mock_time,
                weather["description"],
                weather["temp"],
                weather["feels_like"],
                weather["max_temp"]),
            True)

        user_input, termination_desire = Speech2TextUtil().user_input_func(self.s2t, self.t2s)

        if termination_desire:
            self.t2s.trigger("Terminating", False)
            return

        travel_mode = None
        travel_mode_announcement = None
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

        duration = GoogleMapsApi().google_maps_api_request(
            self.mock_origin,
            self.mock_meeting_place,
            travel_mode,
            None,
            True)[1]

        self.t2s.trigger(
            self.build_travel_time_announcement(
                self.mock_origin,
                self.mock_meeting_place,
                duration,
                travel_mode_announcement),
            True)

    def build_weather_announcement(self, name, time, weather_desc, temp, temp_feels_like, temp_max):
        return f"Good morning <say-as interpret-as=\"name\" format= \"undefined\">{name}</say-as>. " \
               f"The current time is <say-as interpret-as=\"time\" format=\"undefined\">{time}</say-as>. " \
               f"The weather outside is {weather_desc}. The temperature right now is {temp} degrees " \
               f"and it feels like {temp_feels_like} degrees. " \
               f"Today's max temperature will be about {temp_max} degrees.<break strength=\"strong\" /> " \
               f"What means of transportation do you want to use to get to work?"

    def build_travel_time_announcement(self, origin, destination, duration, travel_mode_announcement):
        return f"The estimated travel time from <lang xml:lang=\"de-DE\">{origin}</lang> " \
               f"to your workplace <lang xml:lang=\"de-DE\">{destination}</lang> " \
               f"{travel_mode_announcement} will be about {duration}."
