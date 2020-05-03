class Singleton(type):
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Table():
    
    def __init__(self, players):
        self.players = players
    
class GameInstance(metaclass=Singleton):
    
    def __init__(self):
        self.waiting = []
        self.tables = {}

    def clearWaiting(self):
        self.waiting = []

    def addWaiting(self, name):
        for t in self.tables:
            if name in table.players:
                return 1
        self.waiting.append(name)
        return 0

    def removeWaiting(self, name):
        if name in self.waiting:
            self.waiting.remove(name)
