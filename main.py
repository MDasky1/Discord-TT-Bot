from datetime import datetime
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
    User.ID : [User.Name], Date and Time of last win (1-1-2000 is set if never won)
'''
try:
    with open('contestwinners.pickle', 'rb') as handle:
        contestwinners = pickle.load(handle)
        print('Found previous contest winners file')
except FileNotFoundError:
    print('Previous contest winners file was not found.')

'''
Initialization routine for the Bot. Prints the bot username when logged in.
Generates records for new users and updates the contest winners file.
'''
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    for member in bot.get_all_members():
        if not contestwinners.get(member.id, 0):
            contestwinners[member.id] = [member.name, datetime(2000, 1, 1,0,0,0)]
    print(contestwinners)
    with open('contestwinners.pickle', 'wb') as handle:
        pickle.dump(contestwinners, handle)

@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')

bot.run(os.environ['DISCORD_TOKEN'])