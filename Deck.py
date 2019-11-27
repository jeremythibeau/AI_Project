import Card

class Deck:
    def __init__(self):
        self.numCards = 0
        self.cards = []

        # load the deck
        for i in range(4):
            for y in range(1, 14):
                self.addCard(i, y)

    #add cards to the deck
    def addCard(self, suit, number):
        newCard = Card.Card(suit, number)
        self.cards.append(newCard)
        self.numCards +=1


    # draw the top card of the deck
    def drawCard(self):
        return self.cards.pop(0)

    #print the top card
    def printTop(self):
        return(self.cards[51].printCard())