from operator import truediv
import os
import random
import discord
import ast
import youtube_dl
import googleapiclient.discovery
import googleapiclient.errors
import asyncio
from threading import Thread
from youtubesearchpython import VideosSearch
from time import localtime
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
from pytube import YouTube
from discord.ext import tasks
import requests as req
from bs4 import BeautifulSoup
from cogs import channel_controller, music_controller, play, queue

TOKEN = 'MTAxNzE1NzExMzgwNzY0Njc3Mg.Gu75Eu.g-BVDnMnCGxA2TfYNzQoKQ_olqQiPBcPQX2vTE'

intents = discord.Intents.all()

client = discord.Client(intents=intents)

bot = commands.Bot(command_prefix='o!', intents=intents)

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

COGS = [channel_controller.Channel_controller, music_controller.Music_controller, play.Play, queue.Queue]


async def add_cogs():
    for cog in COGS:
        await bot.add_cog(cog(bot))

asyncio.run(add_cogs())

bot.run(TOKEN)




