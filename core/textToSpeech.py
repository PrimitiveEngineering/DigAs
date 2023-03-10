from abc import ABC, abstractmethod
import pyttsx3
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
import os
import re


class Text2SpeechInterface(ABC):
    @abstractmethod
    def trigger(self, text, ssml=False):
        pass


class OfflineT2S(Text2SpeechInterface):
    """
    Offline text to speech functionality. Worse audio quality but it's free.
    """

    def trigger(self, text, ssml=False):
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
        engine.say(text)
        engine.runAndWait()


class AzureT2S(Text2SpeechInterface):
    """
    Online text to speech functionality. Uses Microsoft Azure speech service. Better audio quality but costs money.

    :attribute speech_key: azure resource key
    :attribute service_region: azure resource region
    :attribute voice: azure voice id
    :attribute prosody: relative speed of speech
    """

    def __init__(self):
        load_dotenv()
        self.speech_key = os.getenv('SPEECH_KEY')
        self.service_region = os.getenv('SERVICE_REGION')
        self.voice = "en-US-JennyMultilingualNeural"
        self.prosody = "-13.00%"

    def trigger(self, text, ssml=False):
        """
        Outputs the entered text as audio output.
        :param text: text input
        :param ssml: (optional) set True if text has ssml properties
        :return:
        """

        speech_config = speechsdk.SpeechConfig(subscription=self.speech_key, region=self.service_region)
        # Note: the voice setting will not overwrite the voice element in input SSML.
        speech_config.speech_synthesis_voice_name = self.voice
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

        if ssml:
            result = speech_synthesizer.speak_ssml_async(self.build_ssml_headtail(text, self.voice, self.prosody)).get()
        else:
            result = speech_synthesizer.speak_text_async(text).get()

        # Check result
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Speech synthesized for text [{}]".format(text))
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))

            # Exception handling: Using Offline t2s
            if ssml:
                text = self.remove_ssml(text)
            OfflineT2S().trigger(text)

    def build_ssml_headtail(self, text, voice, prosody):
        """
        adds the start and end ssml syntax to the text
        :param text: the message input for text to speech
        :param voice: Azure voice ID
        :param prosody: Azure voice relative speed
        :return: text with start and end ssml properties
        """
        return f"<speak xmlns=\"http://www.w3.org/2001/10/synthesis\" xmlns:mstts=\"http://www.w3.org/2001/mstts\" xmlns:emo=\"http://www.w3.org/2009/10/emotionml\" version=\"1.0\" xml:lang=\"en-US\"><voice name=\"{voice}\"><s /><prosody rate=\"{prosody}\">{text}</prosody><s /></voice></speak>"

    def remove_ssml(self, text):
        """
        removes ssml properties
        :param text: text with ssml properties
        :return: param text without cut out ssml properties
        """
        # REGEX: search for a substring that starts with < and ends with >.
        #        The [] exclude that no <> are contained per match.
        return re.sub("<[^<>]*>", "", text)
