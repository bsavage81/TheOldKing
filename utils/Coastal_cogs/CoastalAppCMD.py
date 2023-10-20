from logging import exception
import discord  
from discord.ext import commands    
from discord import app_commands
import time
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import asyncio
from core.common import load_config
from discord.ext.modal_paginator import ModalPaginator, PaginatorModal
from typing import Any, Dict, List

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

sheet = client.open("CCS9 Realm Application").sheet1

# ---CONSTANTS----------------------------------------------------

appinforow = 1
apptitlecol = 1
appdesccol = 2
appreftitlecol = 3
apprefdesccol = 4
appTYtitlecol = 5
appTYdesccol = 6
questiontitle1col = 7
questiontitle2col = 8
questiontitle3col = 9
apptitle = sheet.cell(appinforow, apptitlecol).value
appdesc = sheet.cell(appinforow, appdesccol).value
appreftitle = sheet.cell(appinforow, appreftitlecol).value
apprefdesc = sheet.cell(appinforow, apprefdesccol).value
appTYtitle = sheet.cell(appinforow, appTYtitlecol).value
appTYdesc = sheet.cell(appinforow, appTYdesccol).value
questiontitle1 = sheet.cell(appinforow, questiontitle1col).value
questiontitle2 = sheet.cell(appinforow, questiontitle2col).value
questiontitle3 = sheet.cell(appinforow, questiontitle3col).value

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
q4col = 13
q5col = 14
rule1col = 15
rule2col = 16
refq1col = 17
refq2col = 18
refq3col = 19
Qgamertag = sheet.cell(questionrow, gamertagcol).value
Qcountry = sheet.cell(questionrow, countrycol).value
Qage = sheet.cell(questionrow, agecol).value
Qgender = sheet.cell(questionrow, gendercol).value
Qplatform = sheet.cell(questionrow, platformcol).value
Question1 = sheet.cell(questionrow, q1col).value
Question2 = sheet.cell(questionrow, q2col).value
Question3 = sheet.cell(questionrow, q3col).value
Question4 = sheet.cell(questionrow, q4col).value
Question5 = sheet.cell(questionrow, q5col).value
Qrule1 = sheet.cell(questionrow, rule1col).value
Qrule2 = sheet.cell(questionrow, rule2col).value
Qref1 = sheet.cell(questionrow, refq1col).value
Qref2 = sheet.cell(questionrow, refq2col).value
Qref3 = sheet.cell(questionrow, refq3col).value

# -------------------------------------------------------
personal_questions = {
    "title": questiontitle1,
    "required": True,
    "questions": [
        Qgamertag,
        Qcountry,
        Qage,
        Qgender,
        Qplatform ,
    ],
}
misc_questions = {
    "title": questiontitle2,
    "required": True,
    "questions": [
        Question1,
        Question2,
        Question3,
        Question4,
        Question5,
    ],
}
reason_questions = {
    "title": questiontitle3,
    "required": True,
    "questions": [
        Qrule1,
        Qrule2,
        Qref1,
        Qref2,
        Qref3,
    ],
}
# -------------------------------------------------------


def convert(time):
    try:
        return int(time[:-1]) * time_convert[time[-1]]
    except:
        return time


