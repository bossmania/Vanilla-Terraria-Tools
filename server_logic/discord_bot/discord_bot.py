import envs
import logger
import discord
import asyncio
from discord.ext import commands
from discord_bot import discord_bot_notify, discord_server_commands

def can_run_command(ctx):
    #check if the user has the admin role and is in the right channel
    for role in ctx.author.roles:
        if role.id == envs.ADMIN_ROLE_ID and ctx.channel.id == envs.BOT_CHANNEL_ID:
            return True

    #return false if they can't run the command
    return False

class discord_bot_manager:
    def __init__(self, proc):
        self.proc = proc
        self.bot = None
        self.PREFIX = "!"

    def initalize_bot(self):
        # set the discrod bot to have default permission and the ability to read messages and see member info
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True

        #create the bot client and disable the built in help command
        self.bot = commands.Bot(command_prefix=self.PREFIX, intents=intents)
        self.bot.help_command = None

        #set up the discord bot hooks
        discord_server_commands.initalize(self, self.bot, self.proc)
        discord_bot_notify.initalize(self.bot)

    def start_bot(self):
        #prepare the bot
        self.initalize_bot()

        #add the bot to the thread list
        envs.RUNNING_THREADS.append("discord_bot")

        #run the bot
        self.bot.run(envs.TOKEN)
    
    def stop_bot(self):
        #safely stop the bot
        asyncio.run_coroutine_threadsafe(self.bot.close(), self.bot.loop)

        #remove the bot to the thread list
        envs.RUNNING_THREADS.remove("discord_bot")