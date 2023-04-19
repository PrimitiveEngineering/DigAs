import time
import schedule
from core.speechToText import Speech2TextService
from core.textToSpeech import Text2SpeechService
from morning.morningCon import MorningCon
from joke.jokeCon import JokeCon
from cooking.cookingCon import CookingCon


def main():
    # Init core components
    t2s = Text2SpeechService("offline")
    s2t = Speech2TextService("google")

    # Init use case controller
    MorningCon(t2s, s2t)
    JokeCon(t2s, s2t)
    CookingCon(t2s, s2t)

    # Run scheduler
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
