import requests
import json
import os
from dotenv import load_dotenv
import time
from datetime import timezone

load_dotenv()

class GoogleMapsApiException(Exception):
    """
    Is raised when a Parameter in the Google Maps API is invalid
    """

#

class GoogleMapsApi:
    """
    Google Maps API

    Arguments:
    - origin            (required)
    - destination       (required)
    - travelMode        (optional; types: driving, driving, transit, walking)
    - arrivalTime       (optional; only available when travelMode is transit;
                        type: datetime(year, month, day, hour, minutes) (all as integer))
    - returnStringOnly  (default: True; if False: return Values for distance and duration
                        as integer in meter and seconds)

    Returns:
    - distance as tts string
    - distance as integer in meter (if returnStringOnly=False)
    - destination as tts string
    - destination as integer in seconds (if returnStringOnly=False)
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

    def googleMapsApiRequest(self, origin, destination, travelMode='driving', arrivalTime=None, returnStringsOnly='True'):

        url = self.parameterValid(travelMode, origin, destination, arrivalTime, self.baseUrl)

        response = requests.request("GET", url, headers=self.headers, data=self.payload)
        responseJson = json.loads(response.text)

        print(response.text)

        if returnStringsOnly:
            return self.getDistance(responseJson), self.getDuration(responseJson)
        else:
            return self.getDistance(responseJson), self.getDistanceValue(responseJson), self.getDuration(responseJson), self.getDurationValue(responseJson)


    def parameterValid(self, travelMode, origin, destination, arrivalTime, url):

        self.travelModeValid(travelMode)
        url += '&mode=' + travelMode

        if travelMode == 'transit' and not arrivalTime is None:
            arrivalTime = int(arrivalTime.replace(tzinfo=timezone.utc).timestamp())
            self.arrivalTimeValid(arrivalTime)
            url += '&arrival_time=' + str(arrivalTime)
        
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
    
    
    def arrivalTimeValid(self, arrivalTime):
        if arrivalTime <= int(time.time()):
            raise GoogleMapsApiException(f'ArrivalTime is prior to the current date')
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
    

    def getDurationValue(self, responseJson):
        durationValue = int(responseJson['rows'][0]['elements'][0]['duration']['value'])
        
        return durationValue


    def getDistanceValue(self, responseJson):
        distanceValue = int(responseJson['rows'][0]['elements'][0]['distance']['value'])

        return distanceValue