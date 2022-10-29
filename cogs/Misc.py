import discord
from datetime import datetime as dt
import pytz
import requests
import json
from discord.ext import commands



Signature = "\n\nSincerely, Robot"

print('Cog Misc Loaded', flush=True)

class Misc(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Robot is ready!", flush=True)
        print("---------------", flush=True)

    @commands.command(help="Tells a joke, sometimes it's even funny")
    async def joke(self, ctx):
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

    @commands.command(help="Hello World!")
    async def hello(self, ctx):
        await ctx.send("Hello, I am Robot!")

    @commands.command(help="Summons people for games")
    async def games(self, ctx):
        user = ctx.author.mention
        users = ['<@191661345794424832>', '<@329167323510603786>', '<@537543052982485013>']
        users.remove(user)
        await ctx.send(' '.join(map(str, users)) + " it gaem time." + Signature)

    @commands.command(help="Lists all the important timezones")
    async def times(self, ctx):
        #now = dt.now()
        #current_time = now.strftime("%H:%H")
        MelTZ = pytz.timezone('Australia/Melbourne')
        KiwiTZ = pytz.timezone('Pacific/Auckland')
        CowTZ = pytz.timezone('Australia/Queensland')
        MelTime = dt.now(MelTZ).strftime('%#I:%M %p')
        KiwiTime = dt.now(KiwiTZ).strftime('%#I:%M %p')
        CowTime = dt.now(CowTZ).strftime('%#I:%M %p')
        await ctx.send('The times are:\n**Actual Time**: {}\n**Kiwi Time**: {}\n**Cow Time**: {}\n\nSincerely, Robot'.format(MelTime, KiwiTime, CowTime))

async def setup(bot):
    await bot.add_cog(Misc(bot))
