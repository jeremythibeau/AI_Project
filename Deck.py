import Card
import random

class Deck:
    def __init__(self):
        self.numCards = 0
        self.cards = []

        # load the deck
        for i in range(4):
            for y in range(1, 14):
                self.addCard(i, y)

        #shuffles the deck
        shufflenum = self.numCards
        newDeck = []
        for x in range(0, shufflenum):
            rand = random.randint(0, self.numCards)
            newDeck.append(self.cards.pop(rand-1))
            self.numCards -= 1

        self.numCards = 52
        self.cards = newDeck


    #add cards to the deck
    def addCard(self, suit, number):
        newCard = Card.Card(suit, number)
        self.cards.append(newCard)
        self.numCards +=1


    # draw the top card of the deck
    def drawCard(self):
        if self.numCards == 0:
            return False
        self.numCards -= 1
        return self.cards.pop(len(self.cards)-1)

    #print the top card
    def printTop(self):
        return(self.cards[len(self.cards)-1].printCard())