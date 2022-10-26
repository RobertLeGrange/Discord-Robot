import discord
from discord.ext import commands
import os
import asyncio

intents = discord.Intents.all()
bot = commands.Bot(command_prefix = '!', intents = intents)

Signature = "\n\nSincerely, Robot"

initial_extensions = []

async def setupcogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            initial_extensions.append('cogs.' + filename[:-3])
    for extension in initial_extensions:
        await bot.load_extension(extension)

async def main():
    async with bot:
        await setupcogs()
        await bot.start('MTAzMjA0MTAxMDIyMzY0ODc5OA.GPgesj.bM8Qg19LcmmVXLsjuvGtyh292HUEaetJjhuFtI')

if __name__ == '__main__':
    asyncio.run(main())


#bot.run('MTAzMjA0MTAxMDIyMzY0ODc5OA.GPgesj.bM8Qg19LcmmVXLsjuvGtyh292HUEaetJjhuFtI')
