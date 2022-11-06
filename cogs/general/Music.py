import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import os
import youtube_dl



Signature = "\n\nSincerely, Robot"

print('General Cog Music Loaded', flush=True)

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {'options': '-vn'}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

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

    @commands.command(help="Streams audio from a youtube url")
    async def stream(self, ctx, *, url):
        """Streams from a url (same as yt, but doesn't predownload)"""
        player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
        ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
        await ctx.send('Now playing: {}'.format(player.title))

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
        title = "Below are the folders and songs in {}".format(path[2:])
        if folder_list:
            folders = ("\n").join(folder_list)
        else:
            folders="None"
        if song_list:
            songs = ("\n").join(song_list)
        else:
            songs="None"
        embed = discord.Embed(title=title)
        embed.add_field(name="Folders", value=folders, inline=False)
        embed.add_field(name="Songs", value=songs, inline=False)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Music(bot))