class CoastalApplyModal(ModalPaginator):
    def __init__(self, bot, questions_inputs: List[Dict[str, Any]], *, author_id: int, **kwargs: Any) -> None:
        self.bot = bot
        # initialize the paginator with the the author_id kwarg
        # and any other kwargs we passed to the constructor.
        # possible kwargs are as follows:
        # timeout: Optional[int] = None - the timeout for the paginator (view)
        # disable_after: bool = True - whether to disable all buttons after the paginator is finished or cancelled.
        # can_go_back: bool = True - whether the user can go back to previous modals using the "Previous" button.
        # sort_modals: bool = True - whether to sort the modals by the required kwarg.
        # See more on the class.
        super().__init__(author_id=author_id, **kwargs)
        # iterate over the questions_inputs list
        for data in questions_inputs:
            # unpack the data from the dict
            title: str = data["title"]
            required: bool = data["required"]
            questions: List[str] = data["questions"]
            # create a new modal with the title and required kwarg
            modal = PaginatorModal(title=title, required=required)
            # add the questions to the modal
            for question in questions:
                modal.add_input(
                    label=question,  # the label of the text input
                    min_length=2,  # the minimum length of the text input
                    max_length=200,  # the maximum length of the text input
                    # see the discord.py docs for more info on the other kwargs
                )

            # add the modal to the paginator
            self.add_modal(modal)    

    # override the on_finish method to send the answers to the channel when the paginator is finished.
    async def on_finish(self, interaction: discord.Interaction[Any]) -> None:
        # you probably don't need to defer the response here.
        await interaction.response.defer()
        # call the original on_finish method
        # which will also disable the buttons
        await super().on_finish(interaction)

        # create a list of answers
        # default format: **Modal Title**\nQuestion: Answer\nQuestion: Answer\n... etc
        # Prior defines
        timestamp = datetime.now()
        author = interaction.user
        responseguild = self.bot.get_guild(config['Coastal'])
        print(responseguild)
        responseChannel = responseguild.get_channel(
            config['CoastalApplications'])
        admin = responseguild.get_role(config['CoastalOPTeam'])
        print(admin)
        print(responseChannel)

        titleslist: list[str] = []
        questionlist: list[str] = []
        answerlist: list[str] = []
        for modal in self.modals:
            titles = f"{modal.title}"
            field: discord.ui.TextInput[Any]
            for field in modal.children:  # type: ignore
                questions = f"{field.label}"
                answers = f"{field.value}"
                questionlist.append(questions)
                answerlist.append(answers)

            titleslist.append(titles)

        print(titleslist)
        print(questionlist)
        print(answerlist)

        submittime = timestamp.strftime("%m/%d/%Y %H:%M:%S")
        entryID = (int(sheet.acell('A3').value) + 1)
        print(entryID)
        dname = str(author.name + '#' + author.discriminator)
        if author.display_name == author.name:
            dnick = str(author.name)
        else:
            dnick = str(author.display_name)
        longid = str(author.id)
        #

        # Spreadsheet Data
        row = [
            entryID, dname, dnick, longid, str(answerlist[0]), str(answerlist[1]),
            str(answerlist[2]), str(answerlist[3]), str(answerlist[4]), str(answerlist[5]), str(answerlist[6]),
            str(answerlist[7]), str(answerlist[8]), str(answerlist[9]),
            str(answerlist[10]), str(answerlist[11]), str(answerlist[12]), str(answerlist[13]), str(answerlist[14]), submittime
        ]
        sheet.insert_row(row, 3, value_input_option='USER_ENTERED')

        # Actual Embed with Responses
        embed1 = discord.Embed(
            title="Realm Application",
            description="From\nDiscord - " + dname + "\nAKA - " + dnick +
            "\nLong ID - " + longid +
            "\n============================================",
            color=0x336F75)
        embed1.set_thumbnail(
            url=
            "https://cdn.discordapp.com/attachments/488792053002534920/1157338182392741999/coastal_logo_final_s9.png"
        )
        embed1.add_field(name=Qgamertag,
                         value=str(answerlist[0]),
                         inline=True)
        embed1.add_field(name=Qcountry,
                         value=str(answerlist[1]),
                         inline=True)
        embed1.add_field(name=Qage, value=str(answerlist[2]), inline=True)
        embed1.add_field(name=Qgender, value=str(answerlist[3]), inline=True)
        embed1.add_field(name=Qplatform,
                         value=str(answerlist[4]),
                         inline=False)
        embed1.add_field(name=Question1,
                         value=str(answerlist[5]),
                         inline=False)
        embed1.add_field(name=Question2,
                         value=str(answerlist[6]),
                         inline=False)
        embed1.add_field(name=Question3,
                         value=str(answerlist[7]),
                         inline=False)
        embed1.add_field(name=Question4,
                         value=str(answerlist[8]),
                         inline=False)
        embed1.add_field(name=Question5,
                         value=str(answerlist[9]),
                         inline=False)
        embed2 = discord.Embed(
            title=appreftitle,
            description=apprefdesc +
            "\n============================================",
            color=0x20F6B3)
        embed2.add_field(name=Qrule1, value=str(answerlist[10]), inline=False)
        embed2.add_field(name=Qrule2, value=str(answerlist[11]), inline=False)
        embed2.add_field(name=Qref1, value=str(answerlist[12]), inline=False)
        embed2.add_field(name=Qref2, value=str(answerlist[13]), inline=False)
        embed2.add_field(name=Qref3, value=str(answerlist[14]), inline=False)
        embed2.add_field(
            name="__**Reaction Codes**__",
            value=
            "Please react with the following codes to show your thoughts on this applicant.",
            inline=False)
        embed2.add_field(name="----💚----", value="Approved", inline=True)
        embed2.add_field(name="----💛----", value="Not Sure", inline=True)
        embed2.add_field(name="----❤️----", value="Denied", inline=True)
        embed2.set_footer(text="Application #" + str(entryID) + " | " +
                          submittime)
        await responseChannel.send(admin.mention)
        msg1 = await responseChannel.send(embed=embed1)
        msg2 = await responseChannel.send(embed=embed2)

        # Reaction Appending
        reactions = ['💚', '💛', '❤️']
        for emoji in reactions:
            await msg2.add_reaction(emoji)

        # Confirmation
        embed1 = discord.Embed(
            title="Realm Application Sent",
            description=f"{interaction.user.mention}",
            color=0x336F75)
        embed1.add_field(name=appTYtitle,
                         value=appTYdesc,
                         inline=False)

