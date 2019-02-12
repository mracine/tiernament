import uuid

class Player:
    name = None
    icon = None
    color = None

    def __init__(self, name, icon=None, color=None):
        self.name = name
        self.icon = icon
        self.color = color

    def getPlayerName(self):
        return self.name

    def setPlayerName(self, name):
        self.name = name

    def getPlayerIcon(self):
        return self.icon

    def setPlayerIcon(self, icon):
        self.icon = icon

    def getPlayerColor(self):
        return self.color

    def setPlayerColor(self, color):
        self.color = color

