import random

def getDecks(deckCount=1):
    return ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'B', 'Q', 'K', 'A'] * 4 * deckCount

def getShuffledDeck():
    deck_copy = getDecks()
    random.shuffle(deck_copy)
    return deck_copy