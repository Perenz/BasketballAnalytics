import pandas as pd
import sys

def printPlayers(statsDict):
    for player in statsDict:
        print(player)
        for column in statsDict[player]:
            print(column, ':', statsDict[player][column])

def checkErrs(playersDict):
    #Flag to memorize if an error occured
    error=False
    for player in playersDict:
        if int(playersDict[player]['2P'])>int(playersDict[player]['2PA']):
            error=True
            print(f'Error: Player number {playersDict[player]["Num"]} can\'t make more 2 points shot than attempts')
        if int(playersDict[player]['3P'])>int(playersDict[player]['3PA']):
            error = True
            print(f'Error: Player number {playersDict[player]["Num"]} can\'t make more 3 points shot than attempts')
        if int(playersDict[player]['FT'])>int(playersDict[player]['FTA']):
            error = True
            print(f'Error: Player number {playersDict[player]["Num"]} can\'t make more free throw than attempts')
        if error: print('\n')

    sys.exit("Errors in GameStatSheet must be solved before one can continue") if error \
        else print("No errors encountered, GameStatSheet can be computed")
'''
A simple script to check some error in GameStatSheet
Error's kinds:
    - More Shot made than shot attempted (2P/2PA, 3P/3PA, FT/FTA)
    Correctness in 2p and 3p implies correctness in fg
'''

statsDF = pd.read_excel('fogliExcel/GameStatSheet.xlsx')

statsDF.fillna(0, inplace=True)

statsDict = statsDF.to_dict(orient="index")

# printPlayers(statsDict)

checkErrs(statsDict)
