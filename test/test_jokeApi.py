""" test_jokeApi
    * all basic-tests for jokeApi are implemented here
    author:     inf20086@lehre.dhbw-stuttgart.de
    date:       24.03.2023
    version:    0.0.1
    license:    MIT
"""
from unittest import TestCase
from unittest.mock import MagicMock

from joke.jokeApi import JokeApi

JA = JokeApi()


class MyTestCase(TestCase):
    def test_jokeApiRequest(self):
        result = JA.jokeApiRequest()
        self.assertIsInstance(result, str)

    def test_getJoke(self):
        correct_string = "Didn’t mean to? You put your sword right through his head."
        json_obj = MagicMock()
        json_obj.__getitem__.return_value = "Didn’t mean to? You put your sword right through his head."

        string_to_test = JA.getJoke(json_obj)

        self.assertEqual(correct_string, string_to_test)
        json_obj.__getitem__.assert_called_once_with('joke')
