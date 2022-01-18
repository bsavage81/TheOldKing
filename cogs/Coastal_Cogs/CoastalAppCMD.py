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

appinforow = 1
apptitlecol = 1
appdesccol = 2
appreftitlecol = 3
apprefdesccol = 4
appTYtitlecol = 5
appTYdesccol = 6
apptitle = sheet.cell(appinforow,apptitlecol).value
appdesc = sheet.cell(appinforow,appdesccol).value
appreftitle = sheet.cell(appinforow,appreftitlecol).value
apprefdesc = sheet.cell(appinforow,apprefdesccol).value
appTYtitle = sheet.cell(appinforow,appTYtitlecol).value
appTYdesc = sheet.cell(appinforow,appTYdesccol).value


questionrow = 2
entryidcol = 1
discordnamecol = 2
discordnickcol = 3
longidcol = 4
gamertagcol = 5
countrycol = 6
agecol = 7
platformcol = 8
q1col = 9
q2col = 10
q3col = 11
rulecol = 12
refq1col = 13
refq2col = 14
refq3col = 15
Qgamertag = sheet.cell(questionrow,gamertagcol).value
Qcountry = sheet.cell(questionrow,countrycol).value
Qage = sheet.cell(questionrow,agecol).value
Qplatform = sheet.cell(questionrow,platformcol).value
Question1 = sheet.cell(questionrow,q1col).value
Question2 = sheet.cell(questionrow,q2col).value
Question3 = sheet.cell(questionrow,q3col).value
Qrule = sheet.cell(questionrow,rulecol).value
Qref1 = sheet.cell(questionrow,refq1col).value
Qref2 = sheet.cell(questionrow,refq2col).value
Qref3 = sheet.cell(questionrow,refq3col).value

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


