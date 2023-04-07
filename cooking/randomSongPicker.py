import requests
import json
import random


class ContainsANonString(Exception):
    """
    Is raised when an object contains a non string object
    """


class RandomSongPicker:
    """
    Random Song Picker that picks a random song from a preferred artist

    Arguments:
    - list of artists   (required)

    Returns:
    - random song of the chosen artist
    - chosen artist
    """

    payload = {}
    headers = {}

    def __init__(self):
        self.url = 'https://api.deezer.com/search?q=\"'

    def random_song_picker_request(self, artist_list):
        if not self.check_if_list_is_all_type_string(artist_list):
            raise ContainsANonString(f'In the list artist_list is a non string entry')

        artist = self.pick_random_artist(artist_list)
        url = self.url + artist + '\"'
        response = requests.request("GET", url, headers=self.headers, data=self.payload)
        responseJson = json.loads(response.text)
        all_songs = responseJson['data']
        song = self.pick_random_song(all_songs)

        return song['title'], artist

    def check_if_list_is_all_type_string(self, artist_list):
        return all(isinstance(x, str) for x in artist_list)

    def pick_random_artist(self, artist_list):
        rand = random.randint(0, len(artist_list) - 1)
        return artist_list[rand]

    def pick_random_song(self, all_songs):
        rand = random.randint(0, len(all_songs) - 1)
        return all_songs[rand]