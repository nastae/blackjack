import deck as d
from play import Player, Dealer
import display
import os

def main():
    menu()

def menu():
    print('Welcome to terminal blackjack!')
    option = ''
    while option not in ['s', 'q']:
        print('1. Type "s" and press Enter to start the game of blackjack.')
        print('2. Type "q" and press Enter to quit the program.')
        option = input('Your choice: ')
    if option == 's':
        startGame()
    elif option == 'q':
        pass

def startGame():
    name = input('Write your name: ')
    option = ''
    while option != 'q':
        game(name)
        option = input('Press Enter to play again or type a "q" to end the program: ')

def game(name):
    print('A new game started!')
    deck = d.getShuffledDeck()
    dealer = Dealer('dealer')
    player = Player(name)
    dealer.hit(deck)
    player.hit(deck)
    player.hit(deck)
    display.print_hands([dealer, player])
    print(name, 'turn!')
    playerHandValue = player.play(deck, display)
    if playerHandValue <= 21:
        dealerHandValue = dealer.play(deck, display)
        if dealerHandValue <= 21:
            if playerHandValue >= dealerHandValue:
                print('{sep}\nYou won!\n{sep}\n'.format(sep='-' * 16))
            else:
                print('{sep}\nYou lost!\n{sep}\n'.format(sep='-' * 16))

if __name__ == '__main__':
    main()