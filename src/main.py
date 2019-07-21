import deck as d
from play import Player, Dealer
import os

def main():
    menu()

# https://runnable.com/docker/python/dockerize-your-python-application - dockerize
# https://bicyclecards.com/how-to-play/blackjack/ rules

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
    dealer = Dealer('dealer', 0.0)
    player = Player(name, 100.0)
    option = ''
    while option != 'q':
        game(name, dealer, player)
        option = input('Press Enter to play again or type a "q" to end the program: ')

def game(name, dealer, player):
    print('A new game started!')
    deck = d.getShuffledDeck()
    player.print_bank()
    bet = input('Type your bet: ')
    while not (bet.isdigit() and float(bet) > 0 and float(bet) <= player.getBank()):
        print('Wrong bet value!')
        bet = input('Type your bet: ')
    player.minusBank(int(bet))
    dealer.getHands()[0].hit(deck)
    if dealer.getHands()[0].getHand()[0] in ['A', '10']:
        dealer.getHands()[0].hit(deck)
    player.getHands()[0].hit(deck)
    player.getHands()[0].hit(deck)
    for p in [dealer, player]:
        p.print_hand()
    print(name, 'turn!')
    playerHandValue = player.play(deck)
    if playerHandValue <= 21:
        if playerHandValue == 21:
            print('Player gives 1.5x his bet!')
            player.addBank(int(bet) * 1.5)
        dealerHandValue = dealer.play(deck)
        if dealerHandValue <= 21:
            if playerHandValue > dealerHandValue:
                print('{sep}\nYou won!\n{sep}\n'.format(sep='-' * 16))
                player.addBank(int(bet) * 2)
            elif playerHandValue == 21 or playerHandValue == dealerHandValue:
                print('{sep}\nDraw! You gave your bet back!\n{sep}\n'.format(sep='-' * 16))
                player.addBank(int(bet))
            else:
                print('{sep}\nYou lost!\n{sep}\n'.format(sep='-' * 16))
        else:
            print('{sep}\nYou won!\n{sep}\n'.format(sep='-' * 16))
            player.addBank(int(bet) * 2)
    else:
        print('{sep}\nYou lost!\n{sep}\n'.format(sep='-' * 16))
    player.print_bank()
    player.clear()
    dealer.clear()

if __name__ == '__main__':
    main()