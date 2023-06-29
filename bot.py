## IMPORTS

import discord
import os
import sqlite3
from dotenv import load_dotenv
import uuid
import time










OWNER = 290482004435271680




## GLOBAL VARIABLES

load_dotenv() # load all the variables from the env file
bot = discord.Bot()

conn = sqlite3.connect("lanman.db")

HTML = """<link href="txtstyle.css" rel="stylesheet" type="text/css" /> \n"""














## CLASSES AND HELPERS

def is_owner(id):
      return id == OWNER

def get_lans(ctx):
    sql = "SELECT name FROM lan"
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    print(data)
    print(data[0])
    x = []
    for i in range(0,len(data)):
          x.append(data[i][0])
    return x


def get_teams(ctx):
    sql = "SELECT name FROM team"
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    print(data)
    print(data[0])
    x = []
    for i in range(0,len(data)):
          x.append(data[i][0])
    
    return x


def get_lan_id(lan_name):
    sql = "SELECT id FROM lan WHERE name = ?"
    cursor = conn.cursor()
    cursor.execute(sql, [(lan_name)])
    data = cursor.fetchall()
    return data[0][0]


def get_team_id(team_name):
    sql = "SELECT id FROM team WHERE name = ?"
    cursor = conn.cursor()
    cursor.execute(sql, [(team_name)])
    data = cursor.fetchall()
    return data[0][0]

def get_team_name(team_id):
    sql = "SELECT name FROM team WHERE id = ?"
    cursor = conn.cursor()
    cursor.execute(sql, [(team_id)])
    data = cursor.fetchall()
    return data[0][0]


def get_lan_name(lan_id):
    sql = "SELECT name FROM lan WHERE id = ?"
    cursor = conn.cursor()
    cursor.execute(sql, [(lan_id)])
    data = cursor.fetchall()
    return data[0][0]
      

def get_seats(ctx: discord.AutocompleteContext):

    lan_name = ctx.options['lan_name']
    lan_id = get_lan_id(lan_name)
    print(f"fgreegergregergegege {lan_name}")

    sql = "SELECT max_seats FROM lan WHERE id = ?"
    cursor = conn.cursor()
    cursor.execute(sql, [(lan_id)])
    data = cursor.fetchall()
    print(f"fewhufewifhuw{data}")
    max_seats = data[0][0]
    x = []
    for i in range(1,max_seats+1):
          x.append(str(i))

    sql = "SELECT seat FROM player WHERE lan_id = ?"
    print(lan_id)
    cursor = conn.cursor()
    cursor.execute(sql, [(lan_id)])
    data = cursor.fetchall()
    booked_seats = data
    print(f"booked : {booked_seats}")
    for booked_seat in booked_seats:
          if booked_seat[0] != 0:
            x.pop(x.index(str(booked_seat[0])))
    return x


def get_player_lan(id):
    
    sql = "SELECT lan_id FROM player WHERE id = ?"
    cursor = conn.cursor()
    cursor.execute(sql, [(id)])
    data = cursor.fetchall()
    try:
        return get_lan_name(data[0][0])
    except IndexError:
        return "No LAN"

def get_player_seat(id):
    sql = "SELECT seat FROM player WHERE id = ?"
    cursor = conn.cursor()
    cursor.execute(sql, [(id)])
    data = cursor.fetchall()
    try:
        return data[0][0]
    except IndexError:
        return "No seat"

def get_player_team(id):
    sql = "SELECT team_id FROM player WHERE id = ?"
    cursor = conn.cursor()
    cursor.execute(sql, [(id)])
    data = cursor.fetchall()
    try:
        return get_team_name(data[0][0])
    except IndexError:
        return "No team"

def get_player_games(id):
    sql = "SELECT games FROM player WHERE id = ?"
    cursor = conn.cursor()
    cursor.execute(sql, [(id)])
    data = cursor.fetchall()
    try:
        return data[0][0]
    except IndexError:
        return "No games"

def get_player_handles(id):
    sql = "SELECT handles FROM player WHERE id = ?"
    cursor = conn.cursor()
    cursor.execute(sql, [(id)])
    data = cursor.fetchall()
    try:
        return data[0][0]
    except IndexError:
        return "No handles"

    
def get_player_brings(id):
    sql = "SELECT brings FROM player WHERE id = ?"
    cursor = conn.cursor()
    cursor.execute(sql, [(id)])
    data = cursor.fetchall()
    try:
        return data[0][0]
    except IndexError:
        return "No things youll bring"


