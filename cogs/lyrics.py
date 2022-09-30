from discord.ext import commands
from bs4 import BeautifulSoup
import discord
import requests


class Lyrics(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def get_lyrics(term):
        HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

        url = "https://www.musixmatch.com/search/" + '%20'.join(term.split()) + "/tracks"
        page = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(page.content, 'html.parser')

        song_link = "https://www.musixmatch.com" + soup.find_all('a', class_='title')[0]['href']

        page = requests.get(song_link, headers=HEADERS)
        soup = BeautifulSoup(page.content, 'html.parser')

        lyrics_root = soup.find_all('p', class_='mxm-lyrics__content')

        lyrics = '\n'.join([str(lyrics_root[i].text) for i in range(len(lyrics_root))])
        song_name = soup.find_all('h1', class_="mxm-track-title__track")[0].text[6:]
        artist_name = soup.find_all('a', class_='mxm-track-title__artist mxm-track-title__artist-link')[0].text
        thumbnail = soup.find_all('img')[1]['src']

        return lyrics, song_name, artist_name, thumbnail, song_link

    @commands.command(name='lyrics', help='Shows the lyrics of the song')
    async def lyrics(self, ctx, *args):
        if len(args) == 0:
            if ctx.author.voice is None:
                await ctx.send(embed=discord.Embed(title='You are not in a voice channel.', color=0x800800))
                return
            if ctx.voice_client is None:
                await ctx.send(embed=discord.Embed(title='Not playing anything.', color=0x800800))
                return
            if ctx.voice_client.channel != ctx.message.author.voice.channel:
                await ctx.send(
                    embed=discord.Embed(title='You must be in the same voice channel as the bot.', color=0x800800))
                return

            queue = self.bot.get_cog('Queue')
            term = queue.get_search_term(ctx, 0)

            if term is None:
                await ctx.send(embed=discord.Embed(title='No song is playing.', color=0x800800))
                return
            else:
                lyrics, song_name, artist_name, img, song_link = self.get_lyrics(term)

        else:
            lyrics, song_name, artist_name, img, song_link = self.get_lyrics(' '.join(args))

        embed = discord.Embed(title=artist_name + ' - ' + song_name, description=lyrics, url=song_link, color=0x800800)
        embed.set_author(name='Lyrics')
        embed.set_thumbnail(url='https://' + img[2:])
        embed.set_footer(text='Powered by Musixmatch')

        await ctx.send(embed=embed)
