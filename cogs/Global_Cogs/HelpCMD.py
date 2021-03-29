import discord
from discord.ext import commands
from datetime import datetime
import core.common
import logging

logger = logging.getLogger(__name__)

class HelpCMD(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logger.info("HelpCMD: Cog Loaded!")

    # Help Command
    @commands.group(invoke_without_command=True)
    async def help(self, ctx):
        author = ctx.message.author
        guild = ctx.message.guild
        role1 = discord.utils.find(
            lambda r: r.name == 'Realm Developer', ctx.message.guild.roles)
        role2 = discord.utils.find(
            lambda r: r.name == 'Studio Developer', ctx.message.guild.roles)
        if role1 in author.roles:
            helprealm = discord.Embed(title="Realm Commands \n", description="Use any of the following commands in the_innkeeper channel", color=0x20F6B3)
            helprealm.add_field(name="**applyrealm*",
                            value="*Apply to become a member of Aurafall Realms* \n **Usage:** %applyrealm", inline=False)          
            helprealm.set_thumbnail(url=guild.icon_url)
            timestamp = datetime.now()
            helprealm.set_footer(text=guild.name + " | Date: " +
                              str(timestamp.strftime(r"%x")))
            await ctx.send(embed=helprealm)
            helpmisc = discord.Embed(
                title="Misc Commands \n", description="Use any of the following commands in the_innkeeper channel", color=0x20F6B3)
            helpmisc.add_field(name="**Ping*",
                            value="*Check's API Latency!* \n **Usage:** /ping", inline=False)
            await ctx.send(embed=helpmisc)

        else:
            helprealm = discord.Embed(title="Realm Commands \n", description="Use any of the following commands in the_innkeeper channel", color=0x20F6B3)
            helprealm.add_field(name="*applyrealm*",
                            value="*Apply to become a member of Aurafall Realms* \n **Usage:** %applyrealm", inline=False)          
            helprealm.set_thumbnail(url=guild.icon_url)
            timestamp = datetime.now()
            helprealm.set_footer(text=guild.name + " | Date: " +
                              str(timestamp.strftime(r"%x")))
            await ctx.send(embed=helprealm)
            helpmisc = discord.Embed(
                title="Misc Commands \n", description="Use any of the following commands in the_innkeeper channel", color=0x20F6B3)
            helpmisc.add_field(name="*Ping*",
                            value="*Check's API Latency!* \n **Usage:** /ping", inline=False)
            await ctx.send(embed=helpmisc)

    @commands.command()
    async def info(self, ctx):
        config, _ = core.common.load_config()
        guild = ctx.message.guild
        em = discord.Embed(
            title="The Old King Info", description="Hello. I am The Old King, a `Discord.py` powered bot!", color=0xffd700)
        em.add_field(name="The Old King Owner:", value="BSavage81")
        em.add_field(name="Python Version: ", value="3.8.6")
        em.add_field(name="Discord.py Version:", value="1.5.1")
        em.add_field(name="The Old King Version:", value="1.0")
        em.add_field(name="Help Command:",
                     value=f"Prefix: **{config['prefix']}** | Help Command: **{config['prefix']}help** *or* **{config['prefix']}help (command)**")
        em.set_thumbnail(url=guild.icon_url)
        timestamp = datetime.now()
        em.set_footer(text=guild.name + " | Date: " +
                      str(timestamp.strftime(r"%x")))
        await ctx.send(embed=em)


# nick clear DM newrealm

def setup(bot):
    bot.add_cog(HelpCMD(bot))
