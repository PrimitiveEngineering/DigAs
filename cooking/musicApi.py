from requests.auth import HTTPBasicAuth
import requests
import json
import os
from dotenv import load_dotenv, find_dotenv

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


class MusicApi:

    payload = {
        'grant_type': 'client_credentials'
    }
    client_id = ''
    client_secret = ''
    sp = ''

    def __init__(self):
        load_dotenv(find_dotenv())
        self.__base_url = 'https://accounts.spotify.com/api/token'
        self.client_id = os.getenv('SPOTIFY_CLIENT_ID')
        self.client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        self.sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=os.getenv('SPOTIFY_CLIENT_ID'),
                                                                   client_secret=os.getenv('SPOTIFY_CLIENT_SECRET')))



    def fetch_access_token(self):

        response = requests.post(self.__base_url, auth=HTTPBasicAuth(self.client_id, self.client_secret), data=self.payload)
        response_json = json.loads(response.text)
        access_token = response_json['access_token']

        return access_token

    def music_api_request(self):

        response = self.sp.search(q='why do you love me', limit=1, market='DE')

        print(response)

        for idx, item in enumerate(response['tracks']['items']):
            print(idx, item['artists'][0]['name'], " – ", item['name'])

