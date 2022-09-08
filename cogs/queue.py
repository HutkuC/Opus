from discord.ext import commands


class Queue(commands.Cog):
    def _init_(self, bot):
        self.bot = bot
        self.queue = {}

    def get_from_queue(self, guild_id, index):
        return self.queue[guild_id][index]

    def add_to_queue(self, guild_id, duration, title, url, search_term):
        if self.queue[guild_id] is None:
            self.queue[guild_id] = []
        self.queue[guild_id].append({'duration': duration, 'title': title, 'url': url, 'search_term': search_term})

    @commands.command(name='queue', help='Shows the queue')
    async def queue(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("```You are not in a voice channel.```")
            return
        if ctx.voice_client is None:
            await ctx.send('```Not playing anything.```')
            return
        if ctx.voice_client.channel != ctx.message.author.voice.channel:
            await ctx.send('```You must be in the same voice channel as the bot.```')
            return
        if len(self.queue[ctx.guild.id]) == 0:
            await ctx.send('```The queue is empty.```')
            return
        msg = '```\n'
        msg += 'Current song: ' + self.queue[ctx.guild.id][0][0] + ' - ' + self.queue[ctx.guild.id][0][1] + '\n'
        for i in range(1, len(self.queue[ctx.guild.id])):
            msg += str(i) + ' - ' + self.queue[ctx.guild.id][i][0] + ' - ' + self.queue[ctx.guild.id][i][1] + '\n'
        msg += '```'
        await ctx.send(msg)

    @commands.command(name='now-playing', help='Shows the current song')
    async def now_playing(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("```You are not in a voice channel.```")
            return
        if ctx.voice_client is None:
            await ctx.send('```Not playing anything.```')
            return
        if ctx.voice_client.channel != ctx.message.author.voice.channel:
            await ctx.send('```You must be in the same voice channel as the bot.```')
            return
        if len(self.queue[ctx.guild.id]) == 0:
            await ctx.send('```Not playing anything.```')
            return
        msg = '```\n'
        msg += 'Current song: ' + self.queue[ctx.guild.id][0]['duration'] + ' - ' + self.queue[ctx.guild.id][0]['title'] + '\n'
        msg += '```'
        await ctx.send(msg)

    @commands.command(name='remove', help='Removes a song from the queue')
    async def remove(self, ctx, index):
        if ctx.author.voice is None:
            await ctx.send("```You are not in a voice channel.```")
            return
        if ctx.voice_client is None:
            await ctx.send('```Not playing anything.```')
            return
        if ctx.voice_client.channel != ctx.message.author.voice.channel:
            await ctx.send('```You must be in the same voice channel as the bot.```')
            return
        if len(self.queue[ctx.guild.id]) == 0:
            await ctx.send('```The queue is empty.```')
            return
        if int(index) < 1 or int(index) >= len(self.queue[ctx.guild.id]):
            await ctx.send('```Invalid index.```')
            return
        await ctx.send('```Removed the song ' + self.queue[ctx.guild.id][int(index)]['title'] + ' from the queue.```')
        self.queue[ctx.guild.id].pop(int(index))

    @commands.command(name='clear', help='Clears the queue')
    async def clear(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("```You are not in a voice channel.```")
            return
        if ctx.voice_client is None:
            await ctx.send('```Not playing anything.```')
            return
        if ctx.voice_client.channel != ctx.message.author.voice.channel:
            await ctx.send('```You must be in the same voice channel as the bot.```')
            return
        if len(self.queue[ctx.guild.id]) <= 1:
            await ctx.send('```The queue is empty.```')
            return
        self.queue[ctx.guild.id] = self.queue[ctx.guild.id][:1]
        await ctx.send('```Cleared the queue.```')