from discord.ext import commands
from queue import Queue

class Channel_controller(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='join', help='Joins the voice channel')
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("```You are not in a voice channel.```")
            return
        if ctx.voice_client is not None:
            await ctx.send('```Already in a voice channel.```')
            return
        queue = self.bot.get_cog('Queue')
        queue.construct_queue(ctx.guild.id)
        channel = ctx.message.author.voice.channel
        await channel.connect()

    @commands.command(name='leave', help='Leaves the voice channel')
    async def leave(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("```You are not in a voice channel.```")
            return
        if ctx.voice_client is None:
            return
        if ctx.voice_client.channel != ctx.message.author.voice.channel:
            await ctx.send('```You must be in the same voice channel as the bot.```')
            return
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()
        Queue.queue[ctx.guild.id] = []
        await ctx.voice_client.disconnect()
