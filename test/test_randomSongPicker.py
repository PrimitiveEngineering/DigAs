""" test_randomSongPicker
    * all basic-tests for randomSongPicker are implemented here
    author:     inf20086@lehre.dhbw-stuttgart.de
    date:       16.04.2023
    version:    0.0.1
    license:    MIT
"""

from unittest import TestCase
from cooking.randomSongPicker import RandomSongPicker, ContainsANonString
from unittest.mock import patch

RSP = RandomSongPicker()


class TestRandomSongPicker(TestCase):
    def test_with_all_strings(self):
        artist_list = ["Coldplay", "Radiohead", "The Beatles"]
        with patch('cooking.randomSongPicker.requests.request') as mock_request:
            mock_request.return_value.text = '{"data": [{"title": "Yellow"}, {"title": "Paranoid Android"}, {"title": "Hey Jude"}]}'
            song, artist = RSP.random_song_picker_request(artist_list)
            mock_request.assert_called_once()
            self.assertIn(artist, artist_list)
            self.assertIn(song, ["Yellow", "Paranoid Android", "Hey Jude"])

    def test_with_non_string_entry(self):
        artist_list = ["Coldplay", "Radiohead", 42]
        with self.assertRaises(ContainsANonString):
            song, artist = RSP.random_song_picker_request(artist_list)
