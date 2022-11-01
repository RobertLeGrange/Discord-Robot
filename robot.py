import discord
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv

intents = discord.Intents.all()
bot = commands.Bot(command_prefix = '!', intents = intents)

Signature = "\n\nSincerely, Robot"

load_dotenv()
TOKEN = os.getenv('TOKEN')

initial_extensions = []

async def setupcogs():
    for filename in os.listdir('./cogs/general'):
        if filename.endswith('.py'):
            initial_extensions.append('cogs.general.' + filename[:-3])
    for extension in initial_extensions:
        await bot.load_extension(extension)

async def main():
    async with bot:
        await setupcogs()
        await bot.start(TOKEN)

async def find_cog(arg):
    arg = arg.title()
    file = arg + '.py'
    generalcogs = os.listdir('./cogs/general')
    specialcogs = os.listdir('./cogs/special')
    if file in generalcogs:
        path = 'cogs.general.' + arg
    elif file in specialcogs:
        path = 'cogs.special.' + arg
    else:
        print('Unknown Cog {} Not Found'.format(arg), flush=True)
    return path

@bot.command()
async def load(ctx, arg):
    path = await find_cog(arg)
    await bot.load_extension(path)

@bot.command()
async def unload(ctx, arg):
    path = await find_cog(arg)
    await bot.unload_extension(path)
    print('{} Cog {} Unloaded'.format(path[5:12].title(), arg.title()), flush=True)

@bot.command()
async def reload(ctx, arg):
    path = await find_cog(arg)
    await bot.reload_extension(path)

if __name__ == '__main__':
    asyncio.run(main())
