import discord
from discord.ext import commands
from discord import FFmpegPCMAudio




queues = {}

Signature = "\n\nSincerely, Robot"

print('Cog Music Loaded', flush=True)

class Music(commands.Cog):

    def __init__(self, bot):
         self.bot = bot

    @commands.command()
    async def play(self, ctx, arg):
        extension = '.mp3'
        song = arg + extension
        source = FFmpegPCMAudio(song)
        voice = ctx.guild.voice_client
        player = voice.play(source, after=lambda x=None: check_queue(ctx, ctx.guild.id))

    @commands.command(pass_context = True)
    async def pause(self, ctx):
        voice = ctx.guild.voice_client
        if voice.is_playing():
            voice.pause()

    @commands.command()
    async def resume(self, ctx):
        voice = ctx.guild.voice_client
        if voice.is_paused():
            voice.resume()

    @commands.command()
    async def stop(self, ctx):
        voice = ctx.guild.voice_client
        voice.stop()
        guild_id = ctx.guild.id
        queues.pop(guild_id)

    async def check_queue(self, ctx, id):
        if queues[id] != []:
            voice = ctx.guild.voice_client
            source = queues[id].pop(0)
            player = voice.play(source)

    @commands.command()
    async def queue(self, ctx, arg):
        voice = ctx.guild.voice_client
        extension = '.mp3'
        song = arg + extension
        guild_id = ctx.guild.id
        source = FFmpegPCMAudio(song)
        if guild_id in queues:
            queues[guild_id].append(source)
        else:
            queues[guild_id] = [source]
        await ctx.send("Added '{}' to queue".format(song))
        await ctx.send(queues[guild_id])

async def setup(bot):
    await bot.add_cog(Music(bot))
