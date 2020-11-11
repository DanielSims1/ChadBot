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


#This could be a mapping of gun names to screenshots of meta builds. screenshots could potentially be stored on this device and sent with the message.
known_gun_names = {'hk416a5':"hk416a5.png", 'hk':"hk416a5.png", 'hk416': "hk416a1.png",
    'm4a1':"soonTM.png", 'm4':"soonTM.png",
    'adar': "soonTM.png", 'adar 215': "soonTM.png", 'adar 2-15': "soonTM.png",
    'sa-58':"soonTM.png", 'sa58':"soonTM.png",
    'ak-74m':"soonTM.png", 'ak-74':"soonTM.png", 'ak74m': "soonTM.png", 'ak74': "soonTM.png", 'ak': "soonTM.png",
    'ash-12':"soonTM.png", 'ash':"soonTM.png",
    'asval':"soonTM.png", 'as val':"soonTM.png", 'as-val': "soonTM.png",'val': "soonTM.png",
    'kel-tec rfb':"soonTM.png", 'rfb':"soonTM.png",
    '.308 mdr':"soonTM.png", 'mdr .308':"soonTM.png", 'mdr 308': "soonTM.png", '308 mdr' : "soonTM.png",
    '5.56 mdr':"soonTM.png", '556 mdr':"soonTM.png", 'mdr 5.56': "soonTM.png", 'mdr 556': "soonTM.png",
    'sr-25':"soonTM.png", 'sr25':"soonTM.png",
    'akm':"soonTM.png",
    'rpk':"soonTM.png", 'rpk-16':"soonTM.png", 'rpk16': "soonTM.png",
    'tx-15 dml': "soonTM.png", 'tx-15': "soonTM.png", 'tx15 dml' : "soonTM.png", 'tx15': "soonTM.png",
    'sks': "soonTM.png", 'op-sks' : "soonTM.png",
    'mp5':"soonTM.png", 'mp5k':"soonTM.png", 'mp5k-n': "soonTM.png", 'mp5kn': "soonTM.png",
    'mp7':"hk416a5.png", 'mp7a2':"hk416a5.png",
    'mp9': "soonTM.png",
    'mpx': "soonTM.png",
    'p90': "soonTM.png",
    'm1a': "soonTM.png",
    'rsass': "soonTM.png",
    'vss': "soonTM.png",
    'svd': "soonTM.png",'svds': "soonTM.png",









} 
# 'm4a1':"soonTM", 'SA-58', 'ak-74m', 'ash-12', 'as val', 'kel-tec rfb', '.308 mdr', '5.56 mdr', 'sr-25', 'akm', 'rpk-16'}
# force queries to lowercase to ensure they get correct build

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name= 'cheeki', help = "Help yourself cyka")
async def cheeki(ctx):
    await ctx.send("breeki")

@bot.command(name='best', help = "Gives you the best overall meta build for a given gun")
async def best_gun(ctx, gun_name):
    # force to lowercase to make queries easier
    formatted_gun_name = gun_name.lower()
    # assuming no *recoil* or *ergonomics* modifier
    if formatted_gun_name in known_gun_names.keys():
        # get file from correct location
        gun_image = discord.File(f"images/best/{known_gun_names.get(formatted_gun_name)}")
        await ctx.send("Here is the best build for the {}, enjoy comrade!".format(formatted_gun_name))
        await ctx.send(file=gun_image)

    else:
        await ctx.send(f"The gun *{gun_name}* currently lacks meta builds.... make sure you typed the name correctly")


@bot.command(name='ammo', help = "Gives the best 3 ammo types for a given caliber, or a table of the best ammo for each caliber")
async def ammo(ctx):
    await ctx.send("Nofoodaftermidnight ammo spreadsheet --> https://docs.google.com/spreadsheets/d/1jjWcIue0_PCsbLQAiL5VrIulPK8SzM5jjiCMx9zUuvE/edit#gid=64053005")

@bot.command(name='bestkeys', help = "Gives the best keys for a given map, or a table of all the best keys if no map is given")
async def bestkeys(ctx):
    await ctx.send("out of date best keys --> https://preview.redd.it/let6rgrtq8951.png?width=960&crop=smart&auto=webp&s=bb6ecc50549e3dc4c7e9d6e75529820613d003b1")

bot.run(TOKEN)