import random


TYPES = ['heart', 'spade', 'diamond', 'club']
VALUES = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']


def type():
    return random.choice(TYPES)


def value():
    return random.choice(VALUES)