def get_player_dispos(id):
    sql = "SELECT dispos FROM player WHERE id = ?"
    cursor = conn.cursor()
    cursor.execute(sql, [(id)])
    data = cursor.fetchall()
    try:
        return data[0][0]
    except IndexError:
        return "No dispos"
    





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
                team TEXT,
                dispos TEXT,
                brings TEXT,
                team_id INTEGER
                )
        """)
    
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS team(
                id INTEGER,
                name TEXT,
                points INTEGER)
        """)
    
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS shout(
                message TEXT,
                timestamp INTEGER)
        """)
    
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS screen(
                path TEXT,
                timestamp INTEGER)
        """)


@bot.slash_command(name = "hello", description = "Say hello to the bot")
async def hello(ctx):
    await ctx.respond("Hey!")



@bot.slash_command(name = "join", description = "Join a LAN")
async def inscription(ctx,lan: discord.Option(str, autocomplete=discord.utils.basic_autocomplete(get_lans))):
        
        sql = "INSERT INTO player VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
        cursor = conn.cursor()
        cursor.execute(sql, [(ctx.author.id), (get_lan_id(lan)), (0), ("You did not fill in the games you'd like to play !"), ("You did not fill in your game / launcher handles"), ("No team"), ("You did not fill in your dispos"), ("You did not fill in the things you'll bring to the LAN !"), (0)])
        conn.commit()
        
        await ctx.respond(f'You joined {lan} !')



@bot.slash_command(name = "create", description = "Create a new LAN")
async def creer_lan(ctx,name:str,description:str,max_seats:int):
        if not is_owner(ctx.author.id): 
              await ctx.respond(f'You are not a moderator')
              return
        sql = "INSERT INTO lan VALUES (?, ?, ?, ?)"
        cursor = conn.cursor()
        cursor.execute(sql, [(str(uuid.uuid4())), (name), (description), (max_seats)])
        conn.commit()

        await ctx.respond(f'New LAN created ! Name : {name}, Description : {description}, Seats : {max_seats}')



@bot.slash_command(name = "seat", description = "Choose your seat")
async def seat(ctx,lan_name: discord.Option(str, autocomplete=discord.utils.basic_autocomplete(get_lans)),seat: discord.Option(str, autocomplete=discord.utils.basic_autocomplete(get_seats))):
        sql = "UPDATE player SET seat = ? WHERE id = ?"
        cursor = conn.cursor()
        cursor.execute(sql, [(seat), (ctx.author.id)])
        conn.commit()
        await ctx.respond(f"Seat updated ! Seat nb. : {seat}")



@bot.slash_command(name = "profile", description = "Check anyone's profile")
async def profile(ctx,user:discord.Member):

        await ctx.respond(f"🖥️ `{user.name}'s profile :` \n 👉 LAN : {get_player_lan(user.id)} \n 👉 Seat : {get_player_seat(user.id)}\n 👉 Team : {get_player_team(user.id)} \n 👉 Games : {get_player_games(user.id)} \n 👉 Handles : {get_player_handles(user.id)} \n 👉 Brings : {get_player_brings(user.id)} \n 👉 Dispos : {get_player_dispos(user.id)} ")


@bot.slash_command(name = "games", description = "Change the games you'd like to play (free text)")
async def games(ctx,games:str):

        sql = "UPDATE player SET games = ? WHERE id = ?"
        cursor = conn.cursor()
        cursor.execute(sql, [(games), (ctx.author.id)])
        conn.commit()
        await ctx.respond(f"Games updated !")

@bot.slash_command(name = "bring", description = "Change the things you'll bring to the LAN (free text)")
async def brings(ctx,brings:str):

        sql = "UPDATE player SET brings = ? WHERE id = ?"
        cursor = conn.cursor()
        cursor.execute(sql, [(brings), (ctx.author.id)])
        conn.commit()
        await ctx.respond(f"stuff etc updated !")

@bot.slash_command(name = "dispo", description = "Change your disponibilities fo the LAN (free text)")
async def dispos(ctx,dispos:str):

        sql = "UPDATE player SET dispos = ? WHERE id = ?"
        cursor = conn.cursor()
        cursor.execute(sql, [(dispos), (ctx.author.id)])
        conn.commit()
        await ctx.respond(f"Dispos updated !")


@bot.slash_command(name = "handles", description = "Change your launcher/game handles")
async def handles(ctx,steam:str=0,epicgames:str=0,battlenet:str=0,riot:str=0):
        player_handles = (f"**Steam :** {steam} // **Epic games :** {epicgames} // **Battle.net :** {battlenet} // **RIOT :** {riot}")
        sql = "UPDATE player SET handles = ? WHERE id = ?"
        cursor = conn.cursor()
        cursor.execute(sql, [(player_handles), (ctx.author.id)])
        conn.commit()
        await ctx.respond(f"Handles updated !")


