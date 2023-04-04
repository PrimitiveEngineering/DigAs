from core.speechToText import Speech2TextService
from core.textToSpeech import Text2SpeechService
from morningCon import MorningCon

t2s = Text2SpeechService("azure")
s2t = Speech2TextService("google")
morning_con = MorningCon(t2s, s2t)

morning_con.start_morning_routine()
