from abc import ABC, abstractmethod
import logging
import speech_recognition as sr


class Speech2TextAbstract(ABC):
    __instance = None

    # singleton pattern
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @abstractmethod
    def trigger(self):
        pass


class OnlineS2TnotAvailable(Exception):
    """
    Exception if some online s2t isn't working as expected
    """

    def __init__(self, message):
        """
        Exception if some online s2t isn't working as expected
        :param message: error message
        """
        logging.error(message)


class _OfflineS2T(Speech2TextAbstract):
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
            print("Calibrating...")
            r.adjust_for_ambient_noise(source)
            print("Say something!")
            audio = r.listen(source)

        # recognize speech using Sphinx
        try:
            output = r.recognize_sphinx(audio)
            return (output, True)
        except sr.UnknownValueError:
            return ("Sphinx could not understand audio", False)
        except sr.RequestError as e:
            return ("Sphinx error; {0}".format(e), False)


class _GoogleS2T(Speech2TextAbstract):
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
            print("Calibrating...")
            r.adjust_for_ambient_noise(source)
            print("Say something!")
            audio = r.listen(source)

        # recognize speech using Google Speech Recognition
        try:
            output = r.recognize_google(audio)
            return (output, True)
        except sr.UnknownValueError:
            return ("Google Speech Recognition could not understand audio", False)
        except sr.RequestError as e:
            # Throw exception
            raise OnlineS2TnotAvailable("GoogleS2T failed")


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
    __s2t_abstract = None

    # singleton pattern
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, mode):
        self.change_mode(mode)

    def change_mode(self, mode):
        self.__s2t_abstract = Speech2TextFactory(mode)

    def trigger(self):
        try:
            return self.__s2t_abstract.trigger()
        except OnlineS2TnotAvailable:
            fallback_s2t = Speech2TextFactory("offline")
            return fallback_s2t.trigger()
