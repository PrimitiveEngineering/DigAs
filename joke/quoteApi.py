import requests
import json


class QuoteApi:
    '''
    Quote API

    Arguments:
    None

    Returns:
    - quote as string
    - author name as string
    '''

    payload = {}
    headers = {}

    def quoteApiRequest(self):

        url = 'https://api.quotable.io/random'

        response = requests.request("GET", url, headers=self.headers, data=self.payload)
        responseJson = json.loads(response.text)
        
        return self.getContent(responseJson), self.getAuthor(responseJson)
    
    
    def getContent(self, json):

        return json['content']
    

    def getAuthor(self, json):

        return json['author']
    

quote = QuoteApi()

print(quote.quoteApiRequest())