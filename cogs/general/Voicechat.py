import discord
from discord.ext import commands
from discord import FFmpegPCMAudio






Signature = "\n\nSincerely, Robot"

print('General Cog VoiceChat Loaded', flush=True)

class Voicechat(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Joins the voice channel")
    async def join(self, ctx):
        if ctx.author.voice:
            channel = ctx.message.author.voice.channel
            voice = await channel.connect()
            source = FFmpegPCMAudio('.\Music\cena.mp3')
            player = voice.play(source)
            await ctx.send("Hi, I have joined the voice channel '{}' now.".format(channel) + Signature)
        else:
            await ctx.send("Sorry, but you need to be in the voice channel first in order for me to join." + Signature)

    @commands.command(help="Leaves the voice channel")
    async def leave(self, ctx):
        if ctx.voice_client:
            channel = ctx.guild.voice_client.channel
            await ctx.guild.voice_client.disconnect()
            await ctx.send("Goodbye! I've left the '{}' voice channel now.".format(str(channel)) + Signature)
        else:
            await ctx.send("Sorry, but I'm not in a voice channel at the moment." + Signature)

async def setup(bot):
    await bot.add_cog(Voicechat(bot))