class CoastalAppCMD(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logger.info("RealmCMD: Cog Loaded!")

    @commands.command()
    @check_Coastal_MRP()
    async def applycoastal(self, ctx):
        # Prior defines
        timestamp = datetime.now()
        channel2 = ctx.message.channel
        author = ctx.message.author
        channel = await ctx.author.create_dm()
        guild = ctx.message.guild
        responseChannel = self.bot.get_channel(config['AurafallApplications'])
        admin = discord.utils.get(
            ctx.guild.roles, name="OP Team")

        # Elgibilty Checks
     
        # Channel Check

        #Coastal Craft channel id - 587628369672142848

        if channel2.id != 824746716967600199:
            await ctx.channel.purge(limit=1)
            noGoAway = discord.Embed(title="Woah Woah Woah, Slow Down There Buddy!",
                                     description="This belongs over in Coastal Craft, no one here wants to hear it here!", color=0x20F6B3)
            await ctx.send(embed=noGoAway, delete_after=6)
            return

        await ctx.send("Check your DMs")

        # Answer Check
        def check(m):
            return m.content is not None and m.channel == channel and m.author is not self.bot.user

        # Questions
        introem = discord.Embed(title=apptitle, description=appdesc + "\n**Questions will start in 5 seconds.**", color=0x20F6B3)
        await channel.send(embed=introem)
        time.sleep(5)
        await channel.send(Qgamertag)
        answer1 = await self.bot.wait_for('message', check=check)

        await channel.send(Qcountry)
        answer2 = await self.bot.wait_for('message', check=check)

        await channel.send(Qage)
        answer3 = await self.bot.wait_for('message', check=check)

        await channel.send(Qplatform)
        answer4 = await self.bot.wait_for('message', check=check)

        await channel.send(Question1)
        answer5 = await self.bot.wait_for('message', check=check)

        await channel.send(Question2)
        answer6 = await self.bot.wait_for('message', check=check)

        await channel.send(Question3)
        answer7 = await self.bot.wait_for('message', check=check)

        await channel.send(Qrule)
        answer8 = await self.bot.wait_for('message', check=check)

        refem = discord.Embed(title=appreftitle, description=apprefdesc + "\n**Questions will start in 5 seconds.**", color=0x20F6B3)
        await channel.send(embed=refem)
        time.sleep(5)

        await channel.send(Qref1)
        answer9 = await self.bot.wait_for('message', check=check)

        await channel.send(Qref2)
        answer10 = await self.bot.wait_for('message', check=check)

        await channel.send(Qref3)
        answer11 = await self.bot.wait_for('message', check=check)

        message = await channel.send("**That's it!**\n\nReady to submit?\n✅ - SUBMIT\n❌ - CANCEL\n*You have 300 seconds to react, otherwise the application will automatically cancel. ")
        reactions = ['✅', '❌']
        for emoji in reactions:
            await message.add_reaction(emoji)

        def check2(reaction, user):
            return user == ctx.author and (str(reaction.emoji) == '✅' or str(reaction.emoji) == '❌')
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=300.0, check=check2)

        except asyncio.TimeoutError:
            await channel.send("Looks like you didn't react in time, please try again later!")

        else:
            if str(reaction.emoji) == "✅":
                await channel.send("Standby...")
                await message.delete()
            else:
                await channel.send("Ended Application...")
                await message.delete()
                return

        submittime = timestamp.strftime("%m/%d/%Y %H:%M:%S")
        entryID = (int(sheet.acell('A3').value)+1)
        print(entryID)
        dname = str(author.name + '#' + author.discriminator)
        if author.nick == None:
            dnick = str(author.name)
        else:
            dnick = str(author.nick)
        longid = str(author.id)
        #

        # Spreadsheet Data
        row = [entryID, dname, dnick, longid, answer1.content, answer2.content, answer3.content, answer4.content,
               answer5.content, answer6.content, answer7.content, answer8.content, answer9.content, answer10.content, answer11.content, submittime]
        sheet.insert_row(row, 3, value_input_option='USER_ENTERED')

        # Actual Embed with Responses
        embed1 = discord.Embed(title="Realm Application", description="From\nDiscord - " +
                              dname + "\nAKA - " + dnick + "\nLong ID - " + longid + "\n============================================", color=0x20F6B3)
        embed1.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/488792053002534920/732271833121947738/Coastal_logo_final_s7.png")
        embed1.add_field(name=Qgamertag,
                        value=str(answer1.content), inline=True)
        embed1.add_field(name=Qcountry,
                        value=str(answer2.content), inline=True)
        embed1.add_field(name=Qage,
                        value=str(answer3.content), inline=True)
        embed1.add_field(name=Qplatform,
                        value=str(answer4.content), inline=False)
        embed1.add_field(name=Question1,
                        value=str(answer5.content), inline=False)
        embed1.add_field(name=Question2,
                        value=str(answer6.content), inline=False)
        embed1.add_field(name=Question3,
                        value=str(answer7.content), inline=False)
        embed1.add_field(name=Qrule,
                        value=str(answer8.content), inline=False)
        embed2 = discord.Embed(title=appreftitle, description=apprefdesc + "\n============================================", color=0x20F6B3)        
        embed2.add_field(name=Qref1,
                        value=str(answer9.content), inline=False)
        embed2.add_field(name=Qref2,
                        value=str(answer10.content), inline=False)
        embed2.add_field(name=Qref3,
                        value=str(answer11.content), inline=False)
        embed2.add_field(name="__**Reaction Codes**__",
                        value="Please react with the following codes to show your thoughts on this applicant.", inline=False)
        embed2.add_field(name="----💚----", value="Approved", inline=True)
        embed2.add_field(name="----💛----",
                        value="Not Sure", inline=True)
        embed2.add_field(name="----❤️----", value="Denied", inline=True)
        embed2.set_footer(text="Application #" + str(entryID) + " | " + submittime)
        await responseChannel.send(admin.mention)
        msg1 = await responseChannel.send(embed=embed1)
        msg2 = await responseChannel.send(embed=embed2)

        # Reaction Appending
        reactions = ['💚', '💛', '❤️']
        for emoji in reactions:
            await msg2.add_reaction(emoji)

        # Confirmation
        response = discord.Embed(
            title=appTYtitle, description=appTYdesc, color=0x20F6B3)
        await channel.send(embed=response)

    @applycoastal.error
    async def applycoastal_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Uh oh, looks like I can't execute this command because you don't have permissions!")

        if isinstance(error, commands.TooManyArguments):
            await ctx.send("You sent too many arguments! Did you use quotes for realm names over 2 words?")

        if isinstance(error, commands.CheckFailure):
            await ctx.send("This Command was not designed for this server!")

        else:
            raise error 

def setup(bot):
    bot.add_cog(CoastalAppCMD(bot))
