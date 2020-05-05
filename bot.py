import discord, os
from discord.ext import commands
from functions import parseGame, scoreTable
from functions import TENGO,TENSAN,TENPIN
import requests, sys
import xml.etree.ElementTree as ET

TOKEN = os.environ["DISCORD_TOKEN"]

bot = commands.Bot("!")

@bot.command()
async def parse_log(ctx, log=None, rate="tensan"):
    player = ctx.author
    chan = ctx.channel

    if log == None or rate == None:
        await chan.send("usage: !parse_log [tenhou_log] [rate]\nEx: !parse_log 2020050308gm-0209-19713-4a1a192b tengo")
        
    
    table = [["Name","Score","Shugi","Final"]]

    rate = rate.lower()
    if rate == "tensan":
        players = parseGame(log, TENSAN)
    elif rate == "tengo":
        players = parseGame(log, TENGO)
    elif rate == "tenpin":
        players = parseGame(log, TENPIN)
    
    for p in players:
        table.append([str(p.name),str(p.score),str(p.shugi),str(p.payout)])
    #colMax = [max([len(i) for i in c]) for c in zip(*table)]
    ret = ""
    for col,row in enumerate(table):
        ret += f"{row[col].ljust(8)}\t"
        if (col + 1) % 4 == 0:
            ret += "\n"
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
