import discord
from discord.ext import commands
from discord import app_commands

class RepeatCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    @app_commands.describe(
        message="Phrase to repeat"
    )
    @commands.command(name='repeat', description='Repeats what you type')
    async def repeat(self, ctx, interaction: discord.Interaction, *, message: str):
        await ctx.send(message)

async def setup(bot):
    await bot.add_cog(RepeatCog(bot))