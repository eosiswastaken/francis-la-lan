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



@bot.slash_command(name = "inscription", description = "Inscirs toi a une LAN")
async def inscription(ctx,lan: discord.Option(str, autocomplete=discord.utils.basic_autocomplete(get_lans))):
        await ctx.respond(f'Tu fais partie de la lan {lan} !')



@bot.slash_command(name = "creer_lan", description = "Crée une nouvelle LAN")
async def creer_lan(ctx,name:str,description:str,max_seats:int):
        sql = "INSERT INTO lan VALUES (?, ?, ?, ?)"
        cursor = conn.cursor()
        cursor.execute(sql, [(str(uuid.uuid4())), (name), (description), (max_seats)])
        conn.commit()

        await ctx.respond(f'Nouvelle lan crée ! Nom : {name}, Description : {description}, Setups : {max_seats}')














## RUN BOT

bot.run(os.getenv('TOKEN'))