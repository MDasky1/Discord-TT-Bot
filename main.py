from datetime import datetime
from enum import member

import discord
from discord.ext import commands
import os
import pickle

from discord.ext.commands import Bot

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
contestwinners = {}

bot: Bot = commands.Bot(command_prefix='!', intents=intents)

'''
Attempt to load a contest winners file. File is a Python dictionary in the following format:
    User.ID : [User.Name], Entered, Date and Time of last win (1-1-2000 is set if never won)
'''
try:
    with open('contestwinners.pickle', 'rb') as handle:
        contestwinners = pickle.load(handle)
        print('Found previous contest winners file')
except FileNotFoundError:
    print('Previous contest winners file was not found.')

def UpdateContestWinners():
    with open('contestwinners.pickle', 'wb') as handle:
        pickle.dump(contestwinners, handle)

'''
Initialization routine for the Bot. Prints the bot username when logged in.
Generates records for new users and updates the contest winners file.
'''
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    for member in bot.get_all_members():
        if not contestwinners.get(member.id, 0):
            contestwinners[member.id] = [member.name, False, datetime(2000, 1, 1,0,0,0)]
            print('New record addred for: ' + member.name)
    print(contestwinners)
    UpdateContestWinners()

@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')

# Handle a user's entry into the contest.
@bot.command()
async def enter(ctx):
    for member in bot.get_all_members():
        if not contestwinners.get(ctx.message.author.id, 0):
            contestwinners[ctx.message.author.id] = [member.name, False, datetime(2000, 1, 1,0,0,0)]
    oldrecord = contestwinners[ctx.message.author.id]
    if oldrecord[1]:
        await ctx.send(f'{ctx.message.author}, you are already entered in the contest')

    else:
        oldrecord[1] = True
        contestwinners[ctx.message.author.id] = oldrecord
        await ctx.send(f'{ctx.message.author}, you are now entered in the contest')
    UpdateContestWinners()

bot.run(os.environ['DISCORD_TOKEN'])