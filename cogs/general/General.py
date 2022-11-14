import discord
from datetime import datetime as dt
import pytz
import requests
import json
from discord.ext import commands



Signature = "\n\nSincerely, Robot"

print('General Cog General Loaded', flush=True)

class General(commands.Cog):

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

async def setup(bot):
    await bot.add_cog(General(bot))
