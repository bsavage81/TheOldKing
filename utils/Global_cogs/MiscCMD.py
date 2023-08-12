from core.common import load_config
from pathlib import Path
import discord
from discord.ext import commands
import aiohttp
import random
import json
import requests
import ast
import random
from datetime import datetime
from discord.commands import slash_command
rules = [":one: **No Harassment**, threats, hate speech, inappropriate language, posts or user names!", ":two: **No spamming** in chat or direct messages!", ":three: **No religious or political topics**, those don’t usually end well!", ":four: **Keep pinging to a minimum**, it is annoying!", ":five: **No sharing personal information**, it is personal for a reason so keep it to yourself!",
         ":six: **No self-promotion or advertisement outside the appropriate channels!** Want your own realm channel? **Apply for one!**", ":seven: **No realm or server is better than another!** It is **not** a competition.", ":eight: **Have fun** and happy crafting!", ":nine: **Discord Terms of Service apply!** You must be at least **13** years old."]
config, _ = load_config()
'''
import sentry_sdk
sentry_sdk.init(
    "https://75b468c0a2e34f8ea4b724ca2a5e68a1@o500070.ingest.sentry.io/5579376",
    traces_sample_rate=1.0
)
'''

import logging

logger = logging.getLogger(__name__)

async def random_rgb(ctx, seed=None):
    if seed is not None:
        random.seed(seed)

    d = datetime.datetime.utcnow()
    print (d)

    d.hour
    print (d.hour)

    if d.hour == 17:
        embed = discord.Embed(title="time stuff", description=d.hour, color=discord.Colour.from_rgb(random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))())
        await ctx.send(embed=embed)

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return(quote)


def insert_returns(body):
    # insert return stmt if the last expression is a expression statement
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    # for if statements, we insert returns into the body and the orelse
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    # for with blocks, again we insert returns into the body
    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)


class MiscCMD(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logger.info("MiscCMD: Cog Loaded!")

    # DM Command

    @commands.command()
    @commands.has_role("Moderator")
    async def DM(self, ctx, user: discord.User, *, message=None):
        message = message or "This Message is sent via DM"
        author = ctx.message.author
        await user.send(message)
        #await user.send("Sent by: " + author.name)

    @DM.error
    async def DM_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.send("Uh oh, looks like you don't have the Moderator role!")

    # Uptime Command
    @commands.command()
    async def uptime(self, ctx):
        author = ctx.message.author
        await ctx.send("Really long time, lost track. ")

    # Purge Command
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=2):
        author = ctx.message.author
        await ctx.channel.purge(limit=amount)

    # Nick Commamd
    @commands.command()
    @commands.has_role("Moderator")
    async def nick(self, ctx, user: discord.Member, channel: discord.TextChannel):
        author = ctx.message.author
        name = user.display_name
        channel = channel.name.split('-')
        if len(channel) == 2:  # real-emoji
            realm, emoji = channel
        else:  # realm-name-emoji
            realm, emoji = channel[0], channel[-1]
        await user.edit(nick=str(name) + " " + str(emoji))
        await ctx.send("Changed nickname!")

    @nick.error
    async def nick_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.send("Uh oh, looks like you don't have the Moderator role!")

    # Rule Command [INT]
    #@cog_ext.cog_slash(name="rule", description = "Sends out MRP Server Rules", guild_ids=[config['ServerID'],config['ServerID2']], options=[manage_commands.create_option(name = "number" , description = "Rule Number", option_type = 4, required = True)])
    #async def rule(self, ctx, number = None):
    #    await ctx.send(content = rules[int(number)-1])

    # Add's a gamertag to the database.

    @commands.command(description="Rock Paper Scissors")
    async def rps(self, msg: str):
        """Rock paper scissors. Example : /rps Rock if you want to use the rock."""
        # Les options possibles
        t = ["rock", "paper", "scissors"]
        # random choix pour le bot
        computer = t[random.randint(0, 2)]
        player = msg.lower()
        print(msg)
        if player == computer:
            await self.bot.say("Tie!")
        elif player == "rock":
            if computer == "paper":
                await self.bot.say("You lose! {0} covers {1}".format(computer, player))
            else:
                await self.bot.say("You win! {0} smashes {1}".format(player, computer))
        elif player == "paper":
            if computer == "scissors":
                await self.bot.say("You lose! {0} cut {1}".format(computer, player))
            else:
                await self.bot.say("You win! {0} covers {1}".format(player, computer))
        elif player == "scissors":
            if computer == "rock":
                await self.bot.say("You lose! {0} smashes {1}".format(computer, player))
            else:
                await self.bot.say("You win! {0} cut {1}".format(player, computer))
        else:
            await self.bot.say("That's not a valid play. Check your spelling!")

    @commands.command()
    async def inspire(self, ctx):
        quote = get_quote()
        author = ctx.message.author
        embed = discord.Embed(title="Inspirational Quotes", description="Here is your quote {0}".format(
            author.mention), color=0xffe74d)
        embed.add_field(name="Quote", value=quote)
        await ctx.send(embed=embed)
    
    @commands.command() 
    async def reply(self, ctx):
        id = ctx.message.id
        await ctx.reply(content = "content") 
        

def setup(bot):
    bot.add_cog(MiscCMD(bot))



