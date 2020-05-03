import discord, os
from discord.ext import commands
TOKEN = os.environ["DISCORD_TOKEN"]

bot = commands.Bot("!")

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

bot.run(TOKEN)
