import discord, os
from discord.ext import commands
from functions import GameInstance

TOKEN = os.environ["DISCORD_TOKEN"]

bot = commands.Bot("!")
gi = GameInstance()

@bot.command()
async def join(ctx):
    author = ctx.author
    chan = ctx.channel
    await chan.send(f"{author} Joined!")

@bot.command()
async def remove(ctx):
    author = ctx.author
    chan = ctx.channel
    await chan.send(f"{author} Removed!")

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
