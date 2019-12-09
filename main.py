import csv
import Deck
import Hand
import DataAccess
import pandas as pd
from sklearn.linear_model import LogisticRegression

def clearScreen():
    print("\n" * 100)

def MainMenu(name):
    choice = 0
    #loop through main menu util user quits
    while(choice != 4):
        choice = 0
        clearScreen()
        print("Welcome", name, "to Blackjack Game!")
        print("1. Play Game")
        print("2. View Leaderboard")
        print("3. View Your Score")
        print("4. Quit")

        #loop through for valid input
        while choice != 1 and choice != 2 and choice != 3 and choice != 4:
            try:
                choice = int(input("Please enter a choice."))
            except:
                choice = 0
                continue

        if(choice == 1):
            #play game
            clearScreen()
            newG = Game(name)
            newG.playGame()
            dummyvar = input("Press any button to continue.")

        elif(choice == 2):
            #view leaderboard
            clearScreen()
            viewScoreboard()
            dummyvar = input("Press any button to continue.")

        elif(choice == 3):
            #view your score
            clearScreen()
            viewYourScore()
            dummyvar = input("Press any button to continue.")


def viewScoreboard():
    print("###Scoreboard###")
    scoreboard = pd.read_csv('scoreboard.csv')
    #get scoreboard, group by player name, and sort by wins first, then losses
    scoreboard = scoreboard.groupby(['name']).sum()
    scoreboard.sort_values(by=['win', 'loss'], inplace=True, ascending=[False, True])
    print(scoreboard)

def viewYourScore():
    print("###Your Score###")
    #gets the score for only your name
    scoreboard = pd.read_csv('scoreboard.csv')
    scoreboard = scoreboard[scoreboard['name'].str.contains(pname)].groupby(['name']).sum()
    print(scoreboard)

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

    def __init__(self, name):
        self.Deck = Deck.Deck()
        self.pname = name
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
                self.playerActionArr.append(['data.csv', self.pname, self.playerHand.countScore(),
                                             self.compHand.countScore(), self.playerHand.hasAce, playerchoice])
                self.playerHand.addCard(self.Deck.drawCard())
                #check if player loses
                if self.playerHand.checkBusted():
                    self.winner = True
                    break
            else:
                self.playerActionArr.append(
                    ['data.csv', self.pname, self.playerHand.countScore(), self.compHand.countScore(),
                     self.playerHand.hasAce, 0])
            #computer decision
            #compChoice = self.computerAction()
            compChoice = self.compAIDecision()
            if compChoice == 1:
                self.compActionArr.append(['data.csv', self.pname, self.playerHand.countScore(), self.compHand.countScore
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
                    ['data.csv', self.pname, self.playerHand.countScore(),
                     self.compHand.countScore(), self.compHand.hasAce, 0])
                self.compMsg = "Computer stayed."

            #if both computer and player stayed game ends
            if compChoice == 0 and playerchoice == 2:
                if self.playerHand.countScore() == self.compHand.countScore():
                    self.draw = True
                elif self.playerHand.countScore() > self.compHand.countScore():
                    self.winner = True
                    self.playerWin = True
                elif self.compHand.countScore() > self.playerHand.countScore():
                    self.winner = True
                break

        #determine results, and based on who wins, adds the winner's actions to the dataset for learning
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
        return(int(self.logreg.predict(x_new)))

    def computerAction(self):
        #to be replaced with AI decision tree
        if 21 >= self.playerHand.countScore() > self.compHand.countScore():
            return 1

        #blackjack "rulebook" says you should hit on less than 16 due to odds of hand improvement without busting out
        elif (self.compHand.countScore() <= 15):
            return 1

        #"rulebook" also says you should hit on 16 when you have an ace due to odds of hand improvement without busting out
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


        #add result to your personal score
        DataAccess.add_score(self.pname, self.playerWin, playerLoss, self.draw)

        print("Player Score: ", self.playerHand.countScore())
        print("Player Hand: ", self.playerHand.printHand())
        print("Computer Score: ", self.compHand.countScore())
        print("Computer Hand: ", self.compHand.printHand())
        if self.playerWin is True:
            return "Congratulations, you won!"
        elif self.playerWin is False and self.draw is True:
            return "Well, it's a draw!"
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




####   MAIN #####

pname = input("Please enter your name.")

#prevents issues with uploading data to csv file
while(pname.__contains__(',')):
    pname = input("Please enter your name without commas.")


#prevent program display error for first entry into the game.
DataAccess.add_score(pname, 0, 0, 0)

MainMenu(pname)
print("Thank you for playing!")

