from discord.ext import commands
from queue import Queue
#from play import Play

class Music_controller(commands.Cog):

    def _init_(self, bot):
        self.bot = bot

    @commands.command(name='pause', help='Pauses the current song')
    async def pause(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("```You are not in a voice channel.```")
            return
        if ctx.voice_client is None:
            await ctx.send('```Not playing anything.```')
            return
        if ctx.voice_client.channel != ctx.message.author.voice.channel:
            await ctx.send('```You must be in the same voice channel as the bot.```')
            return
        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send('```Paused.```')
        else:
            await ctx.send('```Already paused.```')

    @commands.command(name='resume', help='Resumes the current song')
    async def resume(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("```You are not in a voice channel.```")
            return
        if ctx.voice_client is None:
            await ctx.send('```Not playing anything.```')
            return
        if ctx.voice_client.channel != ctx.message.author.voice.channel:
            await ctx.send('```You must be in the same voice channel as the bot.```')
            return
        if ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send('```Resumed.```')
        else:
            await ctx.send('```Not paused.```')

    @commands.command(name='skip', help='Skips the current song')
    async def skip(self, ctx, *args):
        if ctx.author.voice is None:
            await ctx.send("```You are not in a voice channel.```")
            return
        if ctx.voice_client is None:
            await ctx.send('```Not playing anything.```')
            return
        if ctx.voice_client.channel != ctx.message.author.voice.channel:
            await ctx.send('```You must be in the same voice channel as the bot.```')
            return

        queue = self.bot.get_cog('Queue')

        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()
        if len(queue.queue[ctx.guild.id]) > 0:
            queue.queue[ctx.guild.id].pop(0)
        if len(args) == 0:
            await ctx.send('```Skipped.```')

        if len(queue.queue[ctx.guild.id]) > 0:
            play = self.bot.get_cog('Play')
            await play.start(self, ctx)
