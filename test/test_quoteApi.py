""" test_quoteApi
    * all basic-tests for quote-API are implemented here
    author:     inf20086@lehre.dhbw-stuttgart.de
    date:       04.04.2023
    version:    0.0.1
    license:    MIT
"""
import unittest
from joke.quoteApi import QuoteApi

QAPI = QuoteApi()


class TestQuoteApi(unittest.TestCase):
    def test_quote_api_request_str_one(self):
        self.assertIsInstance(QAPI.quote_api_request()[0], str)

    def test_quote_api_request_str_two(self):
        self.assertIsInstance(QAPI.quote_api_request()[1], str)

    def test_get_content(self):
        json_data = {"_id": "no", "content": "yes", "author": "no", "tags": ["no", "no"], "authorSlug": "no",
                     "length": 2, "dateAdded": "2000-10-01", "dateModified": "2022-07-04"}
        correct_string = "yes"
        self.assertEqual(correct_string, QAPI.get_content(json_data))

    def test_get_author(self):
        json_data = {"_id": "no", "content": "no", "author": "yes", "tags": ["no", "no"], "authorSlug": "no",
                     "length": 2, "dateAdded": "2000-10-01", "dateModified": "2022-07-04"}
        correct_string = "yes"
        self.assertEqual(correct_string, QAPI.get_author(json_data))
