import discord
from discord import app_commands
from discord.commands.core import slash_command
from discord.ext import commands
import xbox
from core.common import load_config
config, _ = load_config()

class SlashCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Ping Command
    @app_commands.command(name="ping", description = "Shows the bots latency", guild_ids=[config['PBtest']])
    async def ping(self, ctx):
        # await ctx.send(f'**__Latency is__ ** {round(client.latency * 1000)}ms')
        pingembed = discord.Embed(
            title="Pong! ⌛", color=0x20F6B3, description="Current Discord API Latency")
        pingembed.add_field(name="Current Ping:",
                            value=f'{round(self.bot.latency * 1000)}ms')
        await ctx.send(embed=pingembed)

    # Removes your nickname.
    @app_commands.command(name="removenick", description = "Reverts your nickname back to your username!", guild_ids=[config['PBtest']])
    async def removenick(self, ctx):
        author = ctx.author
        name = author.name
        await author.edit(nick=str(author.name))
        await ctx.send(content = "Removed your nickname!")

    # Embed Command
    @app_commands.command(name="embed", description = "converts your message to an embed", guild_ids=[config['PBtest']])
    @commands.has_permissions(manage_channels=True)
    async def embed(self, ctx, channel: discord.TextChannel, title, body):
        colorvalue = int(discord.Colour.random())
        embed = discord.Embed(title=title, description=body, color=colorvalue)
        await channel.send(embed=embed)

    #Say command
    @app_commands.command(name="say", description = "say something as the bot", guild_ids=[config['PBtest']])
    @commands.has_role("Moderator")
    async def say(self, ctx, *, msg):
        await ctx.channel.purge(limit = 1)
        await ctx.send(msg)


async def setup(bot):
    await bot.add_cog(SlashCommands(bot))