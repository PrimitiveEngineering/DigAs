import requests
import json

class JokeApiBlacklistOptionNotFound(Exception):
    """
    Is raised when a blacklist option is not found
    """

class JokeApi:

    blacklist_options = [
        'nsfw',
        'religious',
        'political',
        'racist',
        'sexist',
        'explicit'
    ]

    payload = {}
    headers = {}

    def jokeApiRequest(self, blacklist=None):
        """
            Joke API

            Arguments:
            - list of blacklist flags   (optional; flags: nsfw, religious, political, racist, sexist, explicit)

            Returns:
            - single line joke as string
        """

        url = 'https://v2.jokeapi.dev/joke/Any?type=single'

        blacklistString = self.getBlacklistString(blacklist)

        url += blacklistString

        response = requests.request("GET", url, headers=self.headers, data=self.payload)

        responseJson = json.loads(response.text)

        return self.getJoke(responseJson)
    

    def getBlacklistString(self, blacklist):

        if blacklist is None:
            return ''

        blacklistString = '&blacklistFlags='

        for bl in blacklist:
            if bl not in self.blacklist_options:
                raise JokeApiBlacklistOptionNotFound(f'Blacklist option {bl} not an available option')

        blacklistString += ','.join(blacklist)

        return blacklistString


    def getJoke(self, json):

        jokeRaw = json['joke']
        joke = jokeRaw.replace('\n', '')

        return joke
