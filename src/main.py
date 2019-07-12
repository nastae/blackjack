import deck
from play import Player, Dealer
import display
import os

def main():
    name = input('Write your name: ')
    game_selection = ''
    while game_selection != 'q':
        gameplay(name)
        game_selection = input('Press Enter to play again or type a "q" to end the program: ')

def gameplay(name):
    print('A new game started!\n')
    shuffled_deck = deck.getShuffledDeck()
    dealer = Dealer('dealer')
    player = Player(name)
    dealer.take_card(shuffled_deck)
    player.take_card(shuffled_deck)
    player.take_card(shuffled_deck)
    display.print_hands([dealer, player])
    print(name, 'turn!')
    playerHandValue = player.play(shuffled_deck, display)
    if playerHandValue != None:
        dealerHandValue = dealer.play(shuffled_deck, display)
        if dealerHandValue != None:
            if playerHandValue >= dealerHandValue:
                print('You won!')
            else:
                print('You lost!')

if __name__ == '__main__':
    main()