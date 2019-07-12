def print_hands(players):
    for player in players:
        print('-' * 16)
        print(player.getName())
        print('Hand:', *player.getHand(), sep = " ")
        print('Hand Value: ', player.countHandValue())
        print('-' * 16)