import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

#get the token from the .env file
load_dotenv()
TOKEN = os.getenv("TOKEN")

#set the discrod bot to have default permission and the ability to read messages
intents = discord.Intents.default()
intents.message_content = True

#create the bot client
bot = commands.Bot(command_prefix="!", intents=intents)

#say when the bot is online
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


#basic temp command 
@bot.command()
async def ping(ctx):
    await ctx.send("Pong")

#run the bot
bot.run(TOKEN)
