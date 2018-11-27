import uuid

class Round:
    uuid = None
    gameid = None # uuid of the game this belongs to
    number = -1 # the number round this one was during the game
    placements = [] # array of player placements, ordered from first to last

    def __init__(self, gameid, number, placements):
        self.uuid = str(uuid.uuid4())
        self.gameid = gameid
        self.number = number
        self.placements = placements
