import os
from os import system
from logging import exception
import discord
from discord.ext import commands
from discord.commands import slash_command
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
    return str(len(str_list) + 1)


def entryid_number(sheet):
    str_list = list(filter(None, sheet.col_values(1)))
    return str(len(str_list) - 2)


scope = [
    "https://spreadsheets.google.com/feeds",
    'https://www.googleapis.com/auth/spreadsheets',
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

client = gspread.authorize(creds)

cmsheet = client.open("Coastal Markers")

overworldsheet = cmsheet.worksheet("Overworld")

nethersheet = cmsheet.worksheet("Nether")

endsheet = cmsheet.worksheet("End")

questionsheet = cmsheet.worksheet("Questions")

# ---CONSTANTS----------------------------------------------------

newmarkerrow = 2
entryidcol = 1
xcol = 2
ycol = 3
minmapzoomcol = 4
imagecol = 5
imageanchorcol = 6
text1col = 7
text2col = 8
text3col = 9
textcolorcol = 10
strokecolorcol = 11
offsetxcol = 12
offsetycol = 13
fontcol = 14
poidesc = questionsheet.acell("B1").value
Qtext1 = questionsheet.acell("B2").value
Qtext2 = questionsheet.acell("B3").value
Qtext3 = questionsheet.acell("B4").value
Qtextcolor = questionsheet.acell("B5").value
Qmarkertype = questionsheet.acell("B6").value

# -------------------------------------------------------


def check_Aurafall():
    def predicate(ctx):
        return ctx.guild.id == 298995889551310848 or ctx.guild.id == 448488274562908170

    return commands.check(predicate)


def check_Coastal():
    def predicate(ctx):
        return ctx.guild.id == 305767872410419211 or ctx.guild.id == 448488274562908170

    return commands.check(predicate)


def check_Coastal_MRP():
    def predicate(ctx):
        return ctx.guild.id == 305767872410419211 or ctx.guild.id == 448488274562908170 or ctx.guild.id == 587495640502763521

    return commands.check(predicate)


def convert(time):
    try:
        return int(time[:-1]) * time_convert[time[-1]]
    except:
        return time


class CoastalPOICMD(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logger.info("RealmCMD: Cog Loaded!")

    addpoi = discord.SlashCommandGroup(
        name="addpoi",
        description="Add a point of interest to the map",
        guild_ids=[config['PBtest'], config['Coastal']])

    @addpoi.command(description="Add a POI to the Overworld")
    async def overworld(self, ctx, x_coord: int, z_coord: int):
        responseguild = self.bot.get_guild(config['Coastal'])
        responseChannel = responseguild.get_channel(
            config['CoastalMapUpdates'])
        admin = responseguild.get_role(config['CoastalOPTeam'])
        channel = ctx.channel
        author = ctx.author
        currentsheet = overworldsheet
        entryID = (int(currentsheet.acell('A2').value) + 1)
        print(entryID)
        dname = str(author.name + '#' + author.discriminator)
        if author.nick == None:
            dnick = str(author.name)
        else:
            dnick = str(author.nick)
        # Answer Check
        def check(m):
            return m.content is not None and m.channel == channel and m.author == author

        # Questions
        introem = discord.Embed(title="New POI Entry",
                                description=poidesc +
                                "\n**Questions will start in 3 seconds.**",
                                color=0x336F75)
        await channel.send(embed=introem)
        await asyncio.sleep(3)

        await channel.send(Qtext1)
        answer1 = await self.bot.wait_for('message', check=check)
        await asyncio.sleep(.5)

        await channel.send(Qtext2)
        answer2 = await self.bot.wait_for('message', check=check)
        await asyncio.sleep(.5)

        await channel.send(Qtext3)
        answer3 = await self.bot.wait_for('message', check=check)
        await asyncio.sleep(.5)

        await channel.send(Qtextcolor)
        answer4 = await self.bot.wait_for('message', check=check)
        await asyncio.sleep(.5)

        await channel.send(Qmarkertype)
        answer5 = await self.bot.wait_for('message', check=check)
        await asyncio.sleep(.5)
        # Spreadsheet Data
        if answer2.content == "no" or answer2.content == "No":
            text2content = ""
        else:
            text2content = answer2.content

        if answer3.content == "no" or answer3.content == "No":
            text3content = ""
        else:
            text3content = answer3.content

        if answer5.content == "base" or answer5.content == "Base":
            font = "900 8px 'Font Awesome 6 Free'"
        elif answer5.content == "shop" or answer5.content == "Shop":
            font = "900 10px 'Font Awesome 6 Free'"
        elif answer5.content == "portal" or answer5.content == "Portal":
            font = "900 12px 'Font Awesome 6 Free'"
        else:
            font = "900 8px 'Font Awesome 6 Free'"

        row = [
            entryID, x_coord, z_coord, "-1", "", "", answer1.content,
            text2content, text3content, answer4.content, "#ffffff", "0", "0",
            font
        ]
        currentsheet.insert_row(row, 2, value_input_option='USER_ENTERED')

        await ctx.send("Success!")

        # Actual Embed with Responses
        embed1 = discord.Embed(
            title="New POI Entered",
            description="From\nDiscord - " + dname + "\nAKA - " + dnick +
            "\n============================================",
            color=0x336F75)
        embed1.set_thumbnail(
            url=
            "https://cdn.discordapp.com/attachments/488792053002534920/933389051837415454/coastal_logo_final_s8.png"
        )
        embed1.add_field(name="X_Coord", value=str(x_coord), inline=True)
        embed1.add_field(name="Z_Coord", value=str(z_coord), inline=True)
        embed1.add_field(name="Marker Type",
                         value=str(answer5.content),
                         inline=True)
        embed1.add_field(name="Text Line 1",
                         value=str(answer1.content),
                         inline=False)
        embed1.add_field(name="Text Line 2",
                         value=str(answer2.content),
                         inline=False)
        embed1.add_field(name="Text Line 3",
                         value=str(answer3.content),
                         inline=False)

        await responseChannel.send(admin.mention)
        await responseChannel.send(embed=embed1)

    @addpoi.command(description="Add a POI to the Nether")
    async def nether(self, ctx, x_coord: int, z_coord: int):
        responseguild = self.bot.get_guild(config['Coastal'])
        responseChannel = responseguild.get_channel(
            config['CoastalMapUpdates'])
        admin = responseguild.get_role(config['CoastalOPTeam'])
        channel = ctx.channel
        author = ctx.author
        currentsheet = nethersheet
        entryID = (int(currentsheet.acell('A2').value) + 1)
        print(entryID)
        dname = str(author.name + '#' + author.discriminator)
        if author.nick == None:
            dnick = str(author.name)
        else:
            dnick = str(author.nick)
        # Answer Check
        def check(m):
            return m.content is not None and m.channel == channel and m.author == author

        # Questions
        introem = discord.Embed(title="New POI Entry",
                                description=poidesc +
                                "\n**Questions will start in 3 seconds.**",
                                color=0x336F75)
        await channel.send(embed=introem)
        await asyncio.sleep(3)

        await channel.send(Qtext1)
        answer1 = await self.bot.wait_for('message', check=check)
        await asyncio.sleep(.5)

        await channel.send(Qtext2)
        answer2 = await self.bot.wait_for('message', check=check)
        await asyncio.sleep(.5)

        await channel.send(Qtext3)
        answer3 = await self.bot.wait_for('message', check=check)
        await asyncio.sleep(.5)

        await channel.send(Qtextcolor)
        answer4 = await self.bot.wait_for('message', check=check)
        await asyncio.sleep(.5)

        await channel.send(Qmarkertype)
        answer5 = await self.bot.wait_for('message', check=check)
        await asyncio.sleep(.5)
        # Spreadsheet Data
        if answer2.content == "no" or answer2.content == "No":
            text2content = ""
        else:
            text2content = answer2.content

        if answer3.content == "no" or answer3.content == "No":
            text3content = ""
        else:
            text3content = answer3.content

        if answer5.content == "base" or answer5.content == "Base":
            font = "900 8px 'Font Awesome 6 Free'"
        elif answer5.content == "shop" or answer5.content == "Shop":
            font = "900 10px 'Font Awesome 6 Free'"
        elif answer5.content == "portal" or answer5.content == "Portal":
            font = "900 12px 'Font Awesome 6 Free'"
        else:
            font = "900 8px 'Font Awesome 6 Free'"

        row = [
            entryID, x_coord, z_coord, "-1", "", "", answer1.content,
            text2content, text3content, answer4.content, "#ffffff", "0", "0",
            font
        ]
        currentsheet.insert_row(row, 2, value_input_option='USER_ENTERED')

        await ctx.send("Success!")

        # Actual Embed with Responses
        embed1 = discord.Embed(
            title="New POI Entered",
            description="From\nDiscord - " + dname + "\nAKA - " + dnick +
            "\n============================================",
            color=0x336F75)
        embed1.set_thumbnail(
            url=
            "https://cdn.discordapp.com/attachments/488792053002534920/933389051837415454/coastal_logo_final_s8.png"
        )
        embed1.add_field(name="X_Coord", value=str(x_coord), inline=True)
        embed1.add_field(name="Z_Coord", value=str(z_coord), inline=True)
        embed1.add_field(name="Marker Type",
                         value=str(answer5.content),
                         inline=True)
        embed1.add_field(name="Text Line 1",
                         value=str(answer1.content),
                         inline=False)
        embed1.add_field(name="Text Line 2",
                         value=str(answer2.content),
                         inline=False)
        embed1.add_field(name="Text Line 3",
                         value=str(answer3.content),
                         inline=False)

        await responseChannel.send(admin.mention)
        await responseChannel.send(embed=embed1)

    @addpoi.command(description="Add a POI to the End")
    async def end(self, ctx, x_coord: int, z_coord: int):
        responseguild = self.bot.get_guild(config['Coastal'])
        responseChannel = responseguild.get_channel(
            config['CoastalMapUpdates'])
        admin = responseguild.get_role(config['CoastalOPTeam'])
        channel = ctx.channel
        author = ctx.author
        currentsheet = endsheet
        entryID = (int(currentsheet.acell('A2').value) + 1)
        print(entryID)
        dname = str(author.name + '#' + author.discriminator)
        if author.nick == None:
            dnick = str(author.name)
        else:
            dnick = str(author.nick)
        # Answer Check
        def check(m):
            return m.content is not None and m.channel == channel and m.author == author

        # Questions
        introem = discord.Embed(title="New POI Entry",
                                description=poidesc +
                                "\n**Questions will start in 3 seconds.**",
                                color=0x336F75)
        await channel.send(embed=introem)
        await asyncio.sleep(3)

        await channel.send(Qtext1)
        answer1 = await self.bot.wait_for('message', check=check)
        await asyncio.sleep(.5)

        await channel.send(Qtext2)
        answer2 = await self.bot.wait_for('message', check=check)
        await asyncio.sleep(.5)

        await channel.send(Qtext3)
        answer3 = await self.bot.wait_for('message', check=check)
        await asyncio.sleep(.5)

        await channel.send(Qtextcolor)
        answer4 = await self.bot.wait_for('message', check=check)
        await asyncio.sleep(.5)

        await channel.send(Qmarkertype)
        answer5 = await self.bot.wait_for('message', check=check)
        await asyncio.sleep(.5)
        # Spreadsheet Data
        if answer2.content == "no" or answer2.content == "No":
            text2content = ""
        else:
            text2content = answer2.content

        if answer3.content == "no" or answer3.content == "No":
            text3content = ""
        else:
            text3content = answer3.content

        if answer5.content == "base" or answer5.content == "Base":
            font = "900 8px 'Font Awesome 6 Free'"
        elif answer5.content == "shop" or answer5.content == "Shop":
            font = "900 10px 'Font Awesome 6 Free'"
        elif answer5.content == "portal" or answer5.content == "Portal":
            font = "900 12px 'Font Awesome 6 Free'"
        else:
            font = "900 8px 'Font Awesome 6 Free'"

        row = [
            entryID, x_coord, z_coord, "-1", "", "", answer1.content,
            text2content, text3content, answer4.content, "#ffffff", "0", "0",
            font
        ]
        currentsheet.insert_row(row, 2, value_input_option='USER_ENTERED')

        await ctx.send("Success!")

        # Actual Embed with Responses
        embed1 = discord.Embed(
            title="New POI Entered",
            description="From\nDiscord - " + dname + "\nAKA - " + dnick +
            "\n============================================",
            color=0x336F75)
        embed1.set_thumbnail(
            url=
            "https://cdn.discordapp.com/attachments/488792053002534920/933389051837415454/coastal_logo_final_s8.png"
        )
        embed1.add_field(name="X_Coord", value=str(x_coord), inline=True)
        embed1.add_field(name="Z_Coord", value=str(z_coord), inline=True)
        embed1.add_field(name="Marker Type",
                         value=str(answer5.content),
                         inline=True)
        embed1.add_field(name="Text Line 1",
                         value=str(answer1.content),
                         inline=False)
        embed1.add_field(name="Text Line 2",
                         value=str(answer2.content),
                         inline=False)
        embed1.add_field(name="Text Line 3",
                         value=str(answer3.content),
                         inline=False)

        await responseChannel.send(admin.mention)
        await responseChannel.send(embed=embed1)

    @addpoi.error
    async def addpoi_error(self, ctx, error):
        if isinstance(error, commands.ExtensionFailed):
            print(
                "\n\n\nBLOCKED BY GOOGLE SHEETS RATE LIMITS\nRESTARTING NOW\n\n\n"
            )
            system('kill 1')
        else:
            raise error


def setup(bot):
    bot.add_cog(CoastalPOICMD(bot))
