import discord
from discord.ext import commands

class RepeatCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='repeat', description='Repeats what you type')
    async def repeat(self, ctx, *, message):
        await ctx.send(message)

def setup(bot):
    bot.add_cog(RepeatCog(bot))