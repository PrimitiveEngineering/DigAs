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

    def joke_api_request(self, blacklist=None):
        """
            Joke API

            Arguments:
            - list of blacklist flags   (optional; flags: nsfw, religious, political, racist, sexist, explicit)

            Returns:
            - single line joke as string
        """

        url = 'https://v2.jokeapi.dev/joke/Any?type=single'

        blacklist_string = self.get_blacklist_string(blacklist)

        url += blacklist_string

        response = requests.request("GET", url, headers=self.headers, data=self.payload)

        response_json = json.loads(response.text)

        return self.get_joke(response_json)

    def get_blacklist_string(self, blacklist):

        if blacklist is None:
            return ''

        blacklist_string = '&blacklistFlags='

        for bl in blacklist:
            if bl not in self.blacklist_options:
                raise JokeApiBlacklistOptionNotFound(f'Blacklist option {bl} not an available option')

        blacklist_string += ','.join(blacklist)

        return blacklist_string

    def get_joke(self, json):

        joke_raw = json['joke']
        joke = joke_raw.replace('\n', '')

        return joke
