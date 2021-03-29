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
    "AurafallRealmApplications").sheet1

# ---CONSTANTS----------------------------------------------------

appinforow = 1
apptitlecol = 1
appdesccol = 2
appRPGtitlecol = 3
appRPGdesccol = 4
appTYtitlecol = 5
appTYdesccol = 6
apptitle = sheet.cell(appinforow,apptitlecol).value
appdesc = sheet.cell(appinforow,appdesccol).value
appRPGtitle = sheet.cell(appinforow,appRPGtitlecol).value
appRPGdesc = sheet.cell(appinforow,appRPGdesccol).value
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
rpgq1col = 13
rpgq2col = 14
rpgq3col = 15
Qgamertag = sheet.cell(questionrow,gamertagcol).value
Qcountry = sheet.cell(questionrow,countrycol).value
Qage = sheet.cell(questionrow,agecol).value
Qplatform = sheet.cell(questionrow,platformcol).value
Question1 = sheet.cell(questionrow,q1col).value
Question2 = sheet.cell(questionrow,q2col).value
Question3 = sheet.cell(questionrow,q3col).value
Qrule = sheet.cell(questionrow,rulecol).value
Qrpg1 = sheet.cell(questionrow,rpgq1col).value
Qrpg2 = sheet.cell(questionrow,rpgq2col).value
Qrpg3 = sheet.cell(questionrow,rpgq3col).value

# -------------------------------------------------------

def check_Aurafall():
    def predicate(ctx):
        return ctx.message.guild.id == 298995889551310848 or ctx.message.guild.id == 448488274562908170
    return commands.check(predicate)


def check_Coastal():
    def predicate(ctx):
        return ctx.message.guild.id == 305767872410419211 or ctx.message.guild.id == 448488274562908170
    return commands.check(predicate)

def convert(time):
    try:
        return int(time[:-1]) * time_convert[time[-1]]
    except:
        return time


