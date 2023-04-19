import time
import schedule
from core.speechToText import Speech2TextService
from core.textToSpeech import Text2SpeechService
from core.scheduleUtil import ScheduleUtil
from morning.morningCon import MorningCon
from joke.jokeCon import JokeCon
from timemgr.timemgrCon import TimemgrCon
from cooking.cookingCon import CookingCon


def main():
    # Init core components
    t2s = Text2SpeechService("azure")
    s2t = Speech2TextService("google")
    schedule_util = ScheduleUtil()

    # Init use case controller
    MorningCon(t2s, s2t, schedule_util)
    JokeCon(t2s, s2t, schedule_util)
    TimemgrCon(t2s, s2t, schedule_util)
    CookingCon(t2s, s2t, schedule_util)

    # ---DEMO---
    # jobs = schedule.get_jobs("morning_routine")
    # jobs = schedule.get_jobs("joke_routine")
    # jobs = schedule.get_jobs("cooking_routine")
    # jobs = schedule.get_jobs("meeting")
    #
    # jobs[0].run()
    # ---DEMO---

    # Run scheduler
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
