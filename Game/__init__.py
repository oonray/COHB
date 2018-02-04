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
    def __init__(self,names,server):
        """Holds the current Black card"""
        self.currentCard = {"text":"","pick":0}
        self.serverid = server
        self.serverName = ""

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
       self.serverName = client.get_server(self.serverid).name
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
       Lets every player take an action, based on the action menu
       """
       for i in self.players:
           self.currentPlayer = self.players[i]
           if i not in self.playerNames: self.playerNames.append(i)
           out = """
               {}'s turn to pick cards.
               """.format(i.mention)
           await client.send_message(channel,out)
           while True:
                    options = """
                    +-------------------------------------+
                    New message from: {} use {} before command to respond 
                    Hello {}!
                    My options are: "Cards", "Black", "Status" or "Submit" followed by a <number>
                        Black: shows black card of server
                        Status: gets the servers waiting for you
                        Cards: Shows cards on server
                        Submit: Sends the numbered card to me
                    """.format(client.get_server(self.serverid).name,
                               client.get_server(self.serverid).name,
                                i.mention
                    )
                    await client.send_message(i,options)

                    response = await client.wait_for_message(author=i)

                    if "status" in response.content.lower():
                        if i.name in response.author.name:
                            await client.send_message(response.author,"""
                            {} is waiting for your response
                            Options are: "Cards", "Black", "Status" or "Submit" followed by a <number>
                            """.format(self.serverName))

                    if self.serverName.lower() in response.content.lower():
                            if "cards" in response.content.lower():
                                await self.checkCards(i,client,channel)
                            elif "black" in response.content.lower():
                                await client.send_message(i,"{} , Pick {}".format(self.currentCard["text"],self.currentCard["pick"]))
                            elif "submit" in response.content.lower():
                                resp = response.content.split()
                                if len(resp[-1]) > 0:
                                    await self.submit(resp[-self.currentCard["pick"]:],client,i)
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
                 out = "{} :".format(card)
                 for i in self.submitted[i]["cards"]:
                     out += i
                 await client.send_message(channel,out)

       """Vote starts"""

       contestants = await self.vote(client,channel)

       """if the votes are tied, rince and repeat"""
       winners = max(contestants, key=contestants.get)
       if contestants[winners] == sum([ contestants[i] for i in contestants.keys()])/len(contestants.keys()):
            for i in contestants.keys():
                self.players[i].points += 1
       else:
        for i in contestants.keys():
           if contestants[i] == contestants[winners]:
            await client.send_message(channel,"A Point goes to {}".format(i))
            self.players[i].points += 1


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
                await client.send_message(i, """
                Message from: {} use {} before command to respond 
                """.format(client.get_server(self.serverid).name,client.get_server(self.serverid).name))
                await client.send_message(i,"{} Its your time to vote!".format(i.mention))
                await client.send_message(i, "Vote with Vote <Number>")
                result = await client.wait_for_message(author=i)
                if self.serverName.lower() in result.content.lower():
                    if "vote" in result.content.lower():
                        break
            result = result.content.split()[2:]
            for i, x in zip(self.players, range(len(self.players))):
                if x == int(result[-1]):
                    self.submitted[i]["votes"] += 1

        """OH hamsund"""
        contestants = {}
        for i in self.submitted:
            contestants[i] = self.submitted[i]["votes"]
        return contestants

    async def submit(self,x,client,channel):
        x_prime = []
        cards = []
        """
        Making shure all picks have been picked.
        """
        if not int(x[0]) in range(10):
            if x == "":
                await client.send_message(channel,"Please enter the card(s) you want to submit:")
                x = await client.wait_for_message(author=channel)
                x = x.split()
                x_prime = x[0] if len(x) == 1 else [x_prime.append(i) for i in x]
            else:
                if len(x) < self.currentCard["pick"]:
                    await client.send_message(channel, "Please enter another card you want to submit:")
                    x = await client.wait_for_message(author=channel)
                    x_prime.append(int(x.content))

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
                    x_prime.append(int(x.content))

        while (len(x_prime)+1) < self.currentCard["pick"]:
            if type(x) != list:
                if x == "":
                        await client.send_message(channel, "Please enter another card you want to submit:")
                        x = await client.wait_for_message(author=channel)
                        x = x.content.split()[2:]
                        x_prime = x[0] if len(x) == 1 else [x_prime.append(i) for i in x]
                else:
                    if len(x) < self.currentCard["pick"]:
                        await client.send_message(channel, "Please enter another card you want to submit:")
                        x = await client.wait_for_message(author=channel)
                        x = x.content.split()[2:]
                        x_prime = x[0] if len(x) == 1 else [x_prime.append(i) for i in x]
            else:
                if len(x)< self.currentCard["pick"]:
                    await client.send_message(channel, "Please enter another card you want to submit:")
                    x = await client.wait_for_message(author=channel)
                    x = x.content.split()[2:]
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
