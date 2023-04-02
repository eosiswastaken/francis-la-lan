## IMPORTS

import discord
import os
import sqlite3
from dotenv import load_dotenv
import uuid














## GLOBAL VARIABLES

load_dotenv() # load all the variables from the env file
bot = discord.Bot()

conn = sqlite3.connect("francis.db")
















## CLASSES AND HELPERS



def get_lans(ctx):
    sql = "SELECT name FROM lan"
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    print(data[0])
    print(data[0][0])
    return data[0]


def get_lan_id(lan_name):
    sql = "SELECT id FROM lan where name = ?"
    cursor = conn.cursor()
    cursor.execute(sql, [(lan_name)])
    data = cursor.fetchall()
    return data[0][0]
      







## BOT CODE

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")
    cursor = conn.cursor()
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS lan(
                id INTEGER,
                name TEXT,
                description TEXT,
                max_seats INTEGER)
        """)
    
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS player(
                id INTEGER,
                lan_id INTEGER,
                seat INTEGER,
                games TEXT,
                handles TEXT,
                team TEXT)
        """)


@bot.slash_command(name = "hello", description = "Say hello to the bot")
async def hello(ctx):
    await ctx.respond("Hey!")



@bot.slash_command(name = "join", description = "Join a LAN")
async def inscription(ctx,lan: discord.Option(str, autocomplete=discord.utils.basic_autocomplete(get_lans))):
        
        sql = "INSERT INTO player VALUES (?, ?, ?, ?, ?, ?)"
        cursor = conn.cursor()
        cursor.execute(sql, [(ctx.author.id), (get_lan_id(lan)), (0), (0), (0), (0)])
        conn.commit()
        
        await ctx.respond(f'You joined {lan} !')



@bot.slash_command(name = "create_lan", description = "Create a new LAN")
async def creer_lan(ctx,name:str,description:str,max_seats:int):
        sql = "INSERT INTO lan VALUES (?, ?, ?, ?)"
        cursor = conn.cursor()
        cursor.execute(sql, [(str(uuid.uuid4())), (name), (description), (max_seats)])
        conn.commit()

        await ctx.respond(f'New LAN created ! Name : {name}, Description : {description}, Setups : {max_seats}')



@bot.slash_command(name = "select_setup", description = "Choose your setup")
async def creer_lan(ctx,user:discord.Member):

        await ctx.respond(f"{user.name}'s profile : \n ** -> ** LAN : LMAO NO \n **->** Setup : LMAO NO ")



@bot.slash_command(name = "profile", description = "Check anyone's profile")
async def creer_lan(ctx,user:discord.Member):

        await ctx.respond(f"{user.name}'s profile : \n ** -> ** LAN : LMAO NO \n **->** Setup : LMAO NO ")










## RUN BOT

bot.run(os.getenv('TOKEN'))