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
from .cogs import channel_controller, music_controller, play, queue

TOKEN = '[YOUR TOKEN]'

intents = discord.Intents.all()

client = discord.Client(intents=intents)

bot = commands.Bot(command_prefix='h!', intents=intents)

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

COGS = [channel_controller.Channel_controller, music_controller.Music_controller, play.Play, queue.Queue]

for cog in COGS:
    bot.add_cog(cog(bot))

bot.run(TOKEN)




