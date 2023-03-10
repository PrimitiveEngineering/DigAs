""" test_textToSpeech
    * all basic-tests for textToSpeech are implemented here
    author:     inf20086@lehre.dhbw-stuttgart.de
    date:       10.03.2023
    version:    0.0.1
    license:    MIT
"""
from unittest import TestCase
from core.textToSpeech import AzureT2S

AT2S = AzureT2S()

class TestTextToSpeech(TestCase):
    def test_build_ssml_headtail(self):
        voice = "VOICE"
        prosody = "PROSODY"
        text = "TEXT"
        CorrectString = f"<speak xmlns=\"http://www.w3.org/2001/10/synthesis\" xmlns:mstts=\"http://www.w3.org/2001/mstts\" xmlns:emo=\"http://www.w3.org/2009/10/emotionml\" version=\"1.0\" xml:lang=\"en-US\"><voice name=\"VOICE\"><s /><prosody rate=\"PROSODY\">TEXT</prosody><s /></voice></speak>"
        self.assertEqual(CorrectString,AT2S.build_ssml_headtail(text,voice,prosody))

    def test_remove_ssml(self):
        CorrectString = "Nobody expects the Spanish Inquisition"
        StringToTest = "Nobody expects the <Indish>Spanish Inquisition"
        self.assertEqual(CorrectString,AT2S.remove_ssml(StringToTest))
