"""
By Alexander Bjørnsrud
Aka The Bot Master

This is a Cards against humanity clone made in python.
Thanks to Ranadom person on the internett for submitting the cards in json format.
"""

import time
import discord
from Game import Game
from Server import Game_Server
from DiscordBlackMagic import DarkArts #Requires Dark Arts Expansion
import pickle
import subprocess

Masters = ["270827108924784640","409434856917958657"]

Servers = {}

DA = DarkArts(Masters,Servers) #Requires Dark Arts Expansion

client = discord.Client()

channel = ["404046560322781188"]

def log(inp):
    with open("logfile.log","a") as file:
        file.write(inp+"\n")

def error_log(inp):
    with open("error.log","a") as file:
        file.write(inp + "\n")


def number(num):
    if "1" in num.content.lower() or "2" in num.content.lower() or "3" in num.content.lower():
        return True
    else: return False

async def changeStatus(status):
    await client.change_presence(game=discord.Game(name=status))


@client.event
async def on_ready():
    await changeStatus("Waiting for players to Join!")
    try:
        for i in channel:
            await client.send_message(client.get_channel(i), """
                    |+-----------------------------------------------------------------------+|    
                    $|    Oy! Ten thousand years will give you such a crick in the neck.|$
                    $|    WOW!! Does it feel good to be outta there.                                 |$
                    |+-----------------------------------------------------------------------+|
                    """)
    except Exception as e:
        error_log(str(e))

@client.event
async def on_message(message):

    global players
    global game

    if message.channel not in channel:
        log(message.channel.id)

    try:
        if message.server.id not in Servers.keys():
                    Servers[message.server.id] = Game_Server({
                    "id": message.server.id,
                    "channel": message.channel,
                    "players": [],
                    "everyone": client.get_server(message.server.id).roles[0]
                    })
                    DA.Update_Servers(Servers) #Requires Dark Arts Expansion#4000
                    DA.DarkArt(message) #Requires Dark Arts Expansion#4000
    except:
        pass

    if message.content.lower().startswith("c!"):
            everyone = client.get_server(message.server.id).roles[0]
            server = message.server

            if "join" in message.content.lower():
                Servers[server.id].players.append(message.author)
                await client.send_message(message.channel, "+-------------------------------------+")
                await client.send_message(message.channel,"{}\n Added: \n{}".format(everyone.mention,message.author.mention))

            if "start" in message.content.lower():
                Servers[server.id].channel = message.channel
                if len(Servers[server.id].players) < 2:
                    await client.send_message(Servers[server.id].channel, "+-------------------------------------+")
                    await client.send_message(Servers[server.id].channel, "Too few players: join with 'c! join'")
                else:
                    await changeStatus("Playing Cards Against Humanity!")
                    await client.send_message(Servers[server.id].channel, """
                    +-------------------------------------+
                Starting game with:
                    """)

                    for i in Servers[message.server.id].players:
                            await client.send_message(Servers[message.server.id].channel,i.mention)

                    Servers[message.server.id].start_Game()
                    while True:
                        await client.send_message(message.channel, """+-------------------------------------+
                                        Do you want to:_?
                                               1: Start a new round
                                               2: Leader board
                                               3: Exit
                                     """)

                        b = False

                        response = await client.wait_for_message(channel=Servers[message.server.id].channel, check=lambda x: int(x.content) in range(4) if len(x.content)<2 else False)

                        if "1" in response.content:
                                await Servers[message.server.id].game.round(client, Servers[message.server.id].channel)
                                b = False
                        elif "2" in response.content:
                                await client.send_message(Servers[message.server.id].channel,
                                                          "+-------------------------------------+")
                                for i in Servers[message.server.id].game.players:
                                    await client.send_message(Servers[message.server.id].channel, "{}:{}".format(i.mention,
                                                                                                                 Servers[
                                                                                                                     message.server.id].game.players[
                                                                                                                     i].points
                                                                                                                 )
                                                      )
                                b = False
                        elif "3" in response.content:
                                await client.send_message(message.channel, "[-] Exiting!")
                                Servers[message.server.id].players = []
                                Servers[message.server.id].game = ""
                                with open("servers.bak", "r") as file:
                                    pickle.dumps(Servers, file)
                                b = True
                        else:
                                await client.send_message(message.channel, "[-] Baad Option!")
                                b = False
                        if b:
                                break
                        else:
                                continue

            if "reboot" in message.content.lower():
                if message.author in Masters:
                    subprocess.Popen("Python3.6","./Main.py")
                    exit()

            if "card" in message.content.lower():
                out = """
                       +-------------------------------------+
                       Current Card:
                            {}
                            Pick {}
                       """.format(Servers[message.server.id].game.currentCard["text"], Servers[message.server.id].game.currentCard["pick"])
                await client.send_message(Servers[message.server.id].channel, out)

client.run("NDA1MDkwOTg1NTA1MzI1MDY3.DUnXSg.Yn029C23MR-VS1qI11J1jfPU8yU")