import os

import discord
import asyncio

# for wiki querying
import requests
from bs4 import BeautifulSoup

# for creds
from dotenv import load_dotenv


import re

from discord.ext import commands

import logging

logging.basicConfig(level=logging.INFO)

command_prefix = '!'

bot = commands.Bot(command_prefix= command_prefix)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
TEST_GUILD = os.getenv('DISCORD_TEST_GUILD')
GUILD = os.getenv('DISCORD_GUILD')


# This could be a mapping of gun names to screenshots of meta builds. screenshots could potentially be stored on this device and sent with the message.
known_guns = {
    'hk416a5':"hk416a5.png", 'hk':"hk416a5.png", 'hk416': "hk416a1.png",
    'm4a1':"m4a1.png", 'm4':"m4a1.png",
    'adar': "adar.png", 'adar 215': "adar.png", 'adar 2-15': "adar.png",
    'sa-58':"sa-58.png", 'sa58':"sa-58.png",
    'ak-74m':"ak-74m.png", 'ak-74':"ak-74m.png", 'ak74m': "ak-74m.png", 'ak74': "ak-74m.png", 'ak': "ak-74m.png",
    'asval':"as-val.png", 'as val':"as-val.png", 'as-val': "as-val.png",'val': "as-val.png",
    'kel-tec rfb':"rfb.png", 'rfb':"rfb.png",
    '.308 mdr':"308-mdr.png", 'mdr .308':"308-mdr.png", 'mdr 308': "308-mdr.png", '308 mdr' : "308-mdr.png",
    '5.56 mdr':"mdr-556.png", '556 mdr':"mdr-556.png", 'mdr 5.56': "mdr-556.png", 'mdr 556': "mdr-556.png",
    'sr-25':"sr-25.png", 'sr25':"sr-25.png",
    'akm':"akm.png",
    'rpk':"rpk.png", 'rpk-16':"rpk.png", 'rpk16': "rpk.png",
    'tx-15 dml': "tx-15.png", 'tx-15': "tx-15.png", 'tx15 dml' : "tx-15.png", 'tx15': "tx-15.png",
    'sks': "op-sks.png", 
    'op-sks' : "op-sks.png",
    'mp5':"mp5.png", 
    'mp7':"mp7.png", 'mp7a2':"mp7.png",
    'mpx': "mpx.png",
    'p90': "p90.png",
    'm1a': "m1a.png",
    'rsass': "rsass.png",
    'vss': "vss.png",
    'svd': "svds.png",'svds': "svds.png"
} 
known_gun_names = known_guns.keys()

recoil_param = ["recoil","rec","r"]
ergonomics_param = ["ergonomics","ergo", "e"]

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


# [Simple reflex commands]
@bot.command(name= 'cheeki')
async def cheeki(ctx):
    await ctx.send("breeki")

@bot.command(name= 'dicky')
async def dicky(ctx):
    await ctx.send("needles")


@bot.command(name = "ammo", help = "Shows an ammo chart for the requested gun or caliber")
async def ammo(ctx, gun):
    # Get the ammo page then search for rounds associated with a given gun
    wiki_ammo_page = requests.get("https://escapefromtarkov.gamepedia.com/Ammunition", auth=('user','pass'))
    ammo_soup = BeautifulSoup(wiki_ammo_page.text, 'html.parser')
    ammo_rows = ammo_soup.find_all("tr")

    print(ammo_rows.prettify())




#@bot.command(name = 'key', help = "Gives you the map and rating out of 5 stars for a key")
async def key(ctx):
    # So we want to do another search on the wiki for a key then rate the key  0/5 [ ] --> 5/5 [⭐⭐⭐⭐⭐]
    # also notify user if this is a quest key
    weights = ["ledx", "graphics card", "safe"]
    scoring_items = [50, 30, 20]
    quest = "❗"


@bot.command(name= "price", help = "Queries for lowest current price of item on the flea market")
async def price(ctx, *,search_arg):
    # Use wiki to get well-formatted text then convert to the tarkov-market.com format [" " -> "_"]
    search_string = str(search_arg)
    tarkov_wiki_base_url = "https://escapefromtarkov.gamepedia.com/Special:Search?search="
    tarkov_wiki = requests.get(f"{tarkov_wiki_base_url}{search_string}", auth=('user','pass'))

    tarkov_market_url = "https://tarkov-market.com/item/"

    soup = BeautifulSoup(tarkov_wiki.text, 'html.parser')

    is_correct_page = soup.find("meta", property = "og:description")
    # If we searched the exact name of a page, then we are brought directly to it
    if is_correct_page:
        title_string = soup.find("meta", property = "og:title")["content"]

    else: # return top result
        title_string = soup.find("a", class_ = "unified-search__result__link")["data-title"]
        
    if(title_string):
        url_title = title_string.replace(" ", "_")
    
        is_yelling = re.findall("[A-Z]{2}", url_title)
        if is_yelling:
            url_title = url_title.lower();

        tarkov_market = requests.get(f"{tarkov_market_url}{url_title}", auth=('user','pass'))
        market_soup = BeautifulSoup(tarkov_market.text, 'html.parser')

        if(tarkov_market):
            price = market_soup.find("div", class_="price last").string

            embed = discord.Embed(title=price,description=f"{title_string}")
            await ctx.send(content=f"Price check for {title_string}",embed=embed)

    else:
        await ctx.send(f"Sorry comrade, no prices found for {search_string}")

