import random

GREETINGS = ["Guten Tag", "Tag", "Hallo", "Grüß Gott", "Grüß dich", "Grüß Sie", "Griaß Eich",
             "Grüezi", "Grüessech", "Servus", "Heil", "Moin", "Ahoi", "Willkommen", "Mahlzeit"]


def get_hello():
    hello_random = random.SystemRandom()
    return hello_random.choice(GREETINGS)
