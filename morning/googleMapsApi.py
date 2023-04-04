import requests
import json
import os
from dotenv import load_dotenv, find_dotenv
import time
from datetime import timezone


class GoogleMapsApiException(Exception):
    """
    Is raised when a Parameter in the Google Maps API is invalid
    """


class GoogleMapsApi:
    """
    Google Maps API for receiving distance and travel time between two locations
    """

    def __init__(self):
        load_dotenv(find_dotenv())
        self.__base_url = 'https://maps.googleapis.com/maps/api/distancematrix/json?key=' + os.getenv('GOOGLE_API_KEY')

    available_travel_modes = [
        'bicycling',
        'driving',
        'transit',
        'walking'
    ]

    duration_dictionary = {
        'hours': 'stunden',
        'hour': 'stunde',
        'mins': 'minuten',
        'min': 'minute'
    }

    payload = {}
    headers = {}

    def google_maps_api_request(self, origin, destination, travel_mode='driving', arrival_time=None,
                                return_strings_only='True'):
        """
        Arguments:
        - origin            (required)
        - destination       (required)
        - travel_mode        (optional; types: driving, driving, transit, walking)
        - arrival_time       (optional; only available when travel_mode is transit;
                            type: datetime(year, month, day, hour, minutes) (all as integer))
        - returnStringOnly  (default: True; if False: return Values for distance and duration
                            as integer in meter and seconds)

        Returns:
        - distance as tts string
        - distance as integer in meter (if returnStringOnly=False)
        - destination as tts string
        - destination as integer in seconds (if returnStringOnly=False)
        """

        url = self.parameter_valid(travel_mode, origin, destination, arrival_time, self.__base_url)

        response = requests.request("GET", url, headers=self.headers, data=self.payload)
        response_json = json.loads(response.text)

        print(response.text)

        if return_strings_only:
            return self.get_distance(response_json), self.get_duration(response_json)
        else:
            return self.get_distance(response_json), self.get_distance_value(response_json), self.get_duration(
                response_json), self.get_duration_value(response_json)

    def parameter_valid(self, travel_mode, origin, destination, arrival_time, url):

        self.travel_mode_valid(travel_mode)
        url += '&mode=' + travel_mode

        if travel_mode == 'transit' and not arrival_time is None:
            arrival_time = int(arrival_time.replace(tzinfo=timezone.utc).timestamp())
            self.arrival_time_valid(arrival_time)
            url += '&arrival_time=' + str(arrival_time)

        self.origin_is_string(origin)
        url += '&origins=' + origin

        self.destination_is_string(destination)
        url += '&destinations=' + destination

        return url

    def travel_mode_valid(self, travel_mode):
        if travel_mode:
            if travel_mode not in self.available_travel_modes:
                raise GoogleMapsApiException(f'travel_mode is from no available type (Value: {travel_mode})')
        return True

    def arrival_time_valid(self, arrival_time):
        if arrival_time <= int(time.time()):
            raise GoogleMapsApiException(f'ArrivalTime is prior to the current date')
        return True

    def origin_is_string(self, origin):
        if not isinstance(origin, str):
            raise GoogleMapsApiException(f'Origin is not a string')
        return True

    def destination_is_string(self, destination):
        if not isinstance(destination, str):
            raise GoogleMapsApiException(f'Destination is not a string')
        return True

    def get_duration(self, response_json):
        duration = response_json['rows'][0]['elements'][0]['duration']['text']

        for english, german in self.duration_dictionary.items():
            if 'minuten' not in duration:
                duration = duration.replace(english, german)

        return duration

    def get_distance(self, response_json):
        distance = response_json['rows'][0]['elements'][0]['distance']['text']

        if 'km' in distance:
            distance = distance.replace('km', 'kilometer')
        else:
            distance = distance.replace('m', 'meter')

        return distance

    def get_duration_value(self, response_json):
        duration_value = int(response_json['rows'][0]['elements'][0]['duration']['value'])

        return duration_value

    def get_distance_value(self, response_json):
        distance_value = int(response_json['rows'][0]['elements'][0]['distance']['value'])

        return distance_value
