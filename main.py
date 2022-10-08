import discord
import asyncio
import os
from discord.ext import commands
from cogs import channel_controller, music_controller, play, queue, lyrics, radio
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)

COGS = [channel_controller.Channel_controller,
        music_controller.Music_controller,
        play.Play,
        queue.Queue,
        lyrics.Lyrics,
        radio.Radio]


async def add_cogs():
    for cog in COGS:
        await bot.add_cog(cog(bot))

asyncio.run(add_cogs())


@bot.event
async def on_ready():
    print('Bot is ready.')
    Play = bot.get_cog('Play')
    await Play.check_skip.start()

bot.run(TOKEN)
