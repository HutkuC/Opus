from discord.ext import commands
import discord


class Channel_controller(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='join', help='Joins the voice channel')
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send(embed=discord.Embed(title='You are not in a voice channel.', color=0x800800))
            return
        if ctx.voice_client is not None:
            await ctx.send(embed=discord.Embed(title='Already in a voice channel.', color=0x800800))
            return
        queue = self.bot.get_cog('Queue')
        queue.construct_queue(ctx.guild.id)
        channel = ctx.message.author.voice.channel
        await channel.connect()

    @commands.command(name='leave', help='Leaves the voice channel')
    async def leave(self, ctx):
        if ctx.author.voice is None:
            await ctx.send(embed=discord.Embed(title='You are not in a voice channel.', color=0x800800))
            return
        if ctx.voice_client is None:
            return
        if ctx.voice_client.channel != ctx.message.author.voice.channel:
            await ctx.send(embed=discord.Embed(title='You must be in the same voice channel as the bot.',
                                               color=0x800800))
            return

        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()
        queue = self.bot.get_cog('Queue')
        queue.queue[ctx.guild.id] = []
        await ctx.voice_client.disconnect()
