from abc import ABC, abstractmethod
import logging
import pyttsx3
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv, find_dotenv
import os
import re


class Text2SpeechAbstract(ABC):
    __instance = None

    # singleton pattern
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @abstractmethod
    def trigger(self, text, ssml=False):
        pass


class OnlineT2SnotAvailable(Exception):
    """
    Exception if some online t2s isn't working as expected
    """

    def __init__(self, message):
        """
        Exception if some online t2s isn't working as expected
        :param message: error message
        """
        logging.error(message)


class _OfflineT2S(Text2SpeechAbstract):
    """
    Offline text to speech functionality. Worse audio quality but it's free.
    """

    def trigger(self, text, ssml):
        """
        Outputs the entered text as audio output.
        :param text: text input
        :param ssml: (optional) Offline t2s doesn't support ssml
        :return: none
        """

        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)  # Change index to change voice
        if ssml:
            text = self.remove_ssml(text)
        engine.say(text)
        engine.runAndWait()

    def remove_ssml(self, text):
        """
        removes ssml properties
        :param text: text with ssml properties
        :return: param text without cut out ssml properties
        """

        # REGEX: search for a substring that starts with < and ends with >.
        #        The [] exclude that no <> are contained per match.
        return re.sub("<[^<>]*>", "", text)


class _AzureT2S(Text2SpeechAbstract):
    """
    Online text to speech functionality. Uses Microsoft Azure speech service. Better audio quality but costs money.

    :attribute speech_key: (private) azure resource key
    :attribute service_region: (private) azure resource region
    :attribute voice: azure voice id
    :attribute prosody: relative speed of speech
    """

    def __init__(self):
        load_dotenv(find_dotenv())
        self.__speech_key = os.getenv('SPEECH_KEY')
        self.__service_region = os.getenv('SERVICE_REGION')
        self.voice = "en-US-JennyMultilingualNeural"
        self.prosody = "-13.00%"

    def trigger(self, text, ssml=False):
        """
        Outputs the entered text as audio output.
        :param text: text input
        :param ssml: (optional) set True if text has ssml properties
        :return:
        """

        speech_config = speechsdk.SpeechConfig(subscription=self.__speech_key, region=self.__service_region)
        # Note: the voice setting will not overwrite the voice element in input SSML.
        speech_config.speech_synthesis_voice_name = self.voice
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

        if ssml:
            result = speech_synthesizer.speak_ssml_async(self.build_ssml_headtail(text, self.voice, self.prosody)).get()
        else:
            result = speech_synthesizer.speak_text_async(text).get()

        # Check result
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            # print("Speech synthesized for text [{}]".format(text))
            pass
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            # print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                # print("Error details: {}".format(cancellation_details.error_details))
                pass

            # Throw exception
            raise OnlineT2SnotAvailable("AzureT2S failed")

    def build_ssml_headtail(self, text, voice, prosody):
        """
        adds the start and end ssml syntax to the text
        :param text: the message input for text to speech
        :param voice: Azure voice ID
        :param prosody: Azure voice relative speed
        :return: text with start and end ssml properties
        """

        return f"<speak xmlns=\"http://www.w3.org/2001/10/synthesis\" xmlns:mstts=\"http://www.w3.org/2001/mstts\" xmlns:emo=\"http://www.w3.org/2009/10/emotionml\" version=\"1.0\" xml:lang=\"en-US\"><voice name=\"{voice}\"><s /><prosody rate=\"{prosody}\">{text}</prosody><s /></voice></speak>"


class Text2SpeechFactory(object):
    """
    The Factory class for creating the special T2S interfaces.
    """

    def __new__(cls, mode):
        av_mode = {
            "offline": _OfflineT2S(),
            "azure": _AzureT2S(),
        }
        mode = str.lower(mode)
        if mode in av_mode.keys():
            return av_mode.get(mode)
        else:
            logging.error(f"Text to speech mode {mode} not found. Falling back to OfflineT2S.")
            return av_mode.get("offline")


class Text2SpeechService:
    """
    This class should be used mainly for the text to speech functionality.
    It is the combination of a singleton and strategy pattern
    """

    __instance = None
    __t2s_abstract = None

    # singleton pattern
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, mode):
        self.change_mode(mode)

    def change_mode(self, mode):
        self.__t2s_abstract = Text2SpeechFactory(mode)

    def trigger(self, text, ssml):
        offline_t2s = Text2SpeechFactory("offline")
        try:
            # DEBUG
            cleared_text = text
            if ssml:
                cleared_text = offline_t2s.remove_ssml(text)
            print(cleared_text)
            # DEBUG END

            self.__t2s_abstract.trigger(text, ssml)
        except OnlineT2SnotAvailable:
            offline_t2s_t2s = Text2SpeechFactory("offline")
            if ssml:
                text = offline_t2s.remove_ssml(text)
            offline_t2s.trigger(text, False)
