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
        handle_commands.kick(user, proc)
        await ctx.send(f"Kicked {user} from the server!")

    #ban command 
    @bot.command()
    async def ban(ctx, user=None):
        #stop if there was no username provided
        if user == None or user == "":
            await ctx.send("Please enter in a username!")
            return

        #ban the player and say that they're ban
        handle_commands.ban(user, proc)
        await ctx.send(f"Banned {user} from the server!")

    #save command 
    @bot.command()
    async def save(ctx):
        #save the world
        handle_commands.save(proc)
        await ctx.send(f"Sucessfully saved the world!")

    #exit command 
    @bot.command()
    async def exit(ctx):
        #exit the world
        handle_commands.exit(proc)
        await ctx.send(f"Sucessfully saved and exited the world!")
    
    #settle command 
    @bot.command()
    async def settle(ctx):
        #settle the world's water
        handle_commands.settle(proc)
        await ctx.send(f"Sucessfully settled all of the water in the world!")

    #help command
    @bot.command()
    async def help(ctx):
        #create the embed with title, desc, and color
        embed=discord.Embed(title="Help Commands", description="shows all of the help commands", color=0x2ec27e)

        #set all of the commands
        embed.add_field(name=f"{PREFIX}help", value="Shows the help message.")
        embed.add_field(name=f"{PREFIX}kick <USERNAME>", value="Kicks a player from the server.")
        embed.add_field(name=f"{PREFIX}ban <USERNAME>", value="Bans a player from the server.")
        embed.add_field(name=f"{PREFIX}save", value="Save the world.")
        embed.add_field(name=f"{PREFIX}exit", value="Save and exit the world.")
        embed.add_field(name=f"{PREFIX}settle", value="Settle the moving water.")
        
        #send the embed
        await ctx.send(embed=embed)

    #run the bot
    bot.run(TOKEN)
