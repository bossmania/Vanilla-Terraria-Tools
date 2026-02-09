import os
import discord
import handle_commands
import server_controller
from discord.ext import commands

#set the prefix used
PREFIX = "!"

def start_bot(TOKEN, proc):
    #set the discrod bot to have default permission and the ability to read messages
    intents = discord.Intents.default()
    intents.message_content = True

    #create the bot client and disable the built in help command
    bot = commands.Bot(command_prefix=PREFIX, intents=intents)
    bot.help_command = None

    #say when the bot is online
    @bot.event
    async def on_ready():
        print(f"Logged in as {bot.user}")

    #kick command 
    @bot.command()
    async def kick(ctx, user=None):
        #stop if there was no username provided
        if user == None or user == "":
            await ctx.send("Please enter in a username!")
            return

        #kick the player and say that they're kicked
        msg = handle_commands.kick(user, proc)
        await ctx.send(msg)

    #ban command 
    @bot.command()
    async def ban(ctx, user=None):
        #stop if there was no username provided
        if user == None or user == "":
            await ctx.send("Please enter in a username!")
            return

        #ban the player and say that they're ban
        msg = handle_commands.ban(user, proc)
        await ctx.send(msg)

    #backup command 
    @bot.command()
    async def backup(ctx):
        #backup the world
        msg = handle_commands.backup(proc)
        await ctx.send(msg)

    #save command 
    @bot.command()
    async def save(ctx):
        #save the world
        msg = handle_commands.save(proc)
        await ctx.send(msg)

    #exit command 
    @bot.command()
    async def exit(ctx):
        #exit the world
        msg = handle_commands.exit(proc)
        await ctx.send(msg)
    
    #settle command 
    @bot.command()
    async def settle(ctx):
        #settle the world's water
        msg = handle_commands.settle(proc)
        await ctx.send(msg)

    #help command
    @bot.command()
    async def help(ctx):
        #create the embed with title, desc, and color
        embed=discord.Embed(title="Help Commands", description="shows all of the help commands", color=0x2ec27e)

        #set all of the commands
        embed.add_field(name=f"{PREFIX}kick <USERNAME>", value="Kicks a player from the server.")
        embed.add_field(name=f"{PREFIX}ban <USERNAME>", value="Bans a player from the server.")
        embed.add_field(name=f"{PREFIX}save", value="Save the world.")
        embed.add_field(name=f"{PREFIX}exit", value="Save and exit the world.")
        embed.add_field(name=f"{PREFIX}settle", value="Settle the moving water.")
        embed.add_field(name=f"{PREFIX}help", value="Shows the help message.")
        
        #send the embed
        await ctx.send(embed=embed)

    #run the bot
    bot.run(TOKEN)
