from play import Dealer

def print_hands(players):
    for player in players:
        print_hand(player)

def print_hand(player):
        print("{sep}\n{name}\nHand: {hand}\nHand value: {value}\n{sep}\n".format(
                sep='-' * 16, 
                name='Dealer' if isinstance(player, Dealer) else 'Player: ' + player.getName(), 
                hand=" ".join(map(str, player.getHand())),
                value=player.countHandValue()))