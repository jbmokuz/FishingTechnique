import random
import requests
import xml.etree.ElementTree as ET

class Singleton(type):
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Player():
    def __init__(self):
        self.name = None
        self.score = None
        self.shugi = None
        self.payout = None
        self.calc = ""

    def __str__(self):
        return f"{self.name} {self.score} {self.shugi} {self.payout}"



class GameInstance(metaclass=Singleton):
    
    def __init__(self):
        self.MAX_PLAYERS = 4 # WARNING NEVER EVER SET TO 3!
        self.waiting = []
        self.pWaiting = [] # Priority waiting
        self.lastError = ""

    def reset(self):
        self.waiting = []
        self.pWaiting = []         
        self.lastError = ""
        
    def addWaiting(self, name):
        if name in self.waiting or name in self.pWaiting:
            self.lastError = f"{name} is already waiting"
            return 1
        self.waiting.append(name)
        return 0
        
    def removeWaiting(self, name):
        if name in self.waiting or name in self.pWaiting:
            self.waiting.remove(name)
            return 0
        self.lastError = f"{name} is not currently waiting"
        return 1

    def shuffle(self):
        ret = {}        
        if len(self.waiting) >= self.MAX_PLAYERS:
            random.shuffle(self.waiting)
            while(len(self.waiting) >= self.MAX_PLAYERS):
                count = 0
                while(count in ret.keys()):
                    count += 1
                if not count in ret:
                    ret[count] = []
                for i in range(self.MAX_PLAYERS):
                    ret[count].append(self.waiting.pop())
        return ret


class TableRate():
    
    def __init__(self, rate=0.3, shugi=.50, target=30000, start=25000, uma=[30,10,-10,-30]):
        self.rate = rate     
        self.shugi = shugi        
        self.oka = (target - start) * 4
        self.target = target
        self.start = start
        self.uma = uma        
        
    def __eq__(self, other):
        return (self.rate == other.rate and self.shugi == other.shugi and self.oka == other.oka and self.target == other.target and self.start == other.start and self.uma == other.uma)

    def __str__(self):
        return f"Rate: {self.rate}, Start: {self.start}, Target: {self.target}, Shugi: {self.shugi}, Oka: {self.oka}, Uma: {self.uma}"

# default values rate=0.3, shugi=.50, target=30000, start=25000, uma=[30,10,-10,-30]    
TENSAN = TableRate()
TENGO = TableRate(rate=0.5, shugi=1)
TENPIN = TableRate(rate=1, shugi=2)

def parseGame(log, rate=TENSAN):

    if "https://" in log.lower() or "http://" in log.lower():
        log = log.split("=")[1].split("&")[0]
    xml = requests.get("http://tenhou.net/0/log/?"+log).text
    print("Prasing http://tenhou.net/0/log/?"+log)

    def convertToName(s):
        ret = bytes()
        for c in s.split("%")[1:]:
            ret +=  int(c,16).to_bytes(1,"little")
        return ret.decode("utf-8")

    players = [Player() for i in range(4)]

    root = ET.fromstring(xml)

    type_tag = root.find('UN')
    players[0].name = convertToName(type_tag.get('n0'))
    players[1].name = convertToName(type_tag.get('n1'))
    players[2].name = convertToName(type_tag.get('n2'))
    players[3].name = convertToName(type_tag.get('n3'))

    for type_tag in root.findall('AGARI'):
        owari = type_tag.get("owari")
        if owari == None:
            continue
        owari = owari.split(",")
        # @TODO check if there is shugi
        if len(owari) >= 8:
            owari += [0,0,0,0,0,0,0,0]
        for i in range(0,4):
            players[i].score = int(owari[i*2])*100
            players[i].shugi = int(owari[i*2+8])
        break

    return scoreTable(players, rate)

def scoreTable(players, tableRate):
    
    players.sort(key=lambda x: x.score,reverse=True)

    oka = [tableRate.oka,0,0,0] # giving 1st place oka bonus
    
    for i, p in enumerate(players):
        shugi = tableRate.shugi * p.shugi
        calc = (((p.score + oka[i] - tableRate.target)/1000) + tableRate.uma[i]) * tableRate.rate + shugi
        p.payout = round(calc,2)
        #p.calc = f"(((({p.score}+{oka}-{tableRate.target})/1000)+{tableRate.uma[i]})×({tableRate.rate}×10)+({tableRate.shugi}×{p.shugi}×10))/10\n"
        
    return players


