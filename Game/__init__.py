"""
By Alexander Bjørnsrud
Aka The Bot Master
"""

from Decks import Deck
from Players import Player
import re
import numpy as np


"""
You have lost the game!
The game class is defined here
"""
class Game:
    def __init__(self,names):
        """Holds the current Black card"""
        self.currentCard = {"text":"","pick":0}

        """The b & w decks"""
        self.black = Deck("blackCards")
        self.white = Deck("whiteCards")

        """Holds the current player to do an action"""
        self.currentPlayer = Player("", self.white)

        """A list of all players"""
        self.players = {}
        for i in names:
            self.players[i] = Player(i,self.white)


        """A list of all the player names, wil act as indexing"""
        self.playerNames = []

        """Holds All submitted Cards"""
        self.submitted = {}
        self.submittedCards = []


        """
        Geeeeeet ready!!!!!!
        Our champions wil battle with intence ferocity!
        """
        print("[+] Starting Game with the Players:")
        t = 0
        """List all current players"""
        for i in self.players:
            print("\t{}: {}".format(t,self.players[i].name))
            t+=1

        """No open world im afraid"""
        self.choices = {
            1:self.checkCards,
            2:self.submit
        }

    """Starts a round"""
    def round(self):
       """Draws from b deck"""
       self.currentCard = self.black.draw()

       out = """
       Current Card:
            {}
            Pick {}
       """.format(self.currentCard["text"],self.currentCard["pick"])
       print(out)

       """
       Lets evry player take an action, based on the action menu
       """
       for i in self.players:
           self.currentPlayer = self.players[i]
           if i not in self.playerNames: self.playerNames.append(i)
           while True:
               print("-"*100)
               out = """
               {}'s turn to pick.
               Choices:
                        1: Check Cards
                        2: Submit Cards <number>
                        3: Done
               """.format(i)
               print(out)

               result = input(">")
               result = result.split()

               if int(result[0])< 3:self.choices[int(result[0])](result[1:] if len(result) > 1 else "")
               if int(result[0]) > 1:break
               if int(result[0]) < 1:continue

       for i in range(len(self.playerNames)):
             card = self.currentCard["text"]

             out = "{}: {} :".format(i,self.playerNames[i])
             print(out)

             if re.search("_:",card) != None:
                 for n in self.submitted[self.playerNames[i]]["cards"]:
                    card = re.sub("_:",n,card,1)
                 print(card)
             else:
                 print("{} : {}".format(card,self.submitted[self.playerNames[i]]["cards"][0]))

       """Vote starts"""

       contestants = self.vote()

       """if the votes are tied, rince and repeat"""
       while max(contestants.values()) <= 1:
           print("Cannot Be a tie!")
           contestants = self.vote()

       winner = max(contestants, key=contestants.get)
       print("The point goes to {}".format(winner))
       self.players[winner].points += 1


    def vote(self):
        """Mke sure all votes are zero"""
        for i in self.playerNames:
            self.submitted[self.playerNames[i]]["votes"] = 0

        """Let the voting begin"""
        for i in self.playerNames:
            out = """{}'s turn to Vote.""".format(i)
            print(out)
            result = input(">")
            result = result.split()
            self.submitted[self.playerNames[int(result[0])]]["votes"] += 1

        """OH hamsund"""
        contestants = {}
        for i in self.submitted:
            contestants[i] = self.submitted[i]["votes"]
        return contestants



    def submit(self,x):
        x_prime = []
        cards = []


        """
        Making shure all picks have been picked.
        """
        if type(x) != list:
            if x == "":
                x = input("Please enter the card(s) you want to submit:")
                x = x.split()
                x_prime = x[0] if len(x) == 1 else [x_prime.append(i) for i in x]
            else:
                if len(x) < self.currentCard["pick"]:
                    x = input("Please enter another card to submit:")
                    x_prime.append(int(x))

        while (len(x_prime)+1) < self.currentCard["pick"]:
            print(len(x_prime))
            print(type(x))
            if type(x) != list:
                if x == "":
                        x = input("Please enter the card(s) you want to submit:")
                        x = x.split()
                        x_prime = x[0] if len(x) == 1 else [x_prime.append(i) for i in x]
                else:
                    if len(x) < self.currentCard["pick"]:
                        x = input("Please enter another card to submit:")
                        x_prime.append(int(x))
            else:
                if len(x)< self.currentCard["pick"]:
                    x = input("Please enter another card to submit:")
                    x_prime.append(int(x))
                else:
                    for i in x:
                        x_prime.append(int(i)) if i not in x_prime else ""
        """TL;DR"""


        """Submit the selected cards by adding them to the array"""
        [cards.append(self.currentPlayer.getCard(int(i))) for i in x]
        self.submitted[self.currentPlayer.name] = {"cards":cards,"votes":0}
        print("[+] Submittd!")

        """Remove the cards form the players hand and draw new ones"""
        self.currentPlayer.done(self.white)

    def checkCards(self, x):
        """Returns all the cardsin the players hand"""
        cards = self.currentPlayer.getHand()
        for i in range(len(cards)):
            print("{}: {}".format(i,cards[i]))
