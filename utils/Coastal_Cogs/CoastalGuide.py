from logging import exception
import discord
from discord.ext import commands
import time
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import asyncio
from core.common import load_config
config, _ = load_config()
i = 1
time_convert = {"s": 1, "m": 60, "h": 3600, "d": 86400}
import logging
logger = logging.getLogger(__name__)

# -------------------------------------------------------

def next_available_row(sheet):
    str_list = list(filter(None, sheet.col_values(1)))
    return str(len(str_list)+1)

def entryid_number(sheet):
    str_list = list(filter(None, sheet.col_values(1)))
    return str(len(str_list)-2)

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

client = gspread.authorize(creds)

sheet = client.open(
    "CCS8 Realm Application").sheet1

# ---CONSTANTS----------------------------------------------------


# -------------------------------------------------------

def check_Aurafall():
    def predicate(ctx):
        return (
            ctx.message.guild.id == 298995889551310848
            or ctx.message.guild.id == 448488274562908170
        )

    return commands.check(predicate)


def check_Coastal():
    def predicate(ctx):
        return (
            ctx.message.guild.id == 305767872410419211
            or ctx.message.guild.id == 448488274562908170
        )

    return commands.check(predicate)


def check_Coastal_MRP():
    def predicate(ctx):
        return (
            ctx.message.guild.id == 305767872410419211
            or ctx.message.guild.id == 448488274562908170
            or ctx.message.guild.id == 587495640502763521
        )

    return commands.check(predicate)


def convert(time):
    try:
        return int(time[:-1]) * time_convert[time[-1]]
    except:
        return time


class CoastalGuideCMD(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logger.info("RealmCMD: Cog Loaded!")

    @commands.command()
    @check_Coastal()
    async def guide(self, ctx):
        guild = self.bot.get_guild(config['Coastal'])
        print(guild)
        role = guild.get_role(933398341457428620)
        print(role)
        responsechannel = guild.get_channel(517060711202160640)
        author = ctx.message.author
        channel = await ctx.author.create_dm()

        # Answer Check
        def check(m):
            return m.content is not None and m.channel == channel and m.author is not self.bot.user

        embed = discord.Embed(
            title="Season 8 Guide Agreement",
            description="Read the guide, and then answer the questions that follow.",
            color=0x336F75,
        )
        embed.add_field(
            name="Online version of the guide",
            value="https://bit.ly/CoastalPlayersGuide",
            inline=False,
        )
        embed.add_field(
            name="PDF version of the guide",
            value="https://bit.ly/Coastal8PGpdf",
            inline=False,
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/488792053002534920/933389051837415454/coastal_logo_final_s8.png"
        )
        await channel.send(embed=embed)
        await asyncio.sleep(5)

        question1 = "What should you speak to enter the Realm?"
        await channel.send(question1)
        await asyncio.sleep(2)
        answer1 = await self.bot.wait_for('message', timeout=60.0, check=check)
        while True:
            if answer1.content != str.casefold("friend"):
                prompt = "Wrong! Try again: "
                await channel.send(prompt)
                await asyncio.sleep(2)
                answer1 = await self.bot.wait_for('message', timeout=60.0, check=check)
            else:
                prompt = "Great Job!!!"
                await channel.send(prompt)
                break
        
        question2 = "Do you agree to the guide? Please answer yes or no."
        await channel.send(question2)
        await asyncio.sleep(2)
        answer2 = await self.bot.wait_for('message', timeout=60.0, check=check)            
        if answer2.content == str.casefold("yes"):
            prompt = "Great! Have fun Playing Coastal Craft 8: Coral Crown"
            await channel.send(prompt)
            await author.add_roles(role)
            await asyncio.sleep(2)

            embed = discord.Embed(title="Guide Agreement", description=author.name + "Has agreed to the guide", color=0x000800)
            embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/488792053002534920/933389051837415454/coastal_logo_final_s8.png")
            await responsechannel.send(embed=embed)
        else:
            prompt = "Please get with an OP to discuss your concerns"
            await channel.send(prompt)

    @guide.error
    async def guide_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.send("Uh oh, looks like you don't have the Moderator role!")

        else:
            raise error

async def setup(bot):
    await bot.add_cog(CoastalGuideCMD(bot))
