import os
import discord
import asyncio
from discord.ext import commands
from cogs import channel_controller, music_controller, play, queue

TOKEN = '[Discord Bot Token]'

intents = discord.Intents.all()

client = discord.Client(intents=intents)

bot = commands.Bot(command_prefix='!', intents=intents)

COGS = [channel_controller.Channel_controller, music_controller.Music_controller, play.Play, queue.Queue]


async def add_cogs():
    for cog in COGS:
        await bot.add_cog(cog(bot))

asyncio.run(add_cogs())


@bot.event
async def on_ready():
    print('Bot is ready.')
    play = bot.get_cog('Play')
    await play.check_skip.start()

bot.run(TOKEN)
