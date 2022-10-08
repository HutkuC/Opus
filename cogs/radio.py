from discord.ext import commands
import discord
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By


class Radio(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.radio_status = {}

    def get_radio_status(self, ctx):
        if ctx.guild.id not in self.radio_status:
            self.radio_status[ctx.guild.id] = False
        return self.radio_status[ctx.guild.id]

    @staticmethod
    def get_next_song(url):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        browser = webdriver.Chrome(options=options)
        browser.get(url)
        timeout_in_seconds = 10
        WebDriverWait(browser, timeout_in_seconds).until(ec.presence_of_element_located((By.ID, 'contents')))
        html = browser.page_source
        browser.quit()
        soup = BeautifulSoup(html, features="html.parser")
        href = soup.find('a', class_='yt-simple-endpoint style-scope ytd-compact-video-renderer')['href']
        return href[9:]

    @commands.command(name='radio', help='Opens or closes the radio')
    async def radio(self, ctx, status):
        if ctx.author.voice is None:
            await ctx.send(embed=discord.Embed(title='You are not in a voice channel.', color=0x800800))
            return
        if ctx.voice_client is None:
            await ctx.send(embed=discord.Embed(title='Not playing anything.', color=0x800800))
            return
        if ctx.voice_client.channel != ctx.message.author.voice.channel:
            await ctx.send(embed=discord.Embed(title='You must be in the same voice channel as the bot.',
                                               color=0x800800))
            return

        if status.lower() == 'on':
            self.radio_status[ctx.guild.id] = True
            await ctx.send(embed=discord.Embed(title='Radio is on.', color=0x800800))
            return
        elif status.lower() == 'off':
            self.radio_status[ctx.guild.id] = False
            await ctx.send(embed=discord.Embed(title='Radio is off.', color=0x800800))
            return
        else:
            await ctx.send(embed=discord.Embed(title='Invalid status.', color=0x800800))
            return
