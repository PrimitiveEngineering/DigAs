import requests
import json


class QuoteApi:
    payload = {}
    headers = {}

    def quoteApiRequest(self):
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
        responseJson = json.loads(response.text)

        return self.getContent(responseJson), self.getAuthor(responseJson)

    def getContent(self, json):
        return json['content']

    def getAuthor(self, json):
        return json['author']