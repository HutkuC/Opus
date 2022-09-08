from discord.ext import commands
from youtubesearchpython import VideosSearch
from pytube import YouTube
import discord
import os


class Play(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.is_skip = set()

    def auto_skip(self, ctx):
        self.is_skip.add(ctx)

    async def start(self, ctx):
        queue = self.bot.get_cog('Queue')
        if os.path.exists(".sound_files/" + str(ctx.guild.id) + ".mp3"):
            os.remove(".sound_files/" + str(ctx.guild.id) + ".mp3")

        if len(queue.queue[ctx.guild.id]) == 0:
            return

        yt = YouTube(queue[0][2])
        video = yt.streams.filter(only_audio=True).first()
        destination = '.sound_files/'
        out_file = video.download(output_path=destination)
        new_file = str(ctx.guild.id) + ".mp3"
        os.rename(out_file, new_file)

        print(yt.title + " has been successfully downloaded.")
        ctx.voice_client.play(discord.FFmpegPCMAudio(".sound_files/" + str(ctx.guild.id) + ".mp3"),
                              after=lambda e: self.auto_skip(ctx))
        await ctx.send(f'```Current song: {queue[0][0]} - {queue[0][1]}```')

    @commands.command(name='play', help='Plays a song')
    async def play(self, ctx, *args):
        if ctx.message.author.voice is None:
            await ctx.send("```You are not in a voice channel.```")
            return
        if ctx.voice_client is None:
            channel_controller = self.bot.get_cog('Channel_controller')
            await channel_controller.join(ctx)
        elif ctx.voice_client.channel != ctx.message.author.voice.channel:
            await ctx.send('```You must be in the same voice channel as the bot.```')
            return

        search_text = ''
        for word in args:
            search_text += word + ' '

        videosSearch = VideosSearch(search_text, limit=1)

        url = videosSearch.result()['result'][0]['link']
        duration = videosSearch.result()['result'][0]['duration']
        video_title = videosSearch.result()['result'][0]['title']
        video_title = video_title.replace(' - Topic', '')

        queue = self.bot.get_cog('Queue')
        queue.add_queue(ctx.guild.id, duration, video_title, url, search_text)

        await ctx.send(f'```Added to queue:\n{video_title}```')
        if ctx.voice_client.is_playing() is False and \
                ctx.voice_client.is_paused() is False and \
                len(queue.queue[ctx.guild.id]) == 1:
            await self.start(ctx)
