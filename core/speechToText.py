import speech_recognition as sr


class SpeechToTextInterface:
    def get_speech_test(self):

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

        # recognize speech using Google Speech Recognition
        print("Google:")
        try:
            print("\"" + r.recognize_google(audio) + "\"")
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

    def get_speech(self):

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

s2t = SpeechToTextInterface()

print("Output: " + s2t.get_speech())