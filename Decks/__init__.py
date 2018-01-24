import numpy as np
import json

class Deck:
    def __init__(self,name):
        self.stackCounter = 0
        self.discard = []
        self.stack = np.array([])
        self.name = name
        self.getCards()
        self.shuffle()

    def getCards(self):
        self.stack = np.array(json.load(open("cards.json", "r"))[self.name])

    def shuffle(self):
        self.discard = []
        np.random.shuffle(self.stack)

    def draw(self):
        if self.stackCounter in self.discard:
            self.stackCounter = self.stackCounter + 1

        card = self.stack[self.stackCounter]
        self.discard.append(self.stackCounter)
        self.stackCounter = self.stackCounter + 1
        return card
