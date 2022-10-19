import discord

from discord.ext import commands

client = commands.Bot(command_prefix = '!', intents = discord.Intents.all())


@client.event
async def on_ready():
    print("Robot is ready!")
    print("---------------")

@client.command()
async def hello(ctx):
    await ctx.send("Hello, I am Robot!")

client.run('MTAzMjA0MTAxMDIyMzY0ODc5OA.GPgesj.bM8Qg19LcmmVXLsjuvGtyh292HUEaetJjhuFtI')
