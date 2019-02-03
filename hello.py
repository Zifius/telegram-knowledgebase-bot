import random

GREETINGS = [
    "Guten Tag", "Tag", "Hallo", "Grüß Gott", "Griaß Gott", "Grüß Dich", "Grüß Sie", "Griaß Eich", "Griaß Di",
    "Habe die Ehre", "Grüezi", "Grüessech", "Servus", "Heil", "Moin", "Abend", "Ahoi", "Willkommen", "Mahlzeit"
]


def get_hello():
    hello_random = random.SystemRandom()
    return hello_random.choice(GREETINGS)
