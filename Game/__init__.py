"""
By Alexander Bjørnsrud
Aka The Bot Master
"""

import discord
import asyncio
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

        """No open world im afraid"""
        self.choices = {
            1:self.checkCards,
            2:self.submit
        }

    """Starts a round"""
    async def round(self,client,channel):
       """Draws from b deck"""
       self.currentCard = self.black.draw()

       out = """
       +-------------------------------------+
       Current Card:
            {}
            Pick {}
       """.format(self.currentCard["text"],self.currentCard["pick"])
       await client.send_message(channel,out)

       """
       Lets evry player take an action, based on the action menu
       """
       for i in self.players:
           self.currentPlayer = self.players[i]
           if i not in self.playerNames: self.playerNames.append(i)
           await client.send_message(channel,"+-------------------------------------+")
           out = """
               {}'s turn to pick cards.
               """.format(i.mention)
           await client.send_message(channel,out)
           while True:
                    options = """
                    Hello {}!
                    My options are: "Cards" or "Submit" followed by a <number>
                        Cards: Shows cards
                        Submit: Sends the numbered card to me
                    """.format(i.mention)
                    await client.send_message(i,options)
                    response = await client.wait_for_message(author=i)
                    if "cards" in response.content or "Cards" in response.content:
                        await self.checkCards(i,client,channel)
                    elif "submit" in response.content or "Submit" in response.content:
                        resp = response.content.split()
                        if len(resp[-1]) > 0:
                            await self.submit(resp[1:],client,i)
                            break

       for i,x in zip(self.players,range(len(self.players))):
             card = self.currentCard["text"]
             out = "{}: {} :".format(x,i.mention)
             await client.send_message(channel,out)
             if re.search("_:",card) != None:
                 for n in self.submitted[i]["cards"]:
                    card = re.sub("_:",n,card,1)
                 await client.send_message(channel,card)
             else:
                 await client.send_message(channel,"{} : {}".format(card,self.submitted[i]["cards"][0]))

       """Vote starts"""

       contestants = await self.vote(client,channel)

       """if the votes are tied, rince and repeat"""
       while max(contestants.values()) <= 1:
           await client.send_message(channel,"Cannot Be a tie!")
           contestants = await self.vote(client,channel)

       winner = max(contestants, key=contestants.get)
       await client.send_message(channel,"The point goes to {}".format(winner))
       self.players[winner].points += 1


    async def vote(self,client,channel):
        """Mke sure all votes are zero"""
        for i in self.players:
            self.submitted[i]["votes"] = 0

        """Let the voting begin"""
        for i in self.players:
            await client.send_message(channel,"+-------------------------------------+")
            out = """{}'s turn to Vote.""".format(i.mention)
            await client.send_message(channel,out)
            result = None
            while True:
                await client.send_message(i,"{} Its your time to vote!".format(i.mention))
                await client.send_message(i, "Vote with Vote <Number>")
                result = await client.wait_for_message(author=i)
                if "vote" in result.content or "Vote" in result.content:
                    break
            result = result.content.split()[1:]
            for i, x in zip(self.players, range(len(self.players))):
                if x == int(result[-1]):
                    self.submitted[i]["votes"] += 1

        """OH hamsund"""
        contestants = {}
        for i in self.submitted:
            contestants[i] = self.submitted[i]["votes"]
        return contestants

    async def submit(self,x,client,channel):
        print(x)
        x_prime = []
        cards = []
        """
        Making shure all picks have been picked.
        """
        if type(x) != list:
            if x == "":
                await client.send_message(channel,"Please enter the card(s) you want to submit:")
                x = await client.wait_for_message(author=channel)
                x = x.split()
                x_prime = x[0] if len(x) == 1 else [x_prime.append(i) for i in x]
            else:
                if len(x) < self.currentCard["pick"]:
                    await client.send_message(channel, "Please enter another card you want to submit:")
                    x = await client.wait_for_message(author=channel)
                    x_prime.append(int(x))

        while (len(x_prime)+1) < self.currentCard["pick"]:
            print(len(x_prime))
            print(type(x))
            if type(x) != list:
                if x == "":
                        await client.send_message(channel, "Please enter another card you want to submit:")
                        x = await client.wait_for_message(author=channel)
                        x = x.split()
                        x_prime = x[0] if len(x) == 1 else [x_prime.append(i) for i in x]
                else:
                    if len(x) < self.currentCard["pick"]:
                        await client.send_message(channel, "Please enter another card you want to submit:")
                        x = await client.wait_for_message(author=channel)
                        x = x.split()
                        x_prime = x[0] if len(x) == 1 else [x_prime.append(i) for i in x]
            else:
                if len(x)< self.currentCard["pick"]:
                    await client.send_message(channel, "Please enter another card you want to submit:")
                    x = await client.wait_for_message(author=channel)
                    x = x.split()
                    x_prime = x[0] if len(x) == 1 else [x_prime.append(i) for i in x]
                else:
                    for i in x:
                        x_prime.append(int(i)) if i not in x_prime else ""
        """TL;DR"""


        """Submit the selected cards by adding them to the array"""
        [cards.append(self.currentPlayer.getCard(int(i))) for i in x]
        self.submitted[self.currentPlayer.name] = {"cards":cards,"votes":0}
        await client.send_message(channel,"[+] Submittd!")

        """Remove the cards form the players hand and draw new ones"""
        self.currentPlayer.done(self.white)

    async def checkCards(self, x,client,channel):
        """Returns all the cardsin the players hand"""
        await client.send_message(channel,"{}, Checks hand".format(x.mention))
        cards = self.currentPlayer.getHand()
        cardbuf = ""

        for i in range(len(cards)):
            cardbuf += "\n{}: {}".format(i,cards[i])

        await client.send_message(x,cardbuf)
