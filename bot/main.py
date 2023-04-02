## IMPORTS

import discord
import os 
from dotenv import load_dotenv



## GLOBAL VARIABLES

load_dotenv() # load all the variables from the env file
bot = discord.Bot()



## BOT CODE

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

@bot.slash_command(name = "hello", description = "Say hello to the bot")
async def hello(ctx):
    await ctx.respond("Hey!")



## RUN BOT

bot.run(os.getenv('TOKEN'))