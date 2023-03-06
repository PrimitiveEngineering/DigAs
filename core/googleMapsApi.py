import requests
import json
import os
from dotenv import load_dotenv
import time

load_dotenv()

class GoogleMapsApiException(Exception):
    """
    Is raised when a Parameter in the Google Maps API is invalid
    """

class GoogleMapsApi:
    """
    Google Maps API

    Arguments:
    - origin (required)
    - destination (required)
    - travelMode (optional: driving, driving, transit, walking)

    Returns:
    - distance as tts string
    - destination as tts string
    """

    baseUrl = 'https://maps.googleapis.com/maps/api/distancematrix/json?key=' + os.getenv('GOOGLE_API_KEY')

    available_travel_modes = [
        'bicycling',
        'driving',
        'transit',
        'walking'
    ]

    duration_dictionary = {
        'hours' : 'stunden',
        'hour'  : 'stunde',
        'mins'  : 'minuten',
        'min'   : 'minute'
    }

    payload = {}
    headers = {}

    def googleMapsApiRequest(self, origin, destination, travelMode='driving'):

        url = self.parameterValid(travelMode, origin, destination, self.baseUrl)

        response = requests.request("GET", url, headers=self.headers, data=self.payload)
        responseJson = json.loads(response.text)

        return self.getDistance(responseJson), self.getDuration(responseJson)

    def parameterValid(self, travelMode, origin, destination, url):

        self.travelModeValid(travelMode)
        url += '&mode=' + travelMode
        
        self.originIsString(origin)
        url += '&origins=' + origin

        self.destinationIsString(destination)
        url += '&destinations=' + destination

        return url
    
    def travelModeValid(self, travelMode):
        if travelMode:
            if travelMode not in self.available_travel_modes:
                raise GoogleMapsApiException(f'travelMode is from no available type (Value: {travelMode})')
        return True
    
    def originIsString(self, origin):
        if not isinstance(origin, str):
            raise GoogleMapsApiException(f'Origin is not a string')
        return True
    
    def destinationIsString(self, destination):
        if not isinstance(destination, str):
            raise GoogleMapsApiException(f'Destination is not a string')
        return True

    def getDuration(self, responseJson):
        duration = responseJson['rows'][0]['elements'][0]['duration']['text']

        for english, german in self.duration_dictionary.items():
            if 'minuten' not in duration:
                duration = duration.replace(english, german)
        
        return duration

    def getDistance(self, responseJson):
        distance = responseJson['rows'][0]['elements'][0]['distance']['text']

        if 'km' in distance:
            distance = distance.replace('km', 'kilometer')
        else:
            distance = distance.replace('m', 'meter')

        return distance
