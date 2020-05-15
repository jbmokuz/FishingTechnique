import discord, os
from discord.ext import commands
from functions import *
import requests, sys
import xml.etree.ElementTree as ET

TOKEN = os.environ["DISCORD_TOKEN"]

bot = commands.Bot("!")
gi = GameInstance()


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
    Assign fishers to piers!
    """
    player = ctx.author
    chan = ctx.channel
    
    tableD = gi.shuffle()

    
    if tableD == {}:
        await chan.send("Not piers could be made!")
    else:
        ret = ""
        for table in tableD:
            ret += f"Pier {table}:\n"
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
async def score(ctx, log=None, rate="tensan"):
    """
    Score a fishing log! (Results in cm)
    Args:
        log:
            A full url or just the log id
        rate (optional):
            tensan(default), tengo, or tenpin
    """

    
    player = ctx.author
    chan = ctx.channel

    if log == None or rate == None:
        await chan.send("usage: !score [tenhou_log] [rate]\nEx: !score https://tenhou.net/0/?log=2020051313gm-0209-19713-10df4ad2&tw=1 tengo")
        
    
    table = [["Score","","Pay","Name"]]

    rate = rate.lower()
    if rate == "tensan" or rate == "0.3" or rate == ".3":
        players = parseGame(log, TENSAN)
    elif rate == "tengo" or rate == "0.5" or rate == ".5":
        players = parseGame(log, TENGO)
    elif rate == "tenpin" or rate == "1.0":
        players = parseGame(log, TENPIN)
    
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
    ret = "```\n"
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
