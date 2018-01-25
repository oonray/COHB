"""
By Alexander Bjørnsrud
Aka The Bot Master

This is a Cards against humanity clone made in python.
Thanks to Ranadom person on the internett for submitting the cards in json format.
"""

import time
import discord
import asyncio
from Game import Game
from Server import Game_Server


Servers = {}

client = discord.Client()

channel = "404046560322781188"

def number(num):
    if "1" in num.content or "2" in num.content or "3" in num.content:
        return True
    else: return False

async def changeStatus(status):
    await client.change_presence(game=discord.Game(name=status))

async def menu2(response,message):
    global Servers
    global client
    if "1" in response.content:
        await Servers[message.server.id].game.round(client, Servers[message.server.id].channel)
        return True
    elif "2" in response.content:
        await client.send_message(Servers[message.server.id].channel, "+-------------------------------------+")
        for i in Servers[message.server.id].game.players:
            await client.send_message(Servers[message.server.id].channel, "{}:{}".format(i.mention,
                                                                      Servers[message.server.id].game.players[i].points
                                                                                         )
                                      )
        return False
    elif "3" in response.content:
        await client.send_message(message.channel, "[-] Exiting!")
        players = []
        game = ""
        return True
    else:
        await client.send_message(message.channel, "[-] Baad Option!")
        return False

async def menu(message):
    while True:
        await client.send_message(message.channel, """+-------------------------------------+
                        Do you want to:_?
                               1: Start a new round
                               2: Leader board
                               3: Exit
                     """)
        time.sleep(1)
        while True:
            time.sleep(1)
            response = await client.wait_for_message(channel=message.channel,check=number)
            b = await menu2(response,message)
            if b:break

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
    global players
    global game


    if message.content.startswith("c!"):
        if message.server.id not in Servers.keys():
            Servers[message.server.id] = Game_Server({
                "id":message.server.id,
                "channel":message.channel,
                "players":[],
                "everyone":client.get_server(message.server.id).roles[0]
            })
        everyone = client.get_server(message.server.id).roles[0]

        if "join" in message.content:
            print(len(Servers[message.server.id].players))
            Servers[message.server.id].players.append(message.author)
            await client.send_message(message.channel, "+-------------------------------------+")
            await client.send_message(message.channel,"{}\n Added: \n{}".format(everyone.mention,message.author.mention))

        if "start" in message.content:
            Servers[message.server.id].channel = message.channel
            print(len(Servers[message.server.id].players))
            if len(Servers[message.server.id].players) < 2:
                await client.send_message(Servers[message.server.id].channel, "+-------------------------------------+")
                await client.send_message(Servers[message.server.id].channel, "Too few players: join with 'c! join'")
            else:
                await changeStatus("Playing Cards Against Humanity!")
                await client.send_message(Servers[message.server.id].channel, """
                +-------------------------------------+
            Starting game with:
                """)
                for i in Servers[message.server.id].players:
                        await client.send_message(Servers[message.server.id].channel,i.mention)
                Servers[message.server.id].start_Game()
                time.sleep(2)
                await menu(message)



        if "card" in message.content:
            out = """
                   +-------------------------------------+
                   Current Card:
                        {}
                        Pick {}
                   """.format(Servers[message.server.id].game.currentCard["text"], Servers[message.server.id].game.currentCard["pick"])
            await client.send_message(Servers[message.server.id].channel, out)


client.run("NDA1MDkwOTg1NTA1MzI1MDY3.DUnXSg.Yn029C23MR-VS1qI11J1jfPU8yU")