class CoastalAppCMD(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='applycoastal', description='Apply to the Coastal Craft Discord Server')
    @app_commands.guilds(config['MRP'])
    async def applycoastal(self, interaction: discord.Interaction[Any]):
        # initialize the paginator with all the questions data we defined above in a list
        # and the author_id so that only the command invoker can use the paginator.
        questions_inputs = [personal_questions, misc_questions, reason_questions]
        paginator = CoastalApplyModal(self.bot, questions_inputs, author_id=interaction.user.id)
        channel2 = interaction.channel
        
        if channel2.id != config['CoastalMRP']:
            await interaction.channel.purge(limit=1)
            noGoAway = discord.Embed(
                title="Woah Woah Woah, Slow Down There Buddy!",
                description=
                "This belongs over in Coastal Craft, no one here wants to hear it here!",
                color=0x20F6B3)
            await interaction.response.send_message(embed=noGoAway, delete_after=6)
            return

        # send the paginator to the current channel
        introem = discord.Embed(title=apptitle,
                                description=appdesc,
                                color=0x336F75)
        introem2 = discord.Embed(title=appreftitle,
                                description=apprefdesc,
                                color=0x336F75)
        await interaction.response.send_message(embeds=(introem,introem2))
        await paginator.send(interaction.channel)



    @applycoastal.error
    async def applycoastal_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(
                "Uh oh, looks like I can't execute this command because you don't have permissions!"
            )

        if isinstance(error, commands.TooManyArguments):
            await ctx.send(
                "You sent too many arguments! Did you use quotes for realm names over 2 words?"
            )

        if isinstance(error, commands.CheckFailure):
            await ctx.send("This Command was not designed for this server!")

        else:
            raise error

