class Card:
    def __init__(self, suit, number):
        self.suit = suit
        self.number = number


    #prints the value of the top card of the deck
    def printCard(self):
        s = ""
        if self.number == 11:
            s = s+ "Jack"
        elif self.number == 12:
            s = s + "Queen"
        elif self.number == 13:
            s = s + "King"
        elif self.number == 1:
            s = s + "Ace"
        else:
            s = s + str(self.number)
        if self.suit == 0:
            s = s + " \u2663"
        elif self.suit == 1:
            s = s + " \u2666"
        elif self.suit == 2:
            s = s + " \u2665"
        else:
            s = s + " \u2660"

        return s
