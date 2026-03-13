import envs
import discord
import asyncio
from commands import server_commands
from discord.ext import commands

bot = None

def start_bot(proc):
    global bot

    #set the prefix used
    PREFIX = "!"

    #set the discrod bot to have default permission and the ability to read messages and see member info
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    #create the bot client and disable the built in help command
    bot = commands.Bot(command_prefix=PREFIX, intents=intents)
    bot.help_command = None

    #kick command 
    @bot.command()
    async def kick(ctx, user=None):
        #stop if there was no username provided
        if user == None or user == "":
            await ctx.send("Please enter in a username!")
            return

        #kick the player and say that they're kicked
        msg = server_commands.kick(user, proc)
        await ctx.send(msg)

    #say when the bot is online
    @bot.event
    async def on_ready():
        print(f"Logged in as {bot.user}")

    envs.RUNNING_THREADS.append("discord_bot")

    #run the bot
    bot.run(envs.TOKEN)

    envs.RUNNING_THREADS.remove("discord_bot")