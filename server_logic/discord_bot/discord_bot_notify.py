import envs
import logger
import discord
from discord.ext import commands
from discord_bot import discord_server_commands

def initalize(bot):
    #say when the bot is online
    @bot.event
    async def on_ready():
        print(logger.timestamp(f"Logged in as {bot.user}"))

async def notify(msg):
    #get the notify channel and check if it's real
    channel = envs.BOT.bot.get_channel(envs.NOTIFY_CHANNEL_ID)
    if channel:
        #send the message
        await channel.send(msg)

async def chat_log(msg):
    #get the chat channel and check if it's real
    channel = envs.BOT.bot.get_channel(envs.CHAT_CHANNEL_ID)
    if channel:
        #get the username and message
        username = envs.user_regex.search(msg).group()
        message = msg.split(">")[1]

        #send the message as a embed
        embed = discord.Embed(title=username, description=message, color=0xeb7353)
        await channel.send(embed=embed)