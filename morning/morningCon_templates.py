from core.textToSpeech import Text2SpeechService


def showcaseT2S():
    offline_t2s = False

    # TODO: discuss .env file scope and use it here
    t2s = Text2SpeechService("Azure")

    if offline_t2s:
        text = "Good morning Jonathan. It is 10:00. Today the 03/09/2023 in Stuttgart cloudy weather is forecasted. " \
               "It's currently 5 degrees. A maximum temperature of 12 degrees is expected and 5 degrees at night. " \
               "Your first appointment in the calendar is at 14:15 at the DHBW Stuttgart. " \
               "What do you want to come with today?"
    else:
        text = "Good morning Jonathan. It is <say-as interpret-as=\"time\" format=\"undefined\">10:00</say-as>. " \
               "Today the <say-as interpret-as=\"date\" format=\"mdy\">03/09/2023</say-as> in " \
               "<lang xml:lang=\"de-DE\">Stuttgart</lang> cloudy weather is forecasted. It\'s currently 5 degrees. " \
               "A maximum temperature of 12 degrees is expected and 5 degrees at night. " \
               "Your first appointment in the calendar is at " \
               "<say-as interpret-as=\"time\" format=\"undefined\">14:15</say-as>. at the " \
               "<lang xml:lang=\"de-DE\">DHBW Stuttgart</lang>. What do you want to come with today?"
    t2s.trigger(text, True)


# showcaseT2S()
