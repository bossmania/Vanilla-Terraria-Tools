import envs
import logger
import discord
import asyncio
from discord.ext import commands
from commands import server_commands

class discord_bot_manager:
    def __init__(self, proc):
        self.proc = proc
        self.bot = None

    def initalize_bot(self):
        #set the prefix used
        PREFIX = "!"

        # set the discrod bot to have default permission and the ability to read messages and see member info
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True

        #create the bot client and disable the built in help command
        self.bot = commands.Bot(command_prefix=PREFIX, intents=intents)
        self.bot.help_command = None

    def set_bot_commands(self):
        #kick command 
        @self.bot.command()
        async def kick(ctx, user=None):
            #stop if there was no username provided
            if user == None or user == "":
                await ctx.send("Please enter in a username!")
                return

            #kick the player and say that they're kicked
            msg = server_commands.kick(user, self.proc)
            await ctx.send(msg)

        #say when the bot is online
        @self.bot.event
        async def on_ready():
            print(logger.timestamp(f"Logged in as {self.bot.user}"))

    def start_bot(self):
        self.initalize_bot()
        self.set_bot_commands()

        #add the bot to the thread list
        envs.RUNNING_THREADS.append("discord_bot")

        #run the bot
        self.bot.run(envs.TOKEN)
    
    def stop_bot(self):
        #safely stop the bot
        asyncio.run_coroutine_threadsafe(self.bot.close(), self.bot.loop)

        #remove the bot to the thread list
        envs.RUNNING_THREADS.remove("discord_bot")