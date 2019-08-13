

def sum_cards(cards):
    return sum(__value(c.value) for c in cards)


def __value(card):
    if card == 'A':
        return 10
    elif card in ['J', 'Q', 'K']:
        return 10
    else:
        return int(card)
