import envs
import discord
from discord.ext import commands
from discord_bot import discord_bot
from commands import server_commands, world_controller

def initalize(self, bot, proc):
    #kick command 
    @bot.command()
    async def kick(ctx, user=None):
        if discord_bot.can_run_command(ctx):
            #stop if there was no username provided
            if user == None or user == "":
                await ctx.send("Please enter in a username!")
                return

            #kick the player and say that they're kicked
            msg = server_commands.kick(user, proc)
            await ctx.send(msg)
    
    #ban command 
    @bot.command()
    async def ban(ctx, user=None):
        if discord_bot.can_run_command(ctx):
            #stop if there was no username provided
            if user == None or user == "":
                await ctx.send("Please enter in a username!")
                return

            #ban the player and say that they're ban
            msg = server_commands.ban(user, proc)
            await ctx.send(msg)

    #backup command 
    @bot.command()
    async def backup(ctx):
        if discord_bot.can_run_command(ctx):
            #backup the world
            msg = server_commands.backup(proc)
            await ctx.send(msg)
    
    #rollback command 
    @bot.command(aliases=["restore"])
    async def rollback(ctx):
        if discord_bot.can_run_command(ctx):
            #func to check when to stop waiting
            def check(message):
                #pass when the owner respond back at the same channel
                return message.author == ctx.author and message.channel == ctx.channel
            
            #get the amount of most recent backups
            AMOUNT = 20
            rollbacks = world_controller.get_restore_points(AMOUNT)

            #create the embed with title, desc, and color
            embed=discord.Embed(title="Backup Lists", description="shows all of the recent backups.", color=0x966b59)

            #list all of the rollback version in the embed
            for index, rollback in enumerate(rollbacks):
                embed.add_field(name=str(index+1), value=rollback, inline=False)

            #send the embed and the respond msg
            await ctx.send(embed=embed)
            await ctx.send(f"Respond with the number you want to rollback to. (EX: respond with **1** if you want to rollback to {rollbacks[0]})")
            
            #wait for the response, and get the number from it within 2 mins
            msg = await bot.wait_for("message", check=check,timeout=120)
            rollback_ver = int(envs.number_regex.search(msg.content).group())

            #rollback the world now
            await ctx.send(f"Got it! Going to rollback to {rollbacks[rollback_ver-1]} now!")
            world_controller.restore_backup(AMOUNT, rollback_ver-1, proc)

    #save command 
    @bot.command()
    async def save(ctx):
        if discord_bot.can_run_command(ctx):
            #save the world
            msg = server_commands.save(proc)
            await ctx.send(msg)

    #exit command 
    @bot.command()
    async def exit(ctx):
        if discord_bot.can_run_command(ctx):
            #exit the world
            msg = server_commands.exit(proc)
            await ctx.send(msg)

    #exit-nosave command 
    @bot.command(aliases=["exit-nosave"])
    async def exit_nosave(ctx):
        if discord_bot.can_run_command(ctx):
            #exit the world
            msg = server_commands.exit_nosave(proc)
            await ctx.send(msg)
    
    #settle command 
    @bot.command()
    async def settle(ctx):
        if discord_bot.can_run_command(ctx):
            #settle the world's water
            msg = server_commands.settle(proc)
            await ctx.send(msg)

    #help command
    @bot.command(aliases=["admin"])
    async def help(ctx):
        if discord_bot.can_run_command(ctx):
            #create the embed with title, desc, and color
            embed=discord.Embed(title="Help Commands", description="shows all of the help commands", color=0x2ec27e)

            #set all of the commands
            embed.add_field(name=f"{self.PREFIX}kick <USERNAME>", value="Kicks a player from the server.",inline=False)
            embed.add_field(name=f"{self.PREFIX}ban <USERNAME>", value="Bans a player from the server.",inline=False)
            embed.add_field(name=f"{self.PREFIX}backup", value="Backup up the world.",inline=False)
            embed.add_field(name=f"{self.PREFIX}rollback ({self.PREFIX}restore)", value="rollback to a backup from a list of recent backups.",inline=False)
            embed.add_field(name=f"{self.PREFIX}save", value="Save the world.",inline=False)
            embed.add_field(name=f"{self.PREFIX}exit", value="Save and exit the world.",inline=False)
            embed.add_field(name=f"{self.PREFIX}exit-nosave ({self.PREFIX}exit_nosave)", value="Exit the world without saving.",inline=False)
            embed.add_field(name=f"{self.PREFIX}settle", value="Settle the moving water.",inline=False)
            embed.add_field(name=f"{self.PREFIX}help ({self.PREFIX}admin)", value="Shows the help message.",inline=False)
            
            #send the embed
            await ctx.send(embed=embed)