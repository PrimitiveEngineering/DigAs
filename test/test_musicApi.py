""" test_musicApi
    * all basic-tests for musicApi are implemented here
    author:     inf20086@lehre.dhbw-stuttgart.de
    date:       16.03.2023
    version:    0.0.1
    license:    MIT
"""
from unittest import TestCase
from cooking.musicApi import MusicApi

MA = MusicApi()


class TestMusicApi(TestCase):

    def test_play_requested_song(self):
        self.assertEqual(None, MA.play_requested_song("Days of Blues"))

    def test_search_song_uri(self):
        result_string = "spotify:track:6fLnMSHygIfRzdfPlplrCc"
        self.assertEqual(result_string, MA.search_song_uri("Days of Blues"))

    def test_build_requested_song_string(self):
        result_string = "TITEL artist:ARTIST"
        self.assertEqual(result_string, MA.build_requested_song_string("TITEL", "ARTIST"))

    def test_start_song(self):
        self.assertEqual(None, MA.start_song("spotify:track:6fLnMSHygIfRzdfPlplrCc"))
