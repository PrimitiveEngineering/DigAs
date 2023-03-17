from abc import ABC, abstractmethod
import logging
import speech_recognition as sr


class Speech2TextInterface(ABC):
    __instance = None

    # singleton pattern
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @abstractmethod
    def trigger(self):
        pass


class _OfflineS2T(Speech2TextInterface):
    """
    Offline Speech to Text functionality. Worse audio recognition but it's always available.
    """

    def trigger(self):
        """
        Outputs the entered audio as text.
        :return: understood text
        """

        # obtain audio from the microphone
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source)

        # recognize speech using Sphinx
        print("Sphinx:")
        try:
            print("\"" + r.recognize_sphinx(audio) + "\"")
        except sr.UnknownValueError:
            print("Sphinx could not understand audio")
        except sr.RequestError as e:
            print("Sphinx error; {0}".format(e))

class _GoogleS2T(Speech2TextInterface):
    """
    Offline Text to Speech functionality. Better audio recognition but it needs an internet connection.
    """

    def trigger(self):
        """
        Outputs the entered audio as text.
        :return: understood text
        """

        # obtain audio from the microphone
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source)

        # recognize speech using Google Speech Recognition
        print("Google:")
        try:
            output = r.recognize_google(audio)
            return output
        except sr.UnknownValueError:
            return "Google Speech Recognition could not understand audio"
        except sr.RequestError as e:
            return ("Could not request results from Google Speech Recognition service; {0}".format(e))



class Speech2TextFactory(object):
    """
    The Factory class for creating the special S2T interfaces.
    """

    def __new__(cls, mode):
        av_mode = {
            "offline": _OfflineS2T(),
            "google": _GoogleS2T(),
        }
        mode = str.lower(mode)
        if mode in av_mode.keys():
            return av_mode.get(mode)
        else:
            logging.error(f"Speech to text mode {mode} not found. Falling back to OfflineS2T.")
            return av_mode.get("offline")


class Speech2TextService:
    """
    This class should be used mainly for the speech to text functionality.
    It is the combination of a singleton and strategy pattern
    """

    __instance = None
    __s2t_interface = None

    # singleton pattern
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, mode):
        self.change_mode(mode)

    def change_mode(self, mode):
        self.__s2t_interface = Speech2TextFactory(mode)

    def trigger(self, text, ssml):
        self.__s2t_interface.trigger()