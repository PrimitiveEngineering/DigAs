import os
from dotenv import load_dotenv, find_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth


class MusicApi:
    """
    Music API that useses Spotify API to search and play tracks to local devices
    """

    scope = 'user-modify-playback-state'
    redirect_uri = 'http://example.com'

    def __init__(self):
        load_dotenv(find_dotenv())
        self.client_id = os.getenv('SPOTIFY_CLIENT_ID')
        self.client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=self.scope,
                                                            redirect_uri=self.redirect_uri,
                                                            client_id=os.getenv('SPOTIFY_CLIENT_ID'),
                                                            client_secret=os.getenv('SPOTIFY_CLIENT_SECRET')))

    def play_requested_song(self, song_title, artist=None):
        """
        Searches for requested song and plays it on the local Spotify application

        Arguments:
        - song_title    (required)
        - artist        (optional)

        Returns:
        - None
        """
        requested_song = self.build_requested_song_string(song_title, artist)
        song_uri = self.search_song_uri(requested_song)
        self.start_song(song_uri)

    def search_song_uri(self, requested_song):
        response = self.sp.search(q=requested_song, limit=1, offset=0, type='track', market='DE')
        song_uri = response['tracks']['items'][0]['uri']

        return song_uri

    def build_requested_song_string(self, song_title, artist):
        requested_song = song_title
        if artist is not None:
            requested_song += ' artist:' + artist

        return requested_song

    def start_song(self, song_uri):
        self.sp.start_playback(uris=[str(song_uri)])
