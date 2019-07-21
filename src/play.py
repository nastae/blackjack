class Player:
    
    def __init__(self, name, bank):
        self.__name = name
        self.__bank = bank
        self.__hands = []
        self.__hands.append(Hand(self.__name))
    
    def splitHand(self):
        del self.__hands[0].getHand()[1]
        self.__hands.append(Hand(self.__name))
        self.__hands[1].getHand().append(self.__hands[0].getHand()[0])

    def play(self, deck):
        option = ''
        if self.__isDoublingDown():
            self.print_hand()
            option = self.__chooseDoublingDown()
            if option == 'y':
                print('You doubled your bet!')
                self.print_hand()

        if self.__isSplittingPairs():
            self.print_hand()
            option = self.__chooseSplitting()
            if option == 'y':
                self.splitHand()
                self.print_hand()

        for hand in self.__hands:
            option = self.__choosePlay()
            value = hand.countValue()
            while option != 's' and value <= 21:
                if option == 'h':
                    hand.hit(deck)
                    self.print_hand()
                value = hand.countValue()
                if value <= 21:
                    option = self.__choosePlay()
        return self.__getMaxHandValue()

    def __getMaxHandValue(self):
        max_value = self.__hands[0].countValue()
        for hand in self.__hands:
            temp = hand.countValue()
            if (temp > max_value and temp <= 21) or (max_value > 21 and temp <= 21):
                max_value = temp
        return max_value

    def __choosePlay(self):
        choosing_text = 'Choose a play, type whether "s" to stand or "h" (hit) to ask for another card: '
        option = input(choosing_text)
        while option not in ['h', 's']:
            print('The chosen key is incorrect. Try again!')
            option = input(choosing_text)
        return option

    def __chooseSplitting(self):
        choosing_text = 'Type "y" to split your hand or "n" to cancel: '
        option = input(choosing_text)
        while option not in ['y', 'n']:
            print('The chosen key is incorrect. Try again!')
            option = input(choosing_text)
        return option

    def __chooseDoublingDown(self):
        choosing_text = 'Type "y" to double your bet or "n" to cancel: '
        option = input(choosing_text)
        while option not in ['y', 'n']:
            print('The chosen key is incorrect. Try again!')
            option = input(choosing_text)
        return option

    def __isSplittingPairs(self):
        return len(self.__hands[0].getHand()) == 2 and self.__hands[0].getHand()[0] == self.__hands[0].getHand()[1]

    def __isDoublingDown(self):
        return len(self.__hands[0].getHand()) == 2 and self.__hands[0].countValue() in [9, 10, 11]

    def getHands(self):
        return self.__hands

    def getName(self):
         return self.__name

    def getBank(self):
        return self.__bank

    def minusBank(self, minus):
        self.__bank = self.__bank - minus
    
    def addBank(self, addition):
        self.__bank = self.__bank + addition

    def print_bank(self):
        print("Player: {name}\nBank: {bank}".format(
            name=self.__name,
            bank=self.__bank))

    def print_hand(self):
        print("{sep}\n{name}\n{hand}\n{value}\n{sep}\n".format(
                sep='-' * 16, 
                name='Dealer' if isinstance(self, Dealer) else 'Player: ', 
                hand=self.__getHand(),
                value=self.__getHandValue()))

    def __getHand(self):
            if len(self.getHands()) == 1:
                    return "Hand: " + " ".join(map(str, self.getHands()[0].getHand()))
            else:
                    return 'Right hand: ' + " ".join(map(str, self.getHands()[0].getHand())) + ', left hand: ' + " ".join(map(str, self.getHands()[1].getHand()))

    def __getHandValue(self):
            if len(self.getHands()) == 1:
                    return "Hand value: " + str(self.getHands()[0].countValue())
            else:
                    return "Right hand value: " + str(self.getHands()[0].countValue()) + ", left hand value: " + str(self.getHands()[1].countValue())

    def clear(self):
        self.__hands = []
        self.__hands.append(Hand(self.__name))

class Hand:
    def __init__(self, owner):
        self.__owner = owner
        self.__hand = []
    
    def hit(self, deck):
        if len(deck) == 0:
            raise Exception('Deck is empty!')
        card = deck[0]
        print(self.__owner, 'gave', card, '!')
        self.__hand.append(card)
        del deck[0]
        return card

    def countValue(self):
        value = 0
        for card in self.__hand:
            if card.isdigit():
                value += int(card)
            if card in ['B', 'Q', 'K']:
                value += 10
        value += self.countAcesValue(value)
        return value

    def countAcesValue(self, valueWithoutAces):
        aceCount = self.__hand.count('A')
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

    def getHand(self):
        return self.__hand

class Dealer(Player):
    def play(self, deck):
        value = self.getHands()[0].countValue()
        while value < 17:
            self.getHands()[0].hit(deck)
            value = self.getHands()[0].countValue()
        self.print_hand()
        return value