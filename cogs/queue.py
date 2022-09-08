from discord.ext import commands


class Queue(commands.Cog):
    def _init_(self, bot):
        self.bot = bot
        self.queue = {}

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
