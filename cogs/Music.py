import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import os





Signature = "\n\nSincerely, Robot"

print('Cog Music Loaded', flush=True)

class Music(commands.Cog):

    def __init__(self, bot):
         self.bot = bot

    @commands.command()
    async def play(self, ctx, arg):
        extension = '.mp3'
        song = './Music' + arg + extension
        source = FFmpegPCMAudio(song)
        voice = ctx.guild.voice_client
        player = voice.play(source)

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

    async def create_path(self, parent, arg):
        path_list = [parent]
        path_list.extend(list(arg))
        path = '/'.join(path_list)
        return path

    @commands.command()
    async def gather_songs(self, ctx, *arg):
        parent = './Music'
        path =  await self.create_path(parent, arg)
        folder_list, song_list = [], []
        for root, dirs, files in os.walk(path):
            folder_list.extend(dirs)
            song_list.extend(files)
            break
        for song in song_list:
            if not song.endswith('.mp3'):
                song_list.remove(song)
        song_list = [s.replace('.mp3','') for s in song_list]
        await ctx.send('Folder List:\n{} '.format(folder_list))
        await ctx.send('Song List:\n{} '.format(song_list))

async def setup(bot):
    await bot.add_cog(Music(bot))
