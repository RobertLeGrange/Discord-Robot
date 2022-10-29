import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import os





Signature = "\n\nSincerely, Robot"

print('Cog Music Loaded', flush=True)

class Music(commands.Cog):

    def __init__(self, bot):
         self.bot = bot

    @commands.command(help="Plays the requested song")
    async def play(self, ctx, *arg):
        extension = '.mp3'
        parent = './Music'
        path =  await self.create_path(parent, arg)
        song = path + extension
        source = FFmpegPCMAudio(song)
        voice = ctx.guild.voice_client
        player = voice.play(source)

    @commands.command(help="Pauses the song currently playing")
    async def pause(self, ctx):
        voice = ctx.guild.voice_client
        if voice.is_playing():
            voice.pause()

    @commands.command(help="Resumes the song currently paused")
    async def resume(self, ctx):
        voice = ctx.guild.voice_client
        if voice.is_paused():
            voice.resume()

    @commands.command(help="Stops the song currently playing")
    async def stop(self, ctx):
        voice = ctx.guild.voice_client
        voice.stop()
        guild_id = ctx.guild.id

    async def create_path(self, parent, arg):
        path_list = [parent]
        path_list.extend(list(arg))
        path = '/'.join(path_list)
        return path

    @commands.command(help="Lists the songs in the requested folder")
    async def gather_songs(self, ctx, *arg):
        arg_check = [True if x.find("..") >-1 else False for x in arg]
        if any(arg_check):
            await ctx.send("Get outta ma files" + Signature)
            return None
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