#-------------Approve Application Command--------------------------------------

    @app_commands.command(name="approveapp",
                   description="Approve an Application!")
    @app_commands.guilds(config['PBtest'], config['Coastal'])
    @app_commands.describe(
        appnumber="Application number to approve"
    ) 
    @commands.has_role("OP Team")
    async def approveapp(self, interaction: discord.Interaction, appnumber):
        # Status set to null
        DMStatus = "FALSE"
        author = interaction.user.id
        guild = interaction.guild
        mrpguild = self.bot.get_guild(config['MRP'])
        print(mrpguild)
        invitechannel = guild.get_channel(443614533815369728)
        print(invitechannel)
        invite = await invitechannel.create_invite(max_uses=1)
        print(invite.url)
        row = sheet.find(appnumber, in_column=1).row

        #get values from sheet
        userid = sheet.cell(row, 2).value
        print(userid)
        user = mrpguild.get_member_named(userid)
        if user is None:
            userlongid = sheet.cell(row, 4).value
            print(userlongid)
            user = mrpguild.get_member(userlongid)
            if user is None:
                user = await mrpguild.fetch_member(userlongid)
        print(user)

        sheet.update_cell(row, 18, 'Yes')

        DMStatus = "FAILED"
        embed = discord.Embed(title="Congratulations",
                              description="You made it to the next step!",
                              color=0x008000)
        embed.add_field(
            name="Welcome to Coastal Craft!!!",
            value=
            "In this step you need to join our Discord, tell us about yourself, get to know us, and if it is a good fit, the Realm invite will be the next step. We are glad to have you and hope you enjoy your time in Coastal Craft!",
            inline=False)
        embed.set_thumbnail(
            url=
            "https://cdn.discordapp.com/attachments/488792053002534920/1157338182392741999/coastal_logo_final_s9.png"
        )
        try:
            await user.send(embed=embed)
            await user.send(invite.url)
            DMStatus = "DONE"

        finally:
            embed = discord.Embed(title="Application " + appnumber +
                                  "  Approved",
                                  description="Approved by: " + author.mention,
                                  color=0x008000)
            embed.add_field(name="**Applicant**", value=user)
            embed.add_field(name="**Console Logs**",
                            value="**DMStatus:** " + DMStatus)
            embed.set_footer(text="The command has finished all of its tasks")
            embed.set_thumbnail(
                url=
                "https://cdn.discordapp.com/attachments/488792053002534920/1157338182392741999/coastal_logo_final_s9.png"
            )
            await interaction.response.send_message(embed=embed)

    @approveapp.error
    async def approveapp_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(
                "Uh oh, looks like I can't execute this command because you don't have permissions!"
            )

        if isinstance(error, commands.TooManyArguments):
            await ctx.send(
                "You sent too many arguments! Did you use quotes for realm names over 2 words?"
            )

        if isinstance(error, commands.CheckFailure):
            await ctx.send("This Command was not designed for this server!")

        elif isinstance(error, commands.BadArgument):
            await ctx.send("You didn't include all of the arguments!")

        else:
            raise error

#-------------Deny Application Command--------------------------------------

    @app_commands.command(name="denyapp",
                   description="Deny an Application!")
    @app_commands.guilds(config['PBtest'], config['Coastal'])
    @app_commands.describe(
        appnumber="Application number to deny"
    ) 
    @commands.has_role("OP Team")
    async def denyapp(self, interaction: discord.Interaction, appnumber):
        # Status set to null
        DMStatus = "FALSE"
        author = interaction.user.id
        guild = interaction.guild
        mrpguild = self.bot.get_guild(config['MRP'])
        row = sheet.find(appnumber, in_column=1).row

        #get values from sheet
        userid = sheet.cell(row, 2).value
        print(userid)
        user = mrpguild.get_member_named(userid)
        print(user)
        sheet.update_cell(row, 18, 'No')

        DMStatus = "FAILED"
        embed = discord.Embed(title="Sorry",
                              description="Your app has been denied",
                              color=0xff0000)
        embed.add_field(
            name="You can try again!",
            value=
            "Just because you have been denied does not mean it is the end. Keep chatting in the Minecraft Realm Portal, and try again at a later time.",
            inline=False)
        embed.set_thumbnail(
            url=
            "https://cdn.discordapp.com/attachments/488792053002534920/1157338182392741999/coastal_logo_final_s9.png"
        )
        try:
            await user.send(embed=embed)
            DMStatus = "DONE"

        finally:
            embed = discord.Embed(title="Application " + appnumber + " Denied",
                                  description="Denied by: " + author.mention,
                                  color=0xff0000)
            embed.add_field(name="**Applicant**", value=user)
            embed.add_field(name="**Console Logs**",
                            value="**DMStatus:** " + DMStatus)
            embed.set_footer(text="The command has finished all of its tasks")
            embed.set_thumbnail(
                url=
                "https://cdn.discordapp.com/attachments/488792053002534920/1157338182392741999/coastal_logo_final_s9.png"
            )
            await interaction.response.send_message(embed=embed)

    @denyapp.error
    async def denyapp_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(
                "Uh oh, looks like I can't execute this command because you don't have permissions!"
            )

        if isinstance(error, commands.TooManyArguments):
            await ctx.send(
                "You sent too many arguments! Did you use quotes for realm names over 2 words?"
            )

        if isinstance(error, commands.CheckFailure):
            await ctx.send("This Command was not designed for this server!")

        elif isinstance(error, commands.BadArgument):
            await ctx.send("You didn't include all of the arguments!")

        else:
            raise error     

async def setup(bot):
    await bot.add_cog(CoastalAppCMD(bot))
