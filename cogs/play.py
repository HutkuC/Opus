from discord.ext import commands
from youtubesearchpython import VideosSearch
from discord.ext import tasks
import discord
import os
from cogs.song import Song
from cogs.download import Download


class Play(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.skip_set = set()

    def auto_skip(self, ctx):
        self.skip_set.add(ctx)

    @tasks.loop(seconds=1)
    async def check_skip(self):
        if len(self.skip_set) > 0:
            music_controller = self.bot.get_cog('Music_controller')
            for ctx in self.skip_set:
                if ctx.voice_client is not None:
                    await music_controller.skip(ctx, 'auto_skip')
            self.skip_set.clear()

    async def start(self, ctx):
        queue = self.bot.get_cog('Queue')
        if os.path.exists("./sound_files/" + str(ctx.guild.id) + ".mp3"):
            os.remove("./sound_files/" + str(ctx.guild.id) + ".mp3")

        if len(queue.queue[ctx.guild.id]) == 0:
            return

        message = await ctx.send(embed=discord.Embed(title=':hourglass: Loading...', color=0x800800))

        url = queue.get_url(ctx, 0)
        Download.download(ctx, url)

        ctx.voice_client.play(discord.FFmpegPCMAudio("sound_files/" + str(ctx.guild.id) + ".mp3"),
                              after=lambda e: self.auto_skip(ctx))

        embed = discord.Embed(title=queue.get_title(ctx, 0),
                              url=queue.get_url(ctx, 0),
                              color=0x800800)
        embed.set_author(name='Now playing')
        embed.set_thumbnail(url=queue.get_thumbnail(ctx, 0))
        embed.add_field(name='__Duration__', value=queue.get_duration(ctx, 0), inline=True)
        embed.add_field(name='__Requested by__', value=queue.get_requester(ctx, 0), inline=True)

        await message.edit(embed=embed)

    @commands.command(name='play', help='Plays a song')
    async def play(self, ctx, *args):
        if ctx.message.author.voice is None:
            await ctx.send(embed=discord.Embed(title='You are not in a voice channel.', color=0x800800))
            return
        if ctx.voice_client is None:
            channel_controller = self.bot.get_cog('Channel_controller')
            await channel_controller.join(ctx)
        elif ctx.voice_client.channel != ctx.message.author.voice.channel:
            await ctx.send(embed=discord.Embed(title='You must be in the same voice channel as the bot.',
                                               color=0x800800))
            return

        search_term = ''
        for word in args:
            search_term += str(word) + ' '

        videosSearch = VideosSearch(search_term, limit=1)

        video_title = videosSearch.result()['result'][0]['title'].replace(' - Topic', '')
        url = videosSearch.result()['result'][0]['link']
        duration = videosSearch.result()['result'][0]['duration']
        thumbnail = videosSearch.result()['result'][0]['thumbnails'][0]['url']
        requester = ctx.message.author.name

        queue = self.bot.get_cog('Queue')
        queue.add_to_queue(ctx, Song(video_title, url, duration, requester, search_term, thumbnail))

        if len(queue.queue[ctx.guild.id]) != 1:
            queue_len = len(queue.queue[ctx.guild.id])
            embed = discord.Embed(title=queue.get_title(ctx, queue_len-1),
                                  url=queue.get_url(ctx, queue_len-1),
                                  color=0x800800)
            embed.set_author(name='Added to queue')
            embed.set_thumbnail(url=queue.get_thumbnail(ctx, queue_len-1))
            embed.add_field(name='__Duration__', value=queue.get_duration(ctx, queue_len-1), inline=True)
            embed.add_field(name='__Requested by__', value=queue.get_requester(ctx, queue_len-1), inline=True)
            await ctx.send(embed=embed)

        if ctx.voice_client.is_playing() is False and \
                len(queue.queue[ctx.guild.id]) == 1:
            await self.start(ctx)
