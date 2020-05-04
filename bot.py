import discord, os
from discord.ext import commands
from functions import GameInstance
from functions import MAX_PLAYERS
from functions import TENGO,TENSAN,TENPIN

TOKEN = os.environ["DISCORD_TOKEN"]

bot = commands.Bot("!")
gi = GameInstance()

@bot.command()
async def join(ctx, table=None):
    """
    Join a pier to fish at!
    Args:
        pier:
            The name of the pier you want to join
    """
    
    player = ctx.author
    chan = ctx.channel

    if table == None:
        await chan.send("usage: !join [table]\nEx: !join tableA")
        return
    
    ret = gi.addTable(player, table)
    if ret != 0:
        await chan.send(gi.lastError)
        return
    await chan.send(f"{player} joined table {table}")    


@bot.command()
async def leave(ctx):
    """
    Leave a pier!
    """

    player = ctx.author
    chan = ctx.channel

    ret = gi.remove(player)
    if ret != 0:
        await chan.send(gi.lastError)
        return
    await chan.send(f"{player} left!")


@bot.command()
async def list(ctx):
    """
    Show who is fishing!
    """

    player = ctx.author
    chan = ctx.channel

    ret = ""

    for t in gi.tables:
        ret += "Table "+t+":\n"
        ret += str(gi.tables[t]) + "\n"
        ret += "  Players:\n"
        for p in gi.tables[t].players:
            
            ret += "    "+str(p)+"\n"
        ret += "\n"
    if ret == "":
        await chan.send("Currently no one is fishing")
    else:
        await chan.send(ret)

@bot.command()
async def set_rate(ctx, table=None, rate=None):
    """
    Change rate of a table
    Args:
        Table: 
          Name of table
        Rate:
          Current acceptable rates [tensan, tengo, tenpin]
    """
    
    player = ctx.author
    chan = ctx.channel
    
    if table == None or rate == None:
        await chan.send("usage: !set_rate [table] [rate]\nEx: !set_rate tableA tengo")
        return
    
    rate = rate.lower()
    if rate == "tensan":
        ret = gi.setTableRate(table, TENSAN)
    elif rate == "tengo":
        ret = gi.setTableRate(table, TENGO)
    elif rate == "tenpin":
        ret = gi.setTableRate(table, TENPIN)
    else:
         await chan.send(f"{rate} is not a valid rate")
         return

    if ret != 0:
        await chan.send(gi.lastError)
        return
    await chan.send(f"{table} rate changed!")         
        
        
        
@bot.command()
async def report(ctx, score=None, shugi=None):
    """
    Report your catch!
    Args:
        Score:
            How big your fish is
        Shugi:
            How many fish you caught???
    """

    player = ctx.author
    chan = ctx.channel

    if score == None or shugi == None:
        await chan.send("Not a properly formatted score!\nExample !report 35000 +2")
        return
    
    
    ret = gi.report(player, score+" "+shugi)
    if ret != 0:
        await chan.send(gi.lastError)
        return
    await chan.send("Score reported")
    
@bot.command()
async def score(ctx, table, verbose=None):
    """
    See how big your fish are (results in cm)!
    Args:
        Table:
            The table you want to score
    """

    player = ctx.author
    chan = ctx.channel

    if verbose != None:
        ret = gi.scoreTable(table,True)
    else:
        ret = gi.scoreTable(table)        

    if ret == 1:
        await chan.send(gi.lastError)
        return
    await chan.send(f"{ret}")
    
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
