""" test_textToSpeech
    * all basic-tests for textToSpeech are implemented here
    author:     inf20086@lehre.dhbw-stuttgart.de
    date:       10.03.2023
    version:    0.0.1
    license:    MIT
"""
from unittest import TestCase
from core.textToSpeech import _AzureT2S, _OfflineT2S, Text2SpeechFactory

AT2S = _AzureT2S()
OT2S = _OfflineT2S()
T2SF = Text2SpeechFactory

class TestTextToSpeech(TestCase):

    def test_OT2S_remove_ssml(self):
        CorrectString = "Nobody expects the Spanish Inquisition"
        StringToTest = "Nobody expects the <Indish>Spanish Inquisition"
        self.assertEqual(CorrectString,OT2S.remove_ssml(StringToTest))

    def test_AT2S_build_ssml_headtail(self):
        CorrectString = f"<speak xmlns=\"http://www.w3.org/2001/10/synthesis\" xmlns:mstts=\"http://www.w3.org/2001/mstts\" xmlns:emo=\"http://www.w3.org/2009/10/emotionml\" version=\"1.0\" xml:lang=\"en-US\"><voice name=\"VOICE\"><s /><prosody rate=\"PROSODY\">TEXT</prosody><s /></voice></speak>"
        voice = "VOICE"
        prosody = "PROSODY"
        text = "TEXT"
        self.assertEqual(CorrectString, AT2S.build_ssml_headtail(text,voice,prosody))

    def test_T2SF_new_azure(self):
        self.assertEqual(AT2S, T2SF.__new__(T2SF,"azure"))

    def test_T2SF_new_offline(self):
        self.assertEqual(OT2S, T2SF.__new__(T2SF,"offline"))

    def test_T2SF_new_fail(self):
        self.assertEqual(OT2S, T2SF.__new__(T2SF,"BiggusDickus"))



