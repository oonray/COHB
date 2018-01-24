"""
By Alexander Bjørnsrud
Aka The Bot Master

This is a Cards against humanity clone made in python.
Thanks to Ranadom person on the internett for submitting the cards in json format.
"""




"""
The Game Class 
"""
from Game import Game

game = Game(["Alexander","Knut"])

"""
Starting the initial Menu
"""
while True:
    out = """
    Choose Action:
        1 New Round
        2 Leaderboard
        3 Exit
    """
    print(out)
    choice = input(">")

    """
    Splits the choice so that if the user inputs more than one number only the first is regarded
    Checks the input and acts accordingly.
    Memo could use regex ^\d [0] 
    """
    if int(choice.split()[0]) == 1:
        game.round()
    elif int(choice.split()[0]) == 2:
        for i in game.players:
            print("Player {} has {} points".format(game.players[i].name,game.players[i].points))
    else:
        exit()


