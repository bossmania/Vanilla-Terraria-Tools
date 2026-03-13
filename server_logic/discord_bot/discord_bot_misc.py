import logger
from discord.ext import commands
from discord_bot import discord_server_commands

def initalize(bot):
    #say when the bot is online
    @bot.event
    async def on_ready():
        print(logger.timestamp(f"Logged in as {bot.user}"))