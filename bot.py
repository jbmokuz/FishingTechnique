import discord, os
from discord.ext import commands
from functions import GameInstance
from functions import MAX_PLAYERS

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

    ret = gi.addTable(player, table)

    if table == None:
        await chan.send("Please pick a table name")

    if ret == 0:
        await chan.send(f"{player} joined table {table}")    
    elif ret == 3:
        ret = gi.getTableName(player)
        await chan.send(f"{player} is already at table {ret}!")
    elif ret == 4:
        await chan.send(f"{table} already has {MAX_PLAYERS} players!")


@bot.command()
async def remove(ctx):
    """
    Leave a pier!
    """

    player = ctx.author
    chan = ctx.channel

    ret = gi.remove(player)
    if ret == 0:
        await chan.send(f"{player} Removed!")
    elif ret == 1:
        await chan.send(f"{player} is not at any tables!")

        
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
        for p in gi.tables[t].players:
            ret += "    "+str(p)+"\n"
        ret += "\n"
    await chan.send(ret)


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
    if ret == 0:
        await chan.send("Score reported")
    elif ret == 1:
        await chan.send(f"{player} is not at a table")
    elif ret == 2:
        await chan.send(f"{score} is not formated properly")
    
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
