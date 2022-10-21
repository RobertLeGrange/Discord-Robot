import discord
from datetime import datetime as dt
import pytz

from discord.ext import commands

intents = discord.Intents.all()
client = commands.Bot(command_prefix = '!', intents = intents)


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

@client.command()
async def times(ctx):
    #now = dt.now()
    #current_time = now.strftime("%H:%H")
    MelTZ = pytz.timezone('Australia/Melbourne')
    KiwiTZ = pytz.timezone('Pacific/Auckland')
    CowTZ = pytz.timezone('Australia/Queensland')

    MelTime = dt.now(MelTZ).strftime('%#I:%M %p')
    KiwiTime = dt.now(KiwiTZ).strftime('%#I:%M %p')
    CowTime = dt.now(CowTZ).strftime('%#I:%M %p')

    await ctx.send('The times are:\n**Actual Time**: {}\n**Kiwi Time**: {}\n**Cow Time**: {}\n\nSincerely, Robot'.format(MelTime, KiwiTime, CowTime))


client.run('MTAzMjA0MTAxMDIyMzY0ODc5OA.GPgesj.bM8Qg19LcmmVXLsjuvGtyh292HUEaetJjhuFtI')
