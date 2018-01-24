"""
By Alexander Bjørnsrud
Aka The Bot Master

This is a Cards against humanity clone made in python.
Thanks to Ranadom person on the internett for submitting the cards in json format.
"""

import discord
import asyncio
from Game import Game


client = discord.Client()

channel = "404046560322781188"

players = []

async def changeStatus(status):
    await client.change_presence(game=discord.Game(name=status))

#

@client.event
async def on_ready():
    await changeStatus("Waiting for players to Join!")
    c = client.get_channel(channel)
    await client.send_message(c,"""
|+-----------------------------------------------------------------------+|    
$|    Oy! Ten thousand years will give you such a crick in the neck.|$
$|    WOW!! Does it feel good to be outta there.                                 |$
|+-----------------------------------------------------------------------+|
""")


@client.event
async def on_message(message):
    if message.content.startswith("c!"):
        if "join" in message.content:
            players.append(message.author)
            await client.send_message(message.channel, "+-------------------------------------+")
            await client.send_message(message.channel,"Added: \n{}".format(message.author.mention))

        if "start" in message.content:
            await changeStatus("Playing Cards Against Humanity!")
            channel = message.channel
            await client.send_message(message.channel, "+-------------------------------------+")
            await client.send_message(channel,"Starting game with:")
            for i in players:
                    await client.send_message(channel,i.mention)
            game = Game(players)
            while True:
                await client.send_message(message.channel, """+-------------------------------------+
                   Do you want to:_?
                          1: Start a new round
                          2: Exit
                """)
                response = await client.wait_for_message()
                if "1" in response.content:
                    await game.round(client,channel)
                elif "2" in response.content:
                    game = ""
                    break




        if "card" in message.content:
            out = """
                   +-------------------------------------+
                   Current Card:
                        {}
                        Pick {}
                   """.format(game.currentCard["text"], game.currentCard["pick"])
            await client.send_message(channel, out)





client.run("NDA1MDkwOTg1NTA1MzI1MDY3.DUnXSg.Yn029C23MR-VS1qI11J1jfPU8yU")