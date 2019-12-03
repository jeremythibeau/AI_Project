import Card

class Hand:
    def __init__(self):
        self.score = 0
        self.busted = False
        self.cards = []
        self.hasAce = False
        self.numAces = 0


    #calculates the score of the hand
    def countScore(self):
        self.score = 0
        for i in range(len(self.cards)):
            if self.cards[i].number == 13 or self.cards[i].number == 12 or self.cards[i].number == 11:
                self.score += 10
            elif self.cards[i].number == 1:
                if (self.score + 11) > 21:
                    self.score += 1
                else:
                    self.score += 11
                self.hasAce = True
                #to be used later in score calculation
                self.numAces += 1
            else:
                self.score += self.cards[i].number

        return self.score


    #calculates blackjack
    def blackJackCheck(self):
        if self.countScore() == 21:
            return True
        return False

    #checks if the hand is busted by being over 21
    def checkBusted(self):
        if (self.countScore() > 21):
            self.busted = True

        return self.busted

   #adds a card to the hand
    def addCard(self, card):
        self.cards.append(card)

    #prints hand contents
    def printHand(self):
        s = ""
        for x in range(len(self.cards)):
            s += self.cards[x].printCard() + ", "
        s = s[:-2]
        return s

    def printCompHand(self):
        #computer only shows one card, not both
        s = ""
        for y in range(1, len(self.cards)):
            s += self.cards[y].printCard() + ", "
        s = s[:-2]
        return s