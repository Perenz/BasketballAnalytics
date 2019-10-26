import pandas as pd

'''
class Player:
    columnsNameList = list()

    def __init__(self, gameStats):
        self.playerGameStats = gameStats


    def __str__(self):
        toRtn = ""
        for column in Player.columnsNameList:
            toRtn += str(column) + ": " + str(self.playerGameStats[column]) + "\n"
        toRtn += "\n\n"
        return toRtn


def importPlayers(players):
    playersList = pd.read_excel("GameStatSheet.xlsx", sheet_name="Giocatori")

    # Create a list with columns names
    columnsNameArray = playersList.columns.values
    Player.columnsNameList = list(columnsNameArray)

    playersList.fillna(0, inplace=True)
    for index, row in playersList.iterrows():
        playerGameStats = dict()
        for column in Player.columnsNameList:
            # print(str(column) + " " + str(row[column]))
            playerGameStats[column] = row[column]

        # Salvo i giocatori estratti, con le proprie stats, nel dizionario dei giocatori
        players[row['Num']] = Player(playerGameStats)
        # print(players[row['Num']])

        # Ogni giocatore dalla singola partita va memorizzato, con le proprie stat e poi sommato alle stat generali
'''


def computeCombStats(players):
    eFG = list()
    TSPerc= list()
    AstPerc=list()
    calcoloTeamStatsBase(players)
    for index, row in players.iterrows():

            players.at[index, 'TRB'] = players.at[index, 'DRB']+players.at[index, 'ORB']

            # Compute total rebounds
            players.at[index, 'TRB'] = players.at[index, 'DRB']+players.at[index, 'ORB']

            # Compute total points
            players.at[index, 'PTS'] = players.at[index, '2P']*2 + players.at[index, '3P']*3 + players.at[index, 'FT']

            # Sum total field goals
            players.at[index, 'FG'] = players.at[index, '2P'] + players.at[index, '3P']
            players.at[index, 'FGA'] = players.at[index, '2PA'] + players.at[index, '3PA']

            # Compute percentages%
            players.at[index, 'FG%'] = players.at[index, 'FG'] / players.at[index, 'FGA'] \
                if players.at[index, 'FGA'] > 0 else 0

            players.at[index, '2P%'] = players.at[index, '2P'] / players.at[index, '2PA'] \
                if players.at[index, '2PA'] > 0 else 0

            players.at[index, '3P%'] = players.at[index, '3P'] / players.at[index, '3PA'] \
                if players.at[index, '3PA'] > 0 else 0

            players.at[index, 'FT%'] = players.at[index, 'FT'] / players.at[index, 'FTA'] \
                if players.at[index, 'FTA'] > 0 else 0

            eFG.append((players.at[index, 'FG'] + 0.5*players.at[index, '3P'])/players.at[index, 'FGA'])
            TSPerc.append(players.at[index, 'PTS'] / (2*(players.at[index, 'FGA']+0.44*players.at[index, 'FTA'])))

            # AST% Formula: 100 * AST / (((MP / (Tm MP / 5)) * Tm FG) - FG)
            AstPerc.append(100*players.at[index, 'AST']/((players.at[index, 'MP']/(players.at['Team', 'MP']/5)) * players.at['Team', 'FG'])-players.at[index, 'FG'])

    players['AST%'] = AstPerc
    players['eFG%'] = eFG
    players['TS%'] = TSPerc


def printPlayers(statsDict):
    for player in statsDict:
        print(player)
        for column in statsDict[player]:
            print(column, ':', statsDict[player][column])


def calcoloTeamStatsBase(players):
    index = 'Team'

    players.at[index, 'TRB'] = players.at[index, 'DRB'] + players.at[index, 'ORB']

    # Compute total rebounds
    players.at[index, 'TRB'] = players.at[index, 'DRB'] + players.at[index, 'ORB']

    # Compute total points
    players.at[index, 'PTS'] = players.at[index, '2P'] * 2 + players.at[index, '3P'] * 3 + players.at[index, 'FT']

    # Sum total field goals
    players.at[index, 'FG'] = players.at[index, '2P'] + players.at[index, '3P']
    players.at[index, 'FGA'] = players.at[index, '2PA'] + players.at[index, '3PA']

    # Compute percentages%
    players.at[index, 'FG%'] = players.at[index, 'FG'] / players.at[index, 'FGA'] \
        if players.at[index, 'FGA'] > 0 else 0

    players.at[index, '2P%'] = players.at[index, '2P'] / players.at[index, '2PA'] \
        if players.at[index, '2PA'] > 0 else 0

    players.at[index, '3P%'] = players.at[index, '3P'] / players.at[index, '3PA'] \
        if players.at[index, '3PA'] > 0 else 0

    players.at[index, 'FT%'] = players.at[index, 'FT'] / players.at[index, 'FTA'] \
        if players.at[index, 'FTA'] > 0 else 0


statsDf = pd.read_excel("fogliExcel/GameStatSheet.xlsx")

# Calculate total team stats
statsDf.loc["Team"] = statsDf.sum(numeric_only=True)
statsDf.at['Team', 'Num'] = 0
statsDf.at['Team', 'Nome'] = "Team"
statsDf.at['Team', 'Cognome'] = "Team"


statsDf.fillna(0, inplace=True)

# statsDict = statsDf.to_dict(orient="index")
# From now on i can edit che dict statsDict

# for num in players:
    # print(players[num])

'''
printPlayers(statsDict)
'''

computeCombStats(statsDf)

# statsDf = pd.DataFrame.from_dict(statsDict, orient="index")
print(statsDf)
statsDf.to_excel("fogliExcel/GameStatSheetComputed.xlsx", engine='xlsxwriter')
# Calcolo delle stats combinate:
    # FG%, 3P%, FT%, TRB