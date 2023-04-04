import random
import os


class FortuneCookieService:
    """
    Fortune Cookie Service

    Arguments:
    None

    Returns:
    - quote as string
    """

    fortunes = []

    def __init__(self) -> None:
        f = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "fortuneList.txt"), "r", encoding='utf8')
        lines = f.readlines()

        for line in lines:
            self.fortunes.append(line)

    def fortune_cookie_service_request(self, joke_number=None):

        if joke_number is None:
            joke_number = random.randint(0, len(self.fortunes))

        return self.fortunes[joke_number]