@bot.slash_command(name = "check_dispos", description = "Check out all the dispos")
async def check_dispos(ctx):

        sql = "SELECT id,dispos FROM player"
        cursor = conn.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        msg = "🖥️ `Dispos :` \n"
        for i in range(0,len(data)):
             msg += f"👉 {await bot.fetch_user(data[i][0])} : {data[i][1]}\n"
        await ctx.respond(msg)

@bot.slash_command(name = "check_bring", description = "Check out all the things people will bring")
async def check_bring(ctx):

        sql = "SELECT id,brings FROM player"
        cursor = conn.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        msg = "🖥️ `What people will bring :` \n"
        for i in range(0,len(data)):
             msg += f"👉 {await bot.fetch_user(data[i][0])} : {data[i][1]}\n"
        await ctx.respond(msg)

@bot.slash_command(name = "check_games", description = "Check out all the games people want to play")
async def check_games(ctx):

        sql = "SELECT id,games FROM player"
        cursor = conn.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        msg = "🖥️ `Games :` \n"
        for i in range(0,len(data)):
             msg += f"👉 {await bot.fetch_user(data[i][0])} : {data[i][1]}\n"
        await ctx.respond(msg)

@bot.slash_command(name = "shout", description = "Shout something on the live whiteboard !")
async def profile(ctx,message:str):
        sql = "INSERT INTO shout VALUES (?, ?)"
        cursor = conn.cursor()
        cursor.execute(sql, [(message), (time.time())])
        conn.commit()
        with open('./whiteboard/shout.html', 'w') as f:
            f.write(HTML + message)
        await ctx.respond(f"Shouted !")


@bot.slash_command(name = "screen", description = "Post an image on the live whiteboard !")
async def profile(ctx,screen:discord.Attachment):
        sql = "INSERT INTO screen VALUES (?, ?)"
        cursor = conn.cursor()
        cursor.execute(sql, [(screen.url), (time.time())])
        conn.commit()
        await screen.save("./whiteboard/screen.png")
        await ctx.respond(f"Screened !")


@bot.slash_command(name = "create_team", description = "Create your own team omg")
async def create_team(ctx,name:str):

        sql = "INSERT INTO team VALUES (?, ?, ?)"
        cursor = conn.cursor()
        cursor.execute(sql, [(str(uuid.uuid4())), (name), (0)])
        conn.commit()
        await ctx.respond(f"You created team {name} !")


@bot.slash_command(name = "join_team", description = "Join your friends")
async def join_team(ctx,team: discord.Option(str, autocomplete=discord.utils.basic_autocomplete(get_teams))):

        sql = "UPDATE player SET team_id = ? WHERE id = ?"
        cursor = conn.cursor()
        cursor.execute(sql, [(get_team_id(team)), (ctx.author.id)])
        conn.commit()
        await ctx.respond(f"You joined team {team} !")

@bot.slash_command(name = "team_win", description = "Add one point to a team !")
async def team_win(ctx,team: discord.Option(str, autocomplete=discord.utils.basic_autocomplete(get_teams))):
        if not is_owner(ctx.author.id): 
              await ctx.respond(f'You are not a moderator')
              return

        sql = "UPDATE team SET points = points + 1 WHERE id = ?"
        cursor = conn.cursor()
        cursor.execute(sql, [(get_team_id(team))])
        conn.commit()
        await ctx.respond(f"Team {team} won one point !")

@bot.slash_command(name = "team_lose", description = "Remove one point to a team !")
async def team_lose(ctx,team: discord.Option(str, autocomplete=discord.utils.basic_autocomplete(get_teams))):
        if not is_owner(ctx.author.id): 
              await ctx.respond(f'You are not a moderator')
              return

        sql = "UPDATE team SET points = points - 1 WHERE id = ?"
        cursor = conn.cursor()
        cursor.execute(sql, [(get_team_id(team))])
        conn.commit()
        await ctx.respond(f"Team {team} lost one point !")

@bot.slash_command(name = "team_reset", description = "Reset the points of a team !")
async def team_reset(ctx,team: discord.Option(str, autocomplete=discord.utils.basic_autocomplete(get_teams))):
        if not is_owner(ctx.author.id): 
              await ctx.respond(f'You are not a moderator')
              return

        sql = "UPDATE team SET points = 0 WHERE id = ?"
        cursor = conn.cursor()
        cursor.execute(sql, [(get_team_id(team))])
        conn.commit()
        await ctx.respond(f"Team {team} got reset !")


@bot.slash_command(name = "teams", description = "Check out all the teams !")
async def teams(ctx):

        sql = "SELECT name, points FROM team ORDER BY points DESC"
        cursor = conn.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        msg = "🖥️ `Team leaderboard:` \n"
        for i in range(0,len(data)):
             msg += f"👉 {data[i][0]} : {data[i][1]} points\n"
             
        await ctx.respond(msg)





## RUN BOT

bot.run(os.getenv('TOKEN'))
