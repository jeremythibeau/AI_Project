from six import unichr
import csv
import Deck
import Hand
import DataAccess
import pandas as pd
import numpy as np
import sklearn
from sklearn.linear_model import LogisticRegression
from Card import Card

def clearScreen():
    print("\n" * 100)


class Game:

    playerWin = False
    winner = False
    draw = False
    compMsg = ""
    playerActionArr = []
    compActionArr = []
    logreg = LogisticRegression(solver='lbfgs')
    dataset = pd.read_csv('data.csv')
    feature_cols = ['player_score', 'comp_score', 'computerHasAce']
    X = dataset.loc[:, feature_cols]
    Y = dataset.decision.astype(int)
    logreg.fit(X, Y)

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


            #used to make player play automatically
            #playerchoice = self.playerAutoAction()
            if playerchoice == 1:
                self.playerActionArr.append(['data.csv', 'dataset', self.playerHand.countScore(),
                                             self.compHand.countScore(), self.playerHand.hasAce, playerchoice])
                self.playerHand.addCard(self.Deck.drawCard())
                #check if player loses
                if self.playerHand.checkBusted():
                    self.winner = True
                    break
            else:
                self.playerActionArr.append(
                    ['data.csv', 'dataset', self.playerHand.countScore(), self.compHand.countScore(),
                     self.playerHand.hasAce, 0])
            #computer decision
            #compChoice = self.computerAction()
            compChoice = self.compAIDecision()
            if compChoice == 1:
                self.compActionArr.append(['data.csv', 'dataset', self.playerHand.countScore(), self.compHand.countScore
                (), self.compHand.hasAce, compChoice])
                self.compMsg = "Computer hit."
                self.compHand.addCard(self.Deck.drawCard())
                #check if computer loses
                if self.compHand.checkBusted():
                    self.winner = True
                    self.playerWin = True
                    break
            else:
                self.compActionArr.append(
                    ['data.csv', 'dataset', self.playerHand.countScore(),
                     self.compHand.countScore(), self.compHand.hasAce, 0])
                self.compMsg = "Computer stayed."

            #if both computer and player stayed game ends
            if compChoice == 0 and playerchoice == 2:
                if self.playerHand.countScore() == self.compHand.countScore():
                    self.draw = True
                break

        #determine results
        if(self.playerWin):
            for x in self.playerActionArr:
                DataAccess.append_data(x)
        elif(self.playerWin == False and self.draw == False):
            for x in self.compActionArr:
                DataAccess.append_data(x)
        print(self.determineWinner())

    def compAIDecision(self):
        fieldnames = ['player_score', 'comp_score', 'computerHasAce']
        with open('newentry.csv', "w", newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({
                "player_score": int(self.playerHand.countScore()),
                "comp_score": int(self.compHand.countScore()),
                "computerHasAce": int(self.compHand.hasAce)
            })

        x = pd.read_csv('newentry.csv')
        x_new = x.loc[:, self.feature_cols]

        #see computer decision
        print(self.logreg.predict(x_new))
        return(self.logreg.predict(x_new))

    def computerAction(self):
        #to be replaced with AI decision tree
        if 21 >= self.playerHand.countScore() > self.compHand.countScore():
            return 1

        #blackjack "rulebook" says you should hit on less than 16 due to odds of hand improvement without busting out
        elif (self.compHand.countScore() <= 15):
            return 1

        elif (self.compHand.countScore() == 16 and self.compHand.hasAce == True):
            return 1
        return 0

    def playerAutoAction(self):
        #was used to auto generate player result
        if 21 >= self.compHand.countScore() > self.playerHand.countScore():
            return 1

        #blackjack "rulebook" says you should hit on less than 16 due to odds of hand improvement without busting out
        elif (self.playerHand.countScore() <= 15):
            return 1

        elif (self.playerHand.countScore() == 16 and self.playerHand.hasAce == True):
            return 1
        return 0

    def determineWinner(self):
        clearScreen()
        if self.playerWin or self.draw:
            playerLoss = False
        else:
            playerLoss = True

        DataAccess.add_score("jeremy", self.playerWin, playerLoss, self.draw)

        print("Player Score: ", self.playerHand.countScore())
        print("Player Hand: ", self.playerHand.printHand())
        print("Computer Score: ", self.compHand.countScore())
        print("Computer Hand: ", self.compHand.printHand())
        if self.playerWin is True:
            return "Congratulations, you won!"
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

#y = pd.read_csv('data.csv').head(3)
#print(y.computerHasAce)
#print(y['decision'].sum())