class RealmCMD(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logger.info("RealmCMD: Cog Loaded!")

    @commands.command()
    async def applyrealm(self, ctx):
        # Prior defines
        timestamp = datetime.now()
        channel2 = ctx.message.channel
        author = ctx.message.author
        channel = await ctx.author.create_dm()
        guild = ctx.message.guild
        responseChannel = self.bot.get_channel(config['AurafallApplications'])
        admin = discord.utils.get(
            ctx.guild.roles, name="Realm Developer")

        # Elgibilty Checks
     
        # Channel Check

        if channel2.name != "the-innkeeper":
            await ctx.channel.purge(limit=1)
            noGoAway = discord.Embed(title="Woah Woah Woah, Slow Down There Buddy!",
                                     description="Tell it to the Inn Keeper, no one here wants to hear it!", color=0x20F6B3)
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

        rpgem = discord.Embed(title=appRPGtitle, description=appRPGdesc + "\n**Questions will start in 5 seconds.**", color=0x20F6B3)
        await channel.send(embed=rpgem)
        time.sleep(5)

        await channel.send(Qrpg1)
        answer9 = await self.bot.wait_for('message', check=check)

        await channel.send(Qrpg2)
        answer10 = await self.bot.wait_for('message', check=check)

        await channel.send(Qrpg3)
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
            url="https://cdn.discordapp.com/attachments/825055185633017876/825055299139534868/Aurafall_Logo_Color_No_Text.png")
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
        embed2 = discord.Embed(title=appRPGtitle, description=appRPGdesc + "\n============================================", color=0x20F6B3)        
        embed2.add_field(name=Qrpg1,
                        value=str(answer9.content), inline=False)
        embed2.add_field(name=Qrpg2,
                        value=str(answer10.content), inline=False)
        embed2.add_field(name=Qrpg3,
                        value=str(answer11.content), inline=False)
        embed2.add_field(name="__**Reaction Codes**__",
                        value="Please react with the following codes to show your thoughts on this applicant.", inline=False)
        embed2.add_field(name="----💚----", value="Approved", inline=True)
        embed2.add_field(name="----💛----",
                        value="RPG Scenario", inline=True)
        embed2.add_field(name="----❤️----", value="Rules/Info", inline=True)
        embed2.add_field(name="----🖤----", value="Denied", inline=True)
        embed2.set_footer(text="Application #" + str(entryID) + " | " + submittime)
        await responseChannel.send(admin.mention)
        msg1 = await responseChannel.send(embed=embed1)
        msg2 = await responseChannel.send(embed=embed2)

        # Reaction Appending
        reactions = ['💚', '💛', '❤️', '🖤']
        for emoji in reactions:
            await msg2.add_reaction(emoji)

        # Confirmation
        response = discord.Embed(
            title=appTYtitle, description=appTYdesc, color=0x20F6B3)
        await channel.send(embed=response)

    @applyrealm.error
    async def applyrealm_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Uh oh, looks like I can't execute this command because you don't have permissions!")

        if isinstance(error, commands.TooManyArguments):
            await ctx.send("You sent too many arguments! Did you use quotes for realm names over 2 words?")

        if isinstance(error, commands.CheckFailure):
            await ctx.send("This Command was not designed for this server!")

        else:
            raise error 
    
    @commands.command()
    @check_Aurafall()
    async def applymrpcr(self ,ctx):
        timestamp = datetime.now()
        channel2 = ctx.message.channel
        author = ctx.message.author
        channel = await ctx.author.create_dm()
        guild = ctx.message.guild
        responseChannel = self.bot.get_channel(config['realmApplyResponse'])

        # Elgibilty Checks
        '''
    Channel Check
    '''
        if channel2.name != "bot-spam":
            await ctx.channel.purge(limit=1)
            noGoAway = discord.Embed(title="Woah Woah Woah, Slow Down There Buddy!",
                                     description="Please switch to #bot-spam! This command is not allowed to be used here.", color=0xfc0b03)
            await ctx.send(embed=noGoAway, delete_after=6)
            return

        '''
    Level Check
    '''
        JustSpawnedCheck = discord.utils.get(
            ctx.guild.roles, name="Just Spawned")
        SpiderSniperCheck = discord.utils.get(
            ctx.guild.roles, name="Spider Sniper")
        if JustSpawnedCheck in author.roles or SpiderSniperCheck in author.roles:
            noGoAway = discord.Embed(title="Woah Woah Woah, Slow Down There Buddy!",
                                     description="I appreciate you trying to apply towards MRPCR here but you must have the `Zombie Slayer` role or have surpassed this role! \n*Please try again when you have reached this role.*", color=0xfc0b03)
            await ctx.send(embed=noGoAway)
            return

        await ctx.send("Please check your DMs!")

        # Answer Check
        def check(m):
            return m.content is not None and m.channel == channel and m.author is not self.bot.user
        
        intro = discord.Embed(title="MRPCR Realm Application", description="Hello! Please make sure you fill every question with a good amount of detail and if at any point you feel like you made a mistake, you will see a cancel reaction at the end. Then you can come back and re-answer your questions! \n**Questions will start in 5 seconds.**", color=0x42f5f5)
        await channel.send(embed=intro)
        time.sleep(5)

        answer1 = str(author.name) + "#" + str(author.discriminator)
        answer2 = str(author.id)

        await channel.send("Gamertag:")
        answer3 = await self.bot.wait_for('message', check=check)

        await channel.send("Age:")
        answer4= await self.bot.wait_for('message', check=check)

        await channel.send("Tell us about yourself and what you love about Minecraft.")
        answer5 = await self.bot.wait_for('message', check=check)

        message = await channel.send("**That's it!**\n\nReady to submit?\n✅ - SUBMIT\n❌ - CANCEL\n*You have 300 seconds to react, otherwise the application will automatically cancel.* ")
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
                await ctx.send("Standby...")
                await message.delete()
            else:
                await ctx.send("Ended Application...")
                await message.delete()
                return

        submittime = str(timestamp.strftime(r"%x"))

        # Spreadsheet Data
        row = [answer1.content, answer2.content, answer3.content, answer4.content, answer5.content,submittime]
        sheet2.insert_row(row, 2)

        # Actual Embed with Responses
        embed = discord.Embed(title="New MRPCR Application!", description="Response turned in by: " +
                              author.mention, color=0x03fc28)
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/588034623993413662/588413853667426315/Portal_Design.png")
        embed.add_field(name="__**Discord Name:**__",value=str(answer1.content), inline=True)
        embed.add_field(name="__**Gamertag:**__",value=str(answer2.content), inline=True)
        embed.add_field(name="__**Age:**__", value=str(answer3.content), inline=False)
        embed.add_field(name="__**Tell us about yourself and what you love about Minecraft.**__", value=str(answer4.content), inline=False)
        embed.add_field(name = "__**Timestamp:**__", value = str(timestamp.strftime(r"%x")))

        embed.add_field(name="__**Reaction Codes**__",value="Please react with the following codes to show your thoughts on this applicant.", inline=False)
        embed.add_field(name="----💚----", value="Approved", inline=True)
        embed.add_field(name="----💛----",value="More Time in Server", inline=True)
        embed.add_field(name="----❤️----", value="Rejected", inline=True)
        embed.set_footer(text="Realm Application | " + submittime)
        msg = await responseChannel.send(embed=embed)

        # Reaction Appending
        reactions = ['💚', '💛', '❤️']
        for emoji in reactions:
            await msg.add_reaction(emoji)

        # Confirmation
        response = discord.Embed(
            title="Success!", description="I have sent in your application, you will hear back if you have passed!", color=0x03fc28)
        await channel.send(embed=response)




def setup(bot):
    bot.add_cog(RealmCMD(bot))
