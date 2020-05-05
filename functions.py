import random

MAX_PLAYERS = 4 # WARNING NEVER EVER SET TO 3!

class Singleton(type):
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class TableRate():
    
    def __init__(self, rate=0.3, shugi=.50, target=30000, start=25000, uma=[30,10,-10,-30]):
        self.rate = rate     
        self.shugi = shugi        
        self.oka = (target - start) * MAX_PLAYERS
        self.target = target
        self.start = start
        self.uma = uma        
        
    def __eq__(self, other):
        return (self.rate == other.rate and self.shugi == other.shugi and self.oka == other.oka and self.target == other.target and self.start == other.start and self.uma == other.uma)

    def __str__(self):
        return f"Rate: {self.rate}, Start: {self.start}, Target: {self.target}, Shugi: {self.shugi}, Oka: {self.oka}, Uma: {self.uma}"

TENSAN = TableRate(rate=0.3, shugi=.50, target=30000, start=25000, uma=[30,10,-10,-30])
TENGO = TableRate(rate=0.5, shugi=1, target=30000, start=25000, uma=[30,10,-10,-30])
TENPIN = TableRate(rate=1, shugi=2, target=30000, start=25000, uma=[30,10,-10,-30])

class Table():
    
    def __init__(self, players=[], tableRate=TENSAN):
        self.players = {}        
        self.tableRate = tableRate

        for p in players:
            self.players[p] = None

    def __str__(self):
        ret = f"""    rate: {self.tableRate.rate}, start: {self.tableRate.start}, target: {self.tableRate.target},
    shugi: {self.tableRate.shugi}, oka: {self.tableRate.oka}, uma: {self.tableRate.uma}"""
        return ret

            
class GameInstance(metaclass=Singleton):
    
    def __init__(self):
        self.waiting = []
        self.tables = {}
        self.players_d = {}
        self.lastError = ""

    def reset(self):
        self.waiting = []
        self.tables = {}
        self.players_d = {}
        self.lastError = ""

    # This is used to get the table a player is playing at
    def getTableName(self, name):
        for t in self.tables:
            if name in self.tables[t].players:
                    return t
        return None

    # Add a player to a table/waiting
    def addTable(self, name, table, rate=TENSAN):

        # The player is already at a table!
        if self.getTableName(name) != None:
            self.lastError = f"Player: {name} already at table: {self.getTableName(name)}"
            return 1

        # Add the player to a table
        else:
            # Make the table if it is not one already
            if not table in self.tables:
                self.tables[table] = Table(tableRate=rate)

            if rate != self.tables[table].tableRate:
                self.lastError = f"Rate missmatch\n Table: {self.tables[table].tableRate}\n New  : {rate}"
                return 1


            # There are already 4 players at this table
            if len(self.tables[table].players) >= MAX_PLAYERS:
                self.lastError = f"Already have {MAX_PLAYERS} at table"
                return 1

            # The None is to track the result
            if not name in self.tables[table].players:
                self.tables[table].players[name] = None
                
        return 0

    def remove(self, name):
        ret = self.getTableName(name)
        if ret == None:
            self.lastError = f"Player: {name} currently not at any table"
            return 1
        del(self.tables[ret].players[name])
        if self.tables[ret].players == {}:
            del(self.tables[ret])
        return 0
    
    def report(self, name, score):
        t = self.getTableName(name)
        if t != None:
            table = self.tables[t]
            score = ' '.join(score.strip().split()).split(" ")
            try:
                score[0] = int(score[0])
                score[1] = int(score[1])
            except:
                self.lastError = f"Invalid format {score}"
                return 1
            table.players[name] = score
            return 0
        self.lastError = f"Player: {name} is not currently at a table"
        return 1
        
    def setTableRate(self, tableName, rate):
        if not tableName in self.tables:
            self.lastError = f"{tableName} is not a table"
            return 1
        if type(rate) != type(TENSAN):
            self.lastError = f"Not a valid rate"
            return 1
        self.tables[tableName].tableRate = rate
        return 0
        
    def scoreTable(self, tableName, verbose=False):
        # Get the table
        if not tableName in self.tables:
            self.lastError = f"{tableName} is not a table"
            return 1

        table = self.tables[tableName]
        
        if len(table.players) != MAX_PLAYERS:
            self.lastError = f"{len(table.players)} is not the correct number of players"
            return 1

        scoreList = []


        # Make all the scores and player info into a list        
        for player in table.players:
            if table.players[player] == None:
                self.LastError = f"{player} does not have a score reported"
                return 1
            scoreList.append([player]+table.players[player])

        # Check that the scores sum properly
        if sum([i[1] for i in scoreList]) != table.tableRate.start*MAX_PLAYERS:
            self.lastError = "Score does not sum to "+ str(table.tableRate.start*MAX_PLAYERS)
            return 1

        # Check that the shugi sums properly
        if sum([i[2] for i in scoreList]) != 0:
            self.lastError =  "Shugi does not sum to 0"
            return 1
            
        scoreList.sort(key=lambda x: x[1])
        scoreList = scoreList[::-1]

        # Show table rules
        ret = ""
        if verbose:        
            ret += "TABLE"+" "+tableName+str(table)
        
        ret += f"Score for table {tableName}:\n"
        player, score, shugi  = scoreList[0]
        oka = table.tableRate.oka

        for i, j in enumerate(scoreList):
            player, score, shugi  = j            
            calc = ((((score+oka-table.tableRate.target)/1000)+table.tableRate.uma[i])*(table.tableRate.rate*10)+(table.tableRate.shugi*(shugi*10)))/10
            if verbose:
                ret += f"    (((({score}+{oka}-{table.tableRate.target})/1000)+{table.tableRate.uma[i]})×({table.tableRate.rate}×10)+({table.tableRate.shugi}×{shugi}×10))/10\n"
            ret += f"    {player}: {calc}\n"
            oka = 0
        return ret
