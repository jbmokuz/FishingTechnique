import random

MAX_PLAYERS = 2 # WARNING NEVER EVER SET TO 3!

class Singleton(type):
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

"""
class Player():

    def __init__(self, name):
        self.name = name
        self.rates = []

    def addRate(self,r):
        self.rates.append(r)
        
    def removeRate(self,r):
        self.rates.remove(r)

    def __str__(self):
        return self.name

    def __eq__(self, other):
        self.name == other.name

    def __hash__(self):
        return id(self)        
"""

"""
class Rate():
    
    def __init__(self, rate=0.3, shugi=1):
        self.rate = rate
        self.shugi = shugi
        
    def __eq__(self, other):
        return (self.rate == other.rate and self.shugi == other.shugi)
"""     
    
class Table():
    
    def __init__(self, players=[], rate=0.3, shugi=.50, oka=20000, target=30000, start=25000, uma=[30,10,-10,-30]):
        
        self.players = {}
        self.rate = rate
        
        self.shugi = shugi        
        self.oka = oka
        self.target = target
        self.start = start
        self.uma = uma
        self.uma.sort()
        self.uma = self.uma[::-1]

        # @TODO Check that uma = 0 and is ok for max players
        
        for p in players:
            self.players[p] = None

    def __str__(self):
        ret = f"""
        players: {self.players.keys()}
        rate: {self.rate}
        target: {self.target}
        start: {self.start}
        shugi: {self.shugi}
        oka: {self.oka}
        uma: {self.uma}
        """
        return ret

            
class GameInstance(metaclass=Singleton):
    
    def __init__(self):
        self.waiting = []
        self.tables = {}
        self.players_d = {}

    def reset(self):
        self.waiting = []
        self.tables = {}
        self.players_d = {}

    # This is used to get the table a player is playing at
    def getTableName(self, name):
        for t in self.tables:
            if name in self.tables[t].players:
                    return t
        return None

    # Add a player to a table/waiting
    def addTable(self, name, table=None):

        # This adds the player to waiting 
        if table == None:
            return self.addWaiting(name)

        # The player is already at a table!
        elif self.getTableName(name) != None:
            return 3

        # Add the player to a table
        else:
            # Make the table if it is not one already
            if not table in self.tables:
                self.tables[table] = Table()

            # There are already 4 players at this table
            if len(self.tables[table].players) >= MAX_PLAYERS:
                return 4

            # The None is to track the result
            if not name in self.tables[table].players:
                self.tables[table].players[name] = None
        return 0

    # Not to be used yet!
    def addWaiting(self, name):
        for t in self.tables:
            if name in self.tables[t]:
                return 1
        if name in self.waiting:
            return 2
        self.waiting.append(name)
        #if not name in self.players_d:
        #    self.players_d[name] = Player(name)
        return 0
                
    def remove(self, name):
        if name in self.waiting:
            self.removeWaiting(name)
            return 0
        ret = self.getTableName(name)
        if ret == None:
            return 1
        del(self.tables[ret].players[name])
        if self.tables[ret].players == {}:
            del(self.tables[ret])
        return 0
    
    # Not to be used yet!
    def removeWaiting(self, name):
        if name in self.waiting:
            self.waiting.remove(name)

    # Not to be used yet!
    def shuffle(self):
        ret = []
        rate_table = []
        
        #@TODO check to see if rate is the same for players
        
        if len(self.waiting) >= MAX_PLAYERS:
            random.shuffle(self.waiting)
            while(len(self.waiting) >= MAX_PLAYERS):
                count = 0
                while(count in self.tables.keys()):
                    count += 1
                self.tables[count] = Table(self.waiting[:MAX_PLAYERS])
                self.waiting = self.waiting[MAX_PLAYERS:]
                ret.append(count)
        return ret

    def listPlaying(self):
        ret = []
        for t in self.tables:
            ret.append(self.tables[t])
        return ret

    def checkScores(self, table):
        for p in table.players:
            if table.players[p] == None:
                return False
        return True


    #   Score   Oka     Target      Uma  Rate
    # ((60000 + 20000 - 30000)/1000)+30)*30
    def report(self, name, score):
        t = self.getTableName(name)
        if t != None:
            table = self.tables[t]
            score = ' '.join(score.strip().split()).split(" ")
            try:
                score[0] = int(score[0])
                score[1] = int(score[1])
            except:
                return 2
            table.players[name] = score
            if self.checkScores(table):
                return 0
        return 1
        

    def scoreTable(self, tableName, verbose=False):
        # Get the table
        if not tableName in self.tables:
            return f"{tableName} is not a table!"

        table = self.tables[tableName]
        
        if len(table.players) != MAX_PLAYERS:
            return f"{len(table.players)} is not the correct number of players"
        
        for p in table.players:
            if table.players[p] == None:
                return f"{p} does not have a score reported"

        scoreList = []

        # Make all the scores and player info into a list
        for player in table.players:
            if table.players[player] == None:
                return "Not all scores reported!"
            scoreList.append([player]+table.players[player])

        # Check that the scores sum properly
        if sum([i[1] for i in scoreList]) != table.start*MAX_PLAYERS:
            return "Score does not sum to "+ str(table.start*MAX_PLAYERS)

        # Check that the shugi sums properly
        if sum([i[2] for i in scoreList]) != 0:
            return "Shugi does not sum to 0"
            

        scoreList.sort(key=lambda x: x[1])
        scoreList = scoreList[::-1]

        # Show table rules
        if verbose:        
            print("TABLE",tableName,str(table))
        
        ret = ""
        ret += f"Score for table {tableName}:\n"
        player, score, shugi  = scoreList[0]
        oka = table.oka

        for i, j in enumerate(scoreList):
            player, score, shugi  = j            
            calc = ((((score+oka-table.target)/1000)+table.uma[i])*(table.rate*10)+(table.shugi*(shugi*10)))/10
            if verbose:
                ret += f"    (((({score}+{oka}-{table.target})/1000)+{table.uma[i]})×({table.rate}×10)+({table.shugi}×{shugi}×10))/10\n"
            ret += f"    {player}: {calc}\n"
            oka = 0
        return ret
