import requests
import json


class JokeApi:
    '''
    Joke API

    Arguments:
    None

    Returns:
    - single line joke as string
    '''

    payload = {}
    headers = {}

    def jokeApiRequest(self):

        url = 'https://v2.jokeapi.dev/joke/Any?type=single'

        response = requests.request("GET", url, headers=self.headers, data=self.payload)
        responseJson = json.loads(response.text)

        return self.getJoke(responseJson)
    
    
    def getJoke(self, json):

        return json['joke']