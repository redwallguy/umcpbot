import os
import discord
from discord.ext import commands
import asyncio

#-----------------------------------------------------------
# Variable imports and client initializations
#-----------------------------------------------------------
discToken = os.environ.get('DISCORD_TOKEN')
clubName = os.environ.get('CLUB_NAME')

bot = commands.Bot(command_prefix="?")
#-----------------------------------------------------------
# Event handlers
#-----------------------------------------------------------
@bot.event
async def on_member_join(member):
    for tc in member.guild.text_channels:
        if tc.name == "role-request":
            roleReq = tc
        if tc.name == "important-readme":
            impRM = tc

    if roleReq is not None and impRM is not None:
        member.send("Welcome to " + clubName + ", " + member.mention +
                    "!\nHead over to " + roleReq.mention + " and add your" +
                    " first game. After you do that, " + impRM.mention +
                    " will disappear and you will be able to engage with the" +
                    " communities that you choose to be in!.\nHappy gaming!")
@bot.command()
async def addgame(ctx, *games):
    """
    Add game role(s) to allow access to text/voice channels
    """
    for game in games:
        gameRole = discord.utils.get(ctx.guild.roles, name=game)
        if gameRole is not None and gameRole not in ctx.author.roles:
            await ctx.author.add_roles(gameRole)

@bot.command()
async def removegame(ctx, *games):
    """
    Remove game role(s)
    """
    for game in games:
        gameRole = discord.utils.get(ctx.guild.roles, name=game)
        if gameRole is not None and gameRole in ctx.author.roles:
            await ctx.author.remove_roles(gameRole)
#-----------------------------------------------------------
# Checks and errors
#-----------------------------------------------------------
@bot.check
async def isRR(ctx):
    return ctx.channel.name == "role-request"

@addgame.error
async def addgame_error(ctx, error):
    if isinstance(error, discord.DiscordException.Forbidden):
        ctx.send("Can't do that, sorry.")

@removegame.error
async def removegame_error(ctx, error):
    if isinstance(error, discord.DiscordException.Forbidden):
        ctx.send("Can't do that, sorry.")
#-----------------------------------------------------------
# Run
#-----------------------------------------------------------
bot.run(discToken)
