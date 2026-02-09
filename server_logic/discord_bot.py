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

    #run the bot
    bot.run(TOKEN)
