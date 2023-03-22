""" test_speechToText
    * all basic-tests for speechToText are implemented here
    author:     inf20086@lehre.dhbw-stuttgart.de
    date:       22.03.2023
    version:    0.0.1
    license:    MIT
"""
from unittest import TestCase

from core.speechToText import _GoogleS2T,Speech2TextFactory,_OfflineS2T


GS2T = _GoogleS2T()
OS2T = _OfflineS2T()
S2TF = Speech2TextFactory

class TestSpeechToText(TestCase):
    def test_T2SF_new_offline(self):
        self.assertEqual(OS2T, S2TF.__new__(S2TF, "offline"))

    def test_T2SF_new_google(self):
        self.assertEqual(GS2T, S2TF.__new__(S2TF, "google"))