@price.error
async def best_gun_error(ctx, error):
    logger = logging.getLogger('tcpserver')
    logger.warn(error)
    await ctx.send('Uhhh comrade have you been breaking into my vodka stash again??\n :rat:\n\n\t\t     :white_small_square:\n\t\t\t\t:white_small_square:\n\t\t\t\t    :champagne: ')


# Join the voice channel of user and greet them with a hello my friend
@bot.command(name = "hello", help = "Hello my friend!")
async def hello_my_friend(ctx):
    # Get user's voice channel
    voice_channel = ctx.author.voice.channel
    if voice_channel != None:
        vc = await voice_channel.connect()
        vc.play(discord.FFmpegPCMAudio("audio/hello_my_friends.wav"), after = disconnect_after_sound(vc))
    else:
        await ctx.send(str(ctx.message.author),"is not in a voice channel")

def disconnect_after_sound(vc):
    def f(error):
        asyncio.run_coroutine_threadsafe(vc.disconnect(), vc.loop)
    return f

#TODO Update this with latest gun builds
@bot.command(name='best', help = "Gives you the best overall meta build for a given gun")
async def best_gun(ctx, *args):
    gun_name = ""
    optimizer = ""
    well_formatted = False

    if len(args) > 2:
        await ctx.send(f"The *{command_prefix}best* command only permits up to 2 arguments: gun_name [required], and recoil/ergonomics (optional) \nEx: !best m4a1 recoil")
    else:
    # extract meaning from commands  
        for arg in args:
            clean_arg = arg.lower()
            if clean_arg in known_gun_names:
                if gun_name == "":
                    gun_name = clean_arg
                    well_formatted = True
                else:
                    await ctx.send("What are you trying to do here? Ask for one gun at a time!")
                    well_formatted = False
            if clean_arg in recoil_param or clean_arg in ergonomics_param:
                if optimizer == "":
                    optimizer = clean_arg
                else:
                    await ctx.send("One gun.... one optimizer... is that so hard??")

        if well_formatted:
            if optimizer in ergonomics_param:
                optimizer = "ergonomics"
                gun_image = discord.File(f"images/ergonomics/{known_guns.get(gun_name)}")
            elif optimizer in recoil_param:
                optimizer = "recoil"
                gun_image = discord.File(f"images/recoil/{known_guns.get(gun_name)}")
            else:
                gun_image = discord.File(f"images/best/{known_guns.get(gun_name)}")
            await ctx.send(f"Here is the best {optimizer} build for the {gun_name}, enjoy comrade!")
            await ctx.send(file=gun_image)
@best_gun.error
async def best_gun_error(ctx, error):
    logger = logging.getLogger('tcpserver')
    logger.warn(error)
    await ctx.send('Uhhh comrade have you been breaking into my vodka stash again??\n :rat:\n\n\t\t     :white_small_square:\n\t\t\t\t:white_small_square:\n\t\t\t\t    :champagne: ')

@bot.command(name='ammochart', help = "Shows a table of the best ammo for each caliber")
async def ammochart(ctx):
    await ctx.send("Nofoodaftermidnight ammo spreadsheet --> https://docs.google.com/spreadsheets/d/1jjWcIue0_PCsbLQAiL5VrIulPK8SzM5jjiCMx9zUuvE/edit#gid=64053005")

@bot.command(name='bestkeys', help = "Gives the best keys for a given map, or a table of all the best keys if no map is given")
async def bestkeys(ctx):
    await ctx.send("out of date best keys --> https://preview.redd.it/let6rgrtq8951.png?width=960&crop=smart&auto=webp&s=bb6ecc50549e3dc4c7e9d6e75529820613d003b1")

@bot.command(name='wiki', help = "Queries the Tarkov Wiki")
async def wiki(ctx, *,search_arg):
    search_string = str(search_arg)
    tarkov_wiki_base_url = "https://escapefromtarkov.gamepedia.com/Special:Search?search="
    tarkov_wiki = requests.get(f"{tarkov_wiki_base_url}{search_string}", auth=('user','pass'))

    soup = BeautifulSoup(tarkov_wiki.text, 'html.parser')

    is_correct_page = soup.find("meta", property = "og:description")
    # If we searched the exact name of a page, then we are brought directly to it
    if is_correct_page:
        embed = discord.Embed(title=search_string,description=f"[{search_string} Wiki Page]({tarkov_wiki_base_url}{search_string})")
        await ctx.send(content=f"Here is the wiki page for `{search_string}` comrade:",embed=embed)
    
    # Otherwise show top x search results
    else:
        top_urls = list()
        for top_result in soup.find_all("a", class_ = "unified-search__result__link"):
            top_urls.append((top_result.get('data-title'),top_result.get('href')))
        
        num_results = 5
        if num_results <= len(top_urls):
            embed = discord.Embed(title=search_string,description=f"Top {num_results} search results for `{search_string}`: ")
            embedString = ""
            for i in range(num_results):
                embedString += f"[{top_urls[i][0]}]({top_urls[i][1]})\n"
            embed.add_field(name=chr(173), value=embedString,inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"Sorry comrade, no results found for {search_string}")

bot.run(TOKEN)