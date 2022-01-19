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
        return ctx.message.guild.id == 298995889551310848 or ctx.message.guild.id == 448488274562908170
    return commands.check(predicate)

def check_Coastal():
    def predicate(ctx):
        return ctx.message.guild.id == 305767872410419211 or ctx.message.guild.id == 448488274562908170
    return commands.check(predicate)

def check_Coastal_MRP():
    def predicate(ctx):
        return ctx.message.guild.id == 305767872410419211 or ctx.message.guild.id == 448488274562908170 or ctx.message.guild.id == 587495640502763521
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
    @commands.check_Coastal()
    async def guide(self, ctx, user: discord.User, *, message=None):
        message = message or "This Message is sent via DM"
        author = ctx.message.author
        await user.send(message)
        #await user.send("Sent by: " + author.name)

    @guide.error
    async def guide_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.send("Uh oh, looks like you don't have the Moderator role!")



def setup(bot):
    bot.add_cog(CoastalGuideCMD(bot))
