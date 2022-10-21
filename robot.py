import discord
from datetime import datetime as dt

from discord.ext import commands

client = commands.Bot(command_prefix = '!', intents = discord.Intents.all())


@client.event
async def on_ready():
    print("Robot is ready!")
    print("---------------")

@client.command()
async def hello(ctx):
    await ctx.send("Hello, I am Robot!")

@client.command()
async def games(ctx):
    await ctx.send("<@191661345794424832> <@329167323510603786> <@537543052982485013> it gaem time. \nSincerely, Robot")

client.run('MTAzMjA0MTAxMDIyMzY0ODc5OA.GPgesj.bM8Qg19LcmmVXLsjuvGtyh292HUEaetJjhuFtI')
