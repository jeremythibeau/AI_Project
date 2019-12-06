import Deck
import Hand
from Card import Card

def clearScreen():
    print("\n" * 100)

class Game:

    playerWin = False
    winner = False
    draw = False
    compMsg = ""

    def __init__(self):
        self.Deck = Deck.Deck()

        self.playerHand = Hand.Hand()
        self.compHand = Hand.Hand()

        #Draw starting hands
        self.playerHand.addCard(self.Deck.drawCard())
        self.compHand.addCard(self.Deck.drawCard())
        self.playerHand.addCard(self.Deck.drawCard())
        self.compHand.addCard(self.Deck.drawCard())


    def playGame(self):
        #loop until a winner is determined
        while self.winner is False:

            #check for blackjacks
            if self.playerHand.blackJackCheck() is True and self.compHand.blackJackCheck() is False:
                self.winner = True
                self.playerWin = True
                break
            elif self.playerHand.blackJackCheck() is True and self.compHand.blackJackCheck() is True:
                self.winner = True
                self.draw = True
                break
            elif self.playerHand.blackJackCheck() is False and self.compHand.blackJackCheck() is True:
                self.winner = True
                break

            #player decision
            playerchoice = self.turnScreen()
            if playerchoice == 1:
                self.playerHand.addCard(self.Deck.drawCard())
                #check if player loses
                if self.playerHand.checkBusted():
                    self.winner = True
                    break

            #computer decision
            compChoice = self.computerAction()
            if compChoice == 1:
                self.compMsg = "Computer hit."
                self.playerHand.addCard(self.Deck.drawCard())
                #check if computer loses
                if self.playerHand.checkBusted():
                    self.winner = True
                    self.playerWin = True
                    break
            else:
                self.compMsg = "Computer stayed."

            #if both computer and player stayed game ends
            if compChoice == 2 and playerchoice == 2:
                if self.playerHand.countScore() == self.compHand.countScore():
                    self.draw = True
                break

        #determine results
        print(self.determineWinner())

    def computerAction(self):
        #to be replaced with AI decision tree
        if 21 >= self.playerHand.countScore() > self.compHand.countScore():
            return 1

        #blackjack "rulebook" says you should hit on less than 16 due to odds of hand improvement without busting out
        elif self.playerHand.countScore() == self.compHand.countScore() and self.compHand.countScore() <= 15:
            return 1
        return 2

    def determineWinner(self):
        clearScreen()
        print("Player Score: ", self.playerHand.countScore())
        print("Player Hand: ", self.playerHand.printHand())
        print("Computer Score: ", self.compHand.countScore())
        print("Computer Hand: ", self.compHand.printHand())
        if self.playerWin is True:
            return "Congratulations you won!"
        elif self.playerWin is False and self.draw is True:
            return "Well, it's a draw! Shall we go again to settle the tie?"
        return "Better luck next time, I won."

    def turnScreen(self):
        clearScreen()
        print(self.compMsg)
        print("################")
        print("Player Hand:")
        print(self.playerHand.printHand())
        print("Player Score: ", self.playerHand.countScore())
        print("################")
        print("Computer Cards Showing:")
        print(self.compHand.printCompHand())
        print("Cards in deck: ", self.Deck.numCards)
        print("################")
        choice = 0

        while choice != 1 and choice != 2:
            try:
                choice = int(input("Please enter to 1 hit or 2 stay, then press enter."))
            except:
                choice = 0
                continue

        return choice


x = Game()
x.playGame()