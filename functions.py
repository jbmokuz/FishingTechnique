import random
import requests
import xml.etree.ElementTree as ET

class Player():
    def __init__(self):
        self.name = None
        self.score = None
        self.shugi = None
        self.payout = None
        self.calc = ""

    def __str__(self):
        return self.name+ " " + str(self.score) + " " + str(self.shugi)+ " "+str(self.payout)

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

TENSAN = TableRate(rate=0.3, shugi=.50, target=30000, start=25000, uma=[30,10,-10,-30])
TENGO = TableRate(rate=0.5, shugi=1, target=30000, start=25000, uma=[30,10,-10,-30])
TENPIN = TableRate(rate=1, shugi=2, target=30000, start=25000, uma=[30,10,-10,-30])

def parseGame(log, rate=TENSAN):
    xml = requests.get("http://tenhou.net/0/log/?"+log).text

    def convertToName(s):
        ret = bytes()
        for c in s.split("%")[1:]:
            ret +=  int(c,16).to_bytes(1,"little")
        return ret.decode("utf-8")

    players = [Player() for i in range(4)]

    root = ET.fromstring(xml)
    for type_tag in root.findall('UN'):
        players[0].name = convertToName(type_tag.get('n0'))
        players[1].name = convertToName(type_tag.get('n1'))
        players[2].name = convertToName(type_tag.get('n2'))
        players[3].name = convertToName(type_tag.get('n3'))

    for type_tag in root.findall('AGARI'):
        owari = type_tag.get("owari")
        if owari == None:
            continue
        owari = owari.split(",")        
        for i in range(0,4):
            players[i].score = int(owari[i*2])*100
            players[i].shugi = int(owari[i*2+8])

    return scoreTable(players, rate)

def scoreTable(players, tableRate):
    
    ret = ""
    players.sort(key=lambda x: x.score,reverse=True)

    players[0].score += tableRate.oka # giving 1st place oka bonus
    
    for i, p in enumerate(players):
        shugi = tableRate.shugi * p.shugi
        endScore = ((p.score - tableRate.target)/1000) + tableRate.uma[i]
        calc =  endScore * tableRate.rate + shugi
        p.payout = round(calc,2)
        ret += f"{p.name}: {p.payout}\n"
        
    return players


