import requests
from dotenv import load_dotenv
import os


class OpenWeatherCityNotFound(Exception):
    pass


class OpenWeather:
    """
    The weather function class
    """

    __api_key = None
    __base_url = "http://api.openweathermap.org/data/2.5/weather?"

    def __init__(self):
        load_dotenv()
        self.__api_key = os.getenv('OPENWEATHER_API_KEY')

    def get_weather(self, city):
        """
        Return today's weather
        :param city: Name of the city
        :return: dictionary: description, temp, feels_like, max_temp
        """

        weather_response = self.__api_call(city)
        if weather_response["cod"] != "404":
            weather_response_main = weather_response["main"]
            weather_data = {
                "description": weather_response["weather"][0]["description"],
                "temp": self.kelvin_to_celsius(weather_response_main["temp"]),
                "feels_like": self.kelvin_to_celsius(weather_response_main["feels_like"]),
                "max_temp": self.kelvin_to_celsius(weather_response_main["temp_max"])
            }
            return weather_data
        else:
            raise OpenWeatherCityNotFound(f"City: {city} not found")

    def __api_call(self, city):
        """
        Makes the api request with url, api_key and the city name
        :param city:
        :return: json response
        """

        complete_url = self.__base_url + "appid=" + self.__api_key + "&q=" + city
        response = requests.get(complete_url)
        return response.json()

    def kelvin_to_celsius(self, kelvin):
        """
        Changes the kelvin values to celsius and rounds them at the first decimal place
        :param kelvin: kelvin value
        :return: celsius value
        """

        kelvin = float(kelvin)
        return round(kelvin - 273.15, 1)
