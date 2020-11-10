"""
ChadBot is an exploration of the Discord Bot API which utilizes information taken from the Official Tarkov Wiki to fuffill user requests
    Potential prefixs
        ! , . , > , / , // , $ , % , ^ , & , * , - , + , = , _ , : , \  

    List of Commands:

        !keys <map> -b[est] -u[seless]
        !bestkeys -m[ap] <map_name>
        !key <key_name> 
        !uselesskeys

        !useful <name>

        !best <gun> -r[ecoil] -e[rgonomics]
            !recoil <gun>
            !ergo <gun>
        !med <name>
        !stim <name>

        !map <name>
        !maps

        !trader -n[ame] <level> 
        !prapor !therapist !pk !jaeger !mechanic !ragman <level> 

        !hideout <station>
        !hideoutitems

        !quests <quest_name)
        !kappa

        !keeplist -h[ideout] -q[uests]

        !ammochart
        !ammo -g[un] <gun_name> -c[aliber] <round_caliber>

        !armor <name>

        !sellorder
        !bitcoin !btc 
        
        !cheeky 
        !dicky

        !chadloadout

        !chadtip

        !rattip

        !value <item>

        !wiki <query>

    
"""

import os

import discord
from dotenv import load_dotenv

from discord.ext import commands

bot = commands.Bot(command_prefix='!')

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
TEST_GUILD = os.getenv('DISCORD_TEST_GUILD')
GUILD = os.getenv('DISCORD_GUILD')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

bot.run(TOKEN)

@bot.command(name='cheeki', help = "Help yourself cyka")
async def cheeki(ctx):
    await ctx.send("breeki")

@bot.command(name='ammo', help = "Gives the best 3 ammo types for a given caliber, or a table of the best ammo for each caliber")
async def ammo(ctx):
    await ctx.send("Nofoodaftermidnight ammo spreadsheet --> https://docs.google.com/spreadsheets/d/1jjWcIue0_PCsbLQAiL5VrIulPK8SzM5jjiCMx9zUuvE/edit#gid=64053005")

@bot.command(name='bestkeys', help = "Gives the best keys for a given map, or a table of all the best keys if no map is given")

bot.run(TOKEN)