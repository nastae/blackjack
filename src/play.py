class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
    
    def hit(self, deck):
        if len(deck) == 0:
            raise Exception('Deck is empty!')
        card = deck[0]
        print(self.name, 'gave', card, '!')
        self.hand.append(card)
        del deck[0]
        return card

    def countHandValue(self):
        value = 0
        for card in self.hand:
            if card.isdigit():
                value += int(card)
            if card in ['B', 'Q', 'K']:
                value += 10
        value += self.countAcesValue(value)
        return value

    def countAcesValue(self, valueWithoutAces):
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

    def play(self, deck, display):
        option = self.__choosePlay()
        value = self.countHandValue()
        while option != 's' and value <= 21:
            if option == 'h':
                self.hit(deck)
                display.print_hands([self])
            value = self.countHandValue()
            if value > 21:
                print("{sep}\nTotal value of your hand is {value}!\nYou lost!\n{sep}\n".format(
                    sep='-' * 16,
                    value=value))
            else:
                option = self.__choosePlay()
        return value

    def __choosePlay(self):
        choosing_text = 'Choose a play, type whether "s" to stand or "h" (hit) to ask for another card: '
        option = input(choosing_text)
        while option not in ['h', 's']:
            print('The chosen key is incorrect. Try again!')
            option = input(choosing_text)
        return option

    def getHand(self):
        return self.hand

    def getName(self):
         return self.name

class Dealer(Player):
    def play(self, deck, display):
        value = self.countHandValue()
        while value < 17:
            self.hit(deck)
            value = self.countHandValue()
            if value > 21:
                print("{sep}\nTotal value of dealer's hand is {value}!\nYou won!\n{sep}\n".format(
                    sep='-' * 16,
                    value=value))
        display.print_hands([self])
        return value