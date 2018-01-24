import numpy as np

class Player:
    def __init__(self,name,deck):
        self.played = []
        self.name = name
        self.hand = []
        self.numCards = 0
        self.points = 0
        self.tsar = False
        for i in range(11):
            self.draw(deck)


    def draw(self,deck):
        self.hand.append(deck.draw())

    def checkHand(self):
        if len(self.hand) > 10:
            del self.hand[np.random.randint(0,len(self.hand))]
    def getHand(self):
        return self.hand

    def done(self,deck):
        for i in self.played:
            del self.hand[i]
        for _ in range(len(self.played)):
            self.draw(deck)
        self.played = []

    def getCard(self,num):
        card = self.hand[num]
        self.played.append(num)
        return card

