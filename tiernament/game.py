import time, uuid
from .round import Round

def rowToGame(row):
    # TODO: Serialize a given database Row to a Game object
    uuid = None
    name = None
    time = 0
    game = None
    tier = None
    players = []
    rounds = 0
    params = []

    return -1

class Game:
    uuid = None
    name = None # custom name for the game
    time = 0 # time the game started, in seconds since epoch
    game = None # name for the game being played
    tier = None # the actual tier we will use
    players = []
    rounds = 0
    params = []

    def __init__(self, name, game, tier, players, params=None):
        # TODO: Potentially shorten uuid for readability
        self.uuid = str(uuid.uuid4())
        self.name = name
        self.time = time.time()
        self.game = game
        self.tier = None
        self.players = []
        self.rounds = 0 # TODO: might want to change later, but just init all games to 0
        # TODO: maybe a deleted player list? (someone left the game)
        self.params = params

    def startGame(self):
        # TODO: probably enter a round 0, where everyone is at (0,0,0,0)...etc
        round0 = Round(gameid=uuid, number=0, placements=[0,0,0,0])
        return -1

    # Updates the game after a round has been played 
    def updateGameAferRound(self, newRound):
        # self.rounds.append(newRound)
        return -1

    # Gets the player currently placed at the specified position in the game
    def getPlayerAtPlacement(self, position):
        return -1

    def addPlayer(self, player):
        # TODO: update db as well
        self.players.append(player)

    # Deletes the most recent round played, in case of accidental entries
    def undoRound(self):
        # TODO: also delete round from db
        #self.rounds.pop()
        return -1

    def getUUID(self):
        return self.uuid

    def getName(self):
        return self.name

    def getTime(self):
        return self.time

    def getGame(self):
        return self.game

    def getTier(self):
        return self.tier

    def getNumRounds(self):
        return self.rounds

