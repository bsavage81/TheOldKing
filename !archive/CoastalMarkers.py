from logging import exception
import discord
from discord import app_commands
from discord.commands.core import slash_command
from discord.ext import commands
import xbox
from discord.ui import InputText, Modal
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

def next_available_row(overworldsheet):
    str_list = list(filter(None, overworldsheet.col_values(1)))
    return str(len(str_list)+1)

def entryid_number(overworldsheet):
    str_list = list(filter(None, overworldsheet.col_values(1)))
    return str(len(str_list)-2)

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

client = gspread.authorize(creds)

cmsheet = client.open("Coastal Markers")

overworldsheet = cmsheet.worksheet(
    "Overworld")

nethersheet = cmsheet.worksheet(
    "Nether")

endsheet = cmsheet.worksheet(
    "End")


# ---CONSTANTS----------------------------------------------------

appinforow = 1
apptitlecol = 1
appdesccol = 2
appreftitlecol = 3
apprefdesccol = 4
appTYtitlecol = 5
appTYdesccol = 6
apptitle = overworldsheet.cell(appinforow,apptitlecol).value
appdesc = overworldsheet.cell(appinforow,appdesccol).value
appreftitle = overworldsheet.cell(appinforow,appreftitlecol).value
apprefdesc = overworldsheet.cell(appinforow,apprefdesccol).value
appTYtitle = overworldsheet.cell(appinforow,appTYtitlecol).value
appTYdesc = overworldsheet.cell(appinforow,appTYdesccol).value


questionrow = 2
entryidcol = 1
discordnamecol = 2
discordnickcol = 3
longidcol = 4
gamertagcol = 5
countrycol = 6
agecol = 7
gendercol = 8
platformcol = 9
q1col = 10
q2col = 11
q3col = 12
rulecol = 13
refq1col = 14
refq2col = 15
refq3col = 16
Qgamertag = overworldsheet.cell(questionrow,gamertagcol).value
Qcountry = overworldsheet.cell(questionrow,countrycol).value
Qage = overworldsheet.cell(questionrow,agecol).value
Qgender = overworldsheet.cell(questionrow,gendercol).value
Qplatform = overworldsheet.cell(questionrow,platformcol).value
Question1 = overworldsheet.cell(questionrow,q1col).value
Question2 = overworldsheet.cell(questionrow,q2col).value
Question3 = overworldsheet.cell(questionrow,q3col).value
Qrule = overworldsheet.cell(questionrow,rulecol).value
Qref1 = overworldsheet.cell(questionrow,refq1col).value
Qref2 = overworldsheet.cell(questionrow,refq2col).value
Qref3 = overworldsheet.cell(questionrow,refq3col).value

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


class MyModal(Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.add_item(InputText(label="Short Input", placeholder="Placeholder Test"))

        self.add_item(
            InputText(
                label="Longer Input",
                value="Longer Value\nSuper Long Value",
                style=discord.InputTextStyle.long,
            )
        )

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Your Modal Results", color=discord.Color.random())
        embed.add_field(name="First Input", value=self.children[0].value, inline=False)
        embed.add_field(name="Second Input", value=self.children[1].value, inline=False)
        await interaction.response.send_message(embeds=[embed])

class CoastalMarkersCMD(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logger.info("RealmCMD: Cog Loaded!")

    @app_commands.command(name="modaltest", guild_ids=[config['PBtest']])
    async def modal_slash(self, ctx):
        """Shows an example of a modal dialog being invoked from a slash command."""
        modal = MyModal(title="Slash Command Modal")
        await ctx.interaction.response.send_modal(modal)


async def setup(bot):
    await bot.add_cog(CoastalMarkersCMD(bot))
