import requests
import json


class QuoteApi:
    payload = {}
    headers = {}

    def quote_api_request(self):
        """
            Quote API

            Arguments:
            None

            Returns:
            - quote as string
            - author name as string
        """

        url = 'https://api.quotable.io/random'

        response = requests.request("GET", url, headers=self.headers, data=self.payload)
        response_json = json.loads(response.text)
        
        return self.get_content(response_json), self.get_author(response_json)
    
    def get_content(self, json):
        return json['content']

    def get_author(self, json):
        return json['author']
