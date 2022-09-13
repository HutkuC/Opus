from discord.ext import commands
import discord
from cogs.song import Song


class Queue(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.queue = {}

    def construct_queue(self, guild_id):
        if guild_id in self.queue:
            return
        self.queue[guild_id] = []

    def get_url(self, ctx, index):
        if ctx.guild.id in self.queue and len(self.queue[ctx.guild.id]) > index:
            return self.queue[ctx.guild.id][index].url
        return None

    def get_title(self, ctx, index):
        if ctx.guild.id in self.queue and len(self.queue[ctx.guild.id]) > index:
            return self.queue[ctx.guild.id][index].title
        return None

    def get_search_term(self, ctx, index):
        if ctx.guild.id in self.queue and len(self.queue[ctx.guild.id]) > index:
            return self.queue[ctx.guild.id][index].search_term
        return None

    def get_duration(self, ctx, index):
        if ctx.guild.id in self.queue and len(self.queue[ctx.guild.id]) > index:
            return self.queue[ctx.guild.id][index].duration
        return None

    def get_requester(self, ctx, index):
        if ctx.guild.id in self.queue and len(self.queue[ctx.guild.id]) > index:
            return self.queue[ctx.guild.id][index].requester
        return None

    def get_thumbnail(self, ctx, index):
        if ctx.guild.id in self.queue and len(self.queue[ctx.guild.id]) > index:
            return self.queue[ctx.guild.id][index].thumbnail
        return None

    def add_to_queue(self, ctx, track: Song):
        if self.queue[ctx.guild.id] is None:
            self.queue[ctx.guild.id] = []
        self.queue[ctx.guild.id].append(track)

    @commands.command(name='queue', help='Shows the queue')
    async def queue(self, ctx):
        if ctx.author.voice is None:
            await ctx.send(embed=discord.Embed(title='You are not in a voice channel.', color=0x800800))
            return
        if ctx.voice_client is None:
            await ctx.send(embed=discord.Embed(title='Not playing anything.', color=0x800800))
            return
        if ctx.voice_client.channel != ctx.message.author.voice.channel:
            await ctx.send(embed=discord.Embed(title='You must be in the same voice channel as the bot.', color=0x800800))
            return
        if len(self.queue[ctx.guild.id]) == 0:
            await ctx.send(embed=discord.Embed(title='The queue is empty.', color=0x800800))
            return

        embed = discord.Embed(title=self.get_title(ctx, 0),
                              url=self.get_url(ctx, 0),
                              description='> Duration: {}    Requested by: {}'.format(self.get_duration(ctx, 0), self.get_requester(ctx, 0)),
                              color=0x800800)
        embed.set_author(name='Queue for ' + ctx.guild.name)
        embed.set_thumbnail(url=self.get_thumbnail(ctx, 0))
        if len(self.queue[ctx.guild.id]) > 1:
            value = ''
            for i in range(1, len(self.queue[ctx.guild.id])):
                value += '{}-  [{}]({})\n'.format(i, self.get_title(ctx, i), self.get_url(ctx, i))
                value += '> Duration: {}    Requested by: {}\n'.format(self.get_duration(ctx, i), self.get_requester(ctx, i))
            embed.add_field(name='**Up next:**', value=value, inline=False)
        else:
            embed.add_field(name='**Up Next:**', value='Nothing', inline=False)

        await ctx.send(embed=embed)

    @commands.command(name='now-playing', help='Shows the current song')
    async def now_playing(self, ctx):
        if ctx.author.voice is None:
            await ctx.send(embed=discord.Embed(title='You are not in a voice channel.', color=0x800800))
            return
        if ctx.voice_client is None:
            await ctx.send(embed=discord.Embed(title='Not playing anything.', color=0x800800))
            return
        if ctx.voice_client.channel != ctx.message.author.voice.channel:
            await ctx.send(embed=discord.Embed(title='You must be in the same voice channel as the bot.', color=0x800800))
            return
        if len(self.queue[ctx.guild.id]) == 0:
            await ctx.send(embed=discord.Embed(title='Not playing anything.', color=0x800800))
            return

        embed = discord.Embed(title=self.get_title(ctx, 0),
                              url=self.get_url(ctx, 0),
                              color=0x800800)
        embed.set_author(name='Now playing')
        embed.set_thumbnail(url=self.get_thumbnail(ctx, 0))
        embed.add_field(name='__Duration__', value=self.get_duration(ctx, 0), inline=True)
        embed.add_field(name='__Requested by__', value=self.get_requester(ctx, 0), inline=True)

        await ctx.send(embed=embed)

    @commands.command(name='remove', help='Removes a song from the queue')
    async def remove(self, ctx, index):
        if ctx.author.voice is None:
            await ctx.send(embed=discord.Embed(title='You are not in a voice channel.', color=0x800800))
            return
        if ctx.voice_client is None:
            await ctx.send(embed=discord.Embed(title='Not playing anything.', color=0x800800))
            return
        if ctx.voice_client.channel != ctx.message.author.voice.channel:
            await ctx.send(embed=discord.Embed(title='You must be in the same voice channel as the bot.', color=0x800800))
            return
        if len(self.queue[ctx.guild.id]) == 0:
            await ctx.send(embed=discord.Embed(title='The queue is empty.', color=0x800800))
            return
        if int(index) < 1 or int(index) >= len(self.queue[ctx.guild.id]):
            await ctx.send(embed=discord.Embed(title='Invalid index.', color=0x800800))
            return

        embed = discord.Embed(title=self.get_title(ctx, int(index)),
                              url=self.get_url(ctx, int(index)),
                              color=0x800800)
        embed.set_author(name='Removed from queue')
        embed.set_thumbnail(url=self.get_thumbnail(ctx, int(index)))
        embed.add_field(name='__Duration__', value=self.get_duration(ctx, int(index)), inline=True)
        embed.add_field(name='__Requested by__', value=self.get_requester(ctx, int(index)), inline=True)

        await ctx.send(embed=embed)
        self.queue[ctx.guild.id].pop(int(index))

    @commands.command(name='clear', help='Clears the queue')
    async def clear(self, ctx):
        if ctx.author.voice is None:
            await ctx.send(embed=discord.Embed(title='You are not in a voice channel.', color=0x800800))
            return
        if ctx.voice_client is None:
            await ctx.send(embed=discord.Embed(title='Not playing anything.', color=0x800800))
            return
        if ctx.voice_client.channel != ctx.message.author.voice.channel:
            await ctx.send(embed=discord.Embed(title='You must be in the same voice channel as the bot.', color=0x800800))
            return
        if len(self.queue[ctx.guild.id]) <= 1:
            await ctx.send(embed=discord.Embed(title='The queue is empty.', color=0x800800))
            return
        self.queue[ctx.guild.id] = self.queue[ctx.guild.id][:1]
        await ctx.send(embed=discord.Embed(title='Cleared the queue.', color=0x800800))
