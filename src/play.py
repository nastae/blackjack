class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
    
    def take_card(self, deck):
        if len(deck) == 0:
            raise Exception('Deck is empty!')
        card = deck[0]
        print(self.name, 'gave', card, '!')
        self.hand.append(card)
        del deck[0]
        return card
    
    def getHand(self):
        return self.hand

    def countHandValue(self):
        value = 0
        for card in self.hand:
            if card.isdigit():
                value += int(card)
            if card in ['B', 'Q', 'K']:
                value += 10
        value += self.countAceValueInHand(value)
        return value

    def countAceValueInHand(self, valueWithoutAces):
        aceCount = self.hand.count('A')
        if aceCount == 1:
            if valueWithoutAces + 11 > 21:
                return 1
            else:
                return 11
        if aceCount == 2:
            if valueWithoutAces + 12 > 21:
                return 2
            else:
                return 12
        if aceCount == 3:
            if valueWithoutAces + 13 > 21:
                return 3
            else:
                return 13
        if aceCount == 4:
            if valueWithoutAces + 14 > 21:
                return 4
            else:
                return 14
        return 0

    def getName(self):
        return self.name

    def play(self, deck, display):
        selection = self.__selectAction()
        handValue = self.countHandValue()
        while selection != 's' and handValue <= 21:
            if selection == 'a':
                self.take_card(deck)
                display.print_hands([self])
            handValue = self.countHandValue()
            if handValue > 21:
                print('Game ended!')
                print('Your total value of the hand is', handValue, '!', 'You lost the game!')
                return None
            else:
                selection = self.__selectAction()
        return handValue

    def __selectAction(self):
        selection_text = 'Select a move by typing a key and pressing Enter. Type an "a" to ask, a "s" to stand: '
        selection = input(selection_text)
        while selection not in ['a', 's']:
            print('The selected key is incorrect. Try again!')
            selection = input(selection_text)
        return selection

class Dealer(Player):
    def play(self, deck, display):
        handValue = self.countHandValue()
        while handValue < 17:
            self.take_card(deck)
            handValue = self.countHandValue()
            if handValue > 21:
                print('Game ended!')
                print('Dealer total value of the hand is', handValue, '!', 'You won the game!')
                return None
        display.print_hands([self])
        return handValue