import discord
from datetime import datetime as dt
import pytz
import requests
import json
from discord.ext import commands

intents = discord.Intents.all()
client = commands.Bot(command_prefix = '!', intents = intents)

Signature = "\n\nSincerely, Robot"

@client.command()
async def joke(ctx):
    jokeurl = "https://v2.jokeapi.dev/joke/Any?safe-mode"
    querystring = {"format":"JSON"}
    headers = {
    	"X-RapidAPI-Key": "01739a5e22mshd021ebbddf5323ep1f7206jsnbbe2f0ce446e",
    	"X-RapidAPI-Host": "jokeapi-v2.p.rapidapi.com"
    }
    response = requests.request("GET", jokeurl, headers=headers, params=querystring)

    type = json.loads(response.text)['type']
    if type == 'twopart':
        setup = json.loads(response.text)['setup']
        delivery = json.loads(response.text)['delivery']
        joke = setup + '\n' + delivery
    if type == 'single':
        joke = json.loads(response.text)['joke']
    await ctx.send(joke)

@client.event
async def on_ready():
    print("Robot is ready!")
    print("---------------")

@client.command(pass_context = True)
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.message.author.voice.channel
        await channel.connect()
        await ctx.send("Hi, I have joined the voice channel '{}' now.".format(channel) + Signature)
    else:
        await ctx.send("Sorry, but you need to be in the voice channel first in order for me to join." + Signature)

@client.command(pass_context = True)
async def leave(ctx):
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
        await ctx.send("Goodbye! I've left the voice channel now." + Signature)
    else:
        await ctx.send("Sorry, but I'm not in a voice channel at the moment." + Signature)

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
