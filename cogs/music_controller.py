from discord.ext import commands
import discord


class Music_controller(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='pause', help='Pauses the current song')
    async def pause(self, ctx):
        if ctx.author.voice is None:
            await ctx.send(embed=discord.Embed(title='You are not in a voice channel.', color=0x800800))
            return
        if ctx.voice_client is None:
            await ctx.send(embed=discord.Embed(title='Not playing anything.', color=0x800800))
            return
        if ctx.voice_client.channel != ctx.message.author.voice.channel:
            await ctx.send(embed=discord.Embed(title='You must be in the same voice channel as the bot.', color=0x800800))
            return
        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send(embed=discord.Embed(title=':pause_button: Paused', color=0x800800))
            return
        else:
            return

    @commands.command(name='resume', help='Resumes the current song')
    async def resume(self, ctx):
        if ctx.author.voice is None:
            await ctx.send(embed=discord.Embed(title='You are not in a voice channel.', color=0x800800))
            return
        if ctx.voice_client is None:
            await ctx.send(embed=discord.Embed(title='Not playing anything.', color=0x800800))
            return
        if ctx.voice_client.channel != ctx.message.author.voice.channel:
            await ctx.send(embed=discord.Embed(title='You must be in the same voice channel as the bot.', color=0x800800))
            return
        if ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send(embed=discord.Embed(title=':arrow_forward: Resumed', color=0x800800))
        else:
            return

    @commands.command(name='skip', help='Skips the current song')
    async def skip(self, ctx, *args):
        if ctx.author.voice is None:
            await ctx.send(embed=discord.Embed(title='You are not in a voice channel.', color=0x800800))
            return
        if ctx.voice_client is None:
            await ctx.send(embed=discord.Embed(title='Not playing anything.', color=0x800800))
            return
        if ctx.voice_client.channel != ctx.message.author.voice.channel:
            await ctx.send(embed=discord.Embed(title='You must be in the same voice channel as the bot.', color=0x800800))
            return

        queue = self.bot.get_cog('Queue')

        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
        if len(args) == 0:
            await ctx.send(embed=discord.Embed(title=':next_track: Skipped', color=0x800800))
        if len(queue.queue[ctx.guild.id]) > 0:
            queue.queue[ctx.guild.id].pop(0)
        if len(queue.queue[ctx.guild.id]) > 0:
            play = self.bot.get_cog('Play')
            await play.start(ctx)
