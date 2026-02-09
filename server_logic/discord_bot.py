import os
import discord
import handle_commands
import server_controller
from discord.ext import commands

def start_bot(TOKEN, proc):
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
