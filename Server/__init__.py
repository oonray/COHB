"""
For evry server

"""

import time
import discord
import asyncio
from Game import Game

class Game_Server:
    def __init__(self,inp):
        self.id = inp["id"]
        self.channel = inp["channel"]
        self.players = inp["players"]
        self.evryone = inp["everyone"]
        self.game_Started = False
        self.game_menu = 0
        self.game_menu_last = 0


    def start_Game(self):
        self.game = Game(self.players,self.id)
        self.game_Started = True
