import discord, os
from discord.ext import commands
from functions import *
import requests, sys, re
import xml.etree.ElementTree as ET
import copy
import urllib

if len(sys.argv) > 1:
    TOKEN = os.environ["DISCORD_DEV_TOKEN"]
    ROOM_KEY = os.environ["TENHOU_DEV_KEY"]
else:
    TOKEN = os.environ["DISCORD_TOKEN"]
    ROOM_KEY = os.environ["TENHOU_KEY"]


bot = commands.Bot("!")
gi = GameInstance()


@bot.command()
async def start(ctx, p1=None, p2=None, p3=None, p4=None):
    """
    Start fishing
    Args:
        player1 player2 player3 player3
    """

    player = ctx.author
    chan = ctx.channel

    if (p1 == None or p2 == None or p3 == None or p4 == None):
        await chan.send(f"Please specify 4 players space separated")
        return

    player_names = [p1,p2,p3,p4]
    data = {
        "L":ROOM_KEY,
        "R2":"0209",
        "RND":"default",
        "WG":"1",
        "M":"\r\n".join(player_names)
    }
    resp = requests.post('https://tenhou.net/cs/edit/start.cgi',data=data)
    if resp.status_code != 200:
        await chan.send(f"http error {resp.status_code} :<")
        return
    await chan.send(urllib.parse.unquote("&".join(resp.url.split("&")[1:])))




@bot.command()
async def ping(ctx):
    """
    Join a list to wait for fishing!
    """

    player = ctx.author
    chan = ctx.channel
    await chan.send(f"pong")


@bot.command()
async def join(ctx):
    """
    Join a list to wait for fishing!
    """

    player = ctx.author
    chan = ctx.channel

    ret = gi.addWaiting(player)
    if ret != 0:
        await chan.send(gi.lastError)
        return
    await chan.send(f"{player} joined the waiting to fish list!")


@bot.command()
async def leave(ctx):
    """
    Leave the waiting to fish list :(
    """

    player = ctx.author
    chan = ctx.channel

    ret = gi.removeWaiting(player)
    if ret != 0:
        await chan.send(gi.lastError)
        return
    await chan.send(f"{player} left the waiting to fish list!")


@bot.command()
async def clear(ctx):
    """
    Clear waiting to fish list
    """
    
    player = ctx.author
    chan = ctx.channel
    
    gi.reset()
    await chan.send(f"Cleared!")

@bot.command()
async def shuffle(ctx):
    """
    Assign fishers to docks!
    """
    player = ctx.author
    chan = ctx.channel
    
    tableD = gi.shuffle()

    
    if tableD == {}:
        await chan.send("Not docks could be made!")
    else:
        ret = ""
        for table in tableD:
            ret += f"Dock {table}:\n"
            for player in tableD[table]:
                ret += "  "+str(player)+"\n"
            ret += "\n"
        await chan.send(ret)

    
@bot.command()
async def list(ctx):
    """
    Show who is looking to fish!
    """

    player = ctx.author
    chan = ctx.channel

    ret = ""

    if gi.waiting == []:
        await chan.send("Currently no one is waiting to fish")
    else:
        for p in gi.waiting:
            ret += str(p) + "\n"
        await chan.send(ret)


@bot.command()
async def explain(ctx):
    """
    Explain how the last scoring was calculated
    """

    player = ctx.author
    chan = ctx.channel

    if(gi.lastScore == ""):
        await chan.send("Nothing has been scored yet")
        return
    await player.send(gi.lastScore)
    
@bot.command()
async def score(ctx, log=None, rate="tensan", shugi=None):
    """
    Score a fishing log! (Results in cm)
    Args:
        log:
            A full url or just the log id
        rate (optional):
            tensan(default), tengo, or tenpin
        shugi (optional):
            defaults to the rate shugi
    """

    
    player = ctx.author
    chan = ctx.channel

    if log == None or rate == None:
        await chan.send("usage: !score [tenhou_log] [rate]\nEx: !score https://tenhou.net/0/?log=2020051313gm-0209-19713-10df4ad2&tw=1 tengo")
        
    
    table = [["Score","","Pay","Name"]]

    rate = rate.lower()
    tableRate = None
    
    if rate == "tensan" or rate == "0.3" or rate == ".3":
        tableRate = copy.deepcopy(TENSAN)
    elif rate == "tengo" or rate == "0.5" or rate == ".5":
        tableRate = copy.deepcopy(TENGO)
    elif rate == "tenpin" or rate == "1.0":
        tableRate = copy.deepcopy(TENPIN)
    else:
        await chan.send(f"{rate} is not a valid rate (try !help score)")
        return

    if(shugi != None):
        try:
            tableRate.shugi = round(float(shugi),3)
        except:
            await chan.send(f"{shugi} is not a valid shugi")
            return
        
    players = gi.parseGame(log, tableRate)

        
    for p in players:
        score = str(p.score)
        shugi = str(p.shugi)
        payout = str(p.payout)
        #if not "-" in score:
        #    score = "+"+score
        if not "-" in shugi:
            shugi = "+"+shugi
        if not "-" in payout:
            payout = "+"+payout       
        table.append([str(score),str(shugi),str(payout),str(p.name)])

    colMax = [max([len(i) for i in c]) for c in zip(*table)]
    colMax[-1] = 0
    
    ret = f"```{tableRate}\n"
    for row in table:
        for i,col in enumerate(colMax):
            ret += row[i].ljust(col+1)
        ret += "\n"
    ret += "```"
    await chan.send(ret)
    
@bot.event
async def on_ready():
    print("Time to fish!")
    print("Logged in as: {}".format(bot.user.name))

@bot.event
async def on_error(event, *args, **kwargs):
    print("ERROR!")
    print("Error from:", event)
    print("Error context:", args, kwargs)

    from sys import exc_info

    exc_type, value, traceback = exc_info()
    print("Exception type:", exc_type)
    print("Exception value:", value)
    print("Exception traceback object:", traceback)

    
bot.run(TOKEN)
