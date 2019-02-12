import uuid

class Round:
    uuid = None
    gameid = None # uuid of the game this belongs to
    number = -1 # the number round this one was during the game
    placements = {} # json of player placements, where each entry is a playername and position in the tier

    def __init__(self, gameid, number, placements):
        self.uuid = str(uuid.uuid4())
        self.gameid = gameid
        self.number = number
        self.placements = placements
