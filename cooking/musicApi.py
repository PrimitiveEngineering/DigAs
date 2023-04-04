from requests.auth import HTTPBasicAuth
import requests
import json
import os
from dotenv import load_dotenv, find_dotenv

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth


class MusicApi:

    payload = {
        'grant_type': 'client_credentials'
    }

    def __init__(self):
        load_dotenv(find_dotenv())
        os.environ['SPOTIPY_CLIENT_ID'] = os.getenv('SPOTIFY_CLIENT_ID')
        os.environ['SPOTIPY_CLIENT_SECRET'] = os.getenv('SPOTIFY_CLIENT_SECRET')
        os.environ['SPOTIPY_REDIRECT_URI'] = 'google.com'
        self.__token_url = 'https://accounts.spotify.com/api/token'
        self.__search_url = 'https://api.spotify.com/v1/search'
        self.__play_url = 'https://api.spotify.com/v1/me/player/play'
        self.client_id = os.getenv('SPOTIFY_CLIENT_ID')
        self.client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth())



    def play_requested_song(self, song_title):

        access_token = self.fetch_access_token()
        url = self.__search_url + '?type=track&market=DE&limit=1&q=' + str(song_title)
        response = requests.request("GET", url, headers={'Authorization': 'Bearer ' + access_token}, data={})
        response_json = json.loads(response.text)

        song_uri = response_json['tracks']['items'][0]['album']['uri']

        print(song_uri)
        print(access_token)
        self.start_song(song_uri, access_token)

    def start_song(self, song_uri, access_token):

        self.sp.start_playback(device_id='23ad0f9f001a35de73dc515625fdb157e2fca6bf', uris=[str(song_uri)])
        #url = self.__play_url + '?device_id=23ad0f9f001a35de73dc515625fdb157e2fca6bf'
        #response = requests.put(url, headers={'Authorization': 'Bearer ' + access_token}, data={"uris": [str(song_uri)]})
        #print(response.text)

    def fetch_access_token(self):

        response = requests.post(self.__token_url, auth=HTTPBasicAuth(self.client_id, self.client_secret), data=self.payload)
        response_json = json.loads(response.text)
        access_token = response_json['access_token']

        return access_token







    def music_api_request(self):

        response = self.sp.search(q='why do you love me', limit=1, market='DE')

        print(response)

        for idx, item in enumerate(response['tracks']['items']):
            print(idx, item['artists'][0]['name'], " – ", item['name'])



a = MusicApi()

a.play_requested_song('The fox')