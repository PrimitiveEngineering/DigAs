import random


class FortuneCookieService:
    '''
    Fortune Cookie Service

    Arguments:
    None

    Returns:
    - quote as string
    '''


    fortunes = []

    def __init__(self) -> None:
        f = open("joke/fortuneList.txt", "r", encoding='utf8')
        Lines = f.readlines()

        for line in Lines:
            self.fortunes.append(line)

    def fortuneCookieServiceRequest(self):

        rand = random.randint(0, len(self.fortunes))

        return self.fortunes[rand]

    

fc = FortuneCookieService()

print(fc.fortuneCookieServiceRequest())