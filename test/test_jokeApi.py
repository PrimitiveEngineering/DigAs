*all
basic - tests
for joke - API are implemented here
author: inf20086 @ lehre.dhbw - stuttgart.de
date: 04.04
.2023
version: 0.0
.1
license: MIT

import unittest
import json
from unittest.mock import patch, Mock
from joke.jokeApi import JokeApi

JA = JokeApi()


class TestJokeApi(unittest.TestCase):
    def test_get_joke(self):
        json_data = {"category": "Programming", "type": "single",
                     "joke": "Excuse me. Are you the Judean People’s Front? - F*** off! ‘Judean People’s Front’?. We’re the People’s Front of Judea!",
                     }
        correct_string = "Excuse me. Are you the Judean People’s Front? - F*** off! ‘Judean People’s Front’?. We’re the People’s Front of Judea!"
        self.assertEqual(correct_string, JA.get_joke(json_data))

    def test_get_blacklist_string(self):
        correct_string = "&blacklistFlags=religious,sexist"
        self.assertEqual(correct_string, JA.get_blacklist_string(["religious", "sexist"]))

    def test_joke_api_request_type(self):
        self.assertIsInstance(JA.joke_api_request(), str)

    def test_joke_api_request_content(self):
        expected_api_result = {
            'joke': 'Excuse me. Are you the Judean People’s Front? - F*** off! ‘Judean People’s Front’?. We’re the People’s Front of Judea!'}

        mock_response = Mock()
        mock_response.text = json.dumps(expected_api_result)

        with patch('requests.request') as mock_request:
            mock_request.return_value = mock_response

            result = JA.joke_api_request()

            mock_request.assert_called_once_with('GET', 'https://v2.jokeapi.dev/joke/Any?type=single', headers={},
                                                 data={})

            self.assertEqual(result, expected_api_result['joke'])
