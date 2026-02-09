import envs
import discord
import handle_commands
import world_controller
from discord.ext import commands

#set the prefix used
PREFIX = "!"

def admin_only(ADMIN_ROLE_ID):
    async def predicate(ctx):
        #check if the user has the admin role
        for role in ctx.author.roles:
            if role.id == ADMIN_ROLE_ID:
                return True
        
        #return false when no roles were found
        return False

    #run the predicate on the command
    return commands.check(predicate)

def bot_channel(BOT_CHANNEL_ID):
    async def predicate(ctx):
        # check if the message is in the right channel
        if ctx.channel.id == BOT_CHANNEL_ID:
            return True
        else:
            return False

    return commands.check(predicate)

def start_bot(TOKEN, ADMIN_ROLE_ID, BOT_CHANNEL_ID, CHAT_CHANNEL_ID, NOTIFY_CHANNEL_ID, proc):
    #set the discrod bot to have default permission and the ability to read messages and see member info
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    #create the bot client and disable the built in help command
    bot = commands.Bot(command_prefix=PREFIX, intents=intents)
    bot.help_command = None

    #say when the bot is online
    @bot.event
    async def on_ready():
        print(f"Logged in as {bot.user}")

    #kick command 
    @bot.command()
    @admin_only(ADMIN_ROLE_ID)
    @bot_channel(BOT_CHANNEL_ID)
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
    @admin_only(ADMIN_ROLE_ID)
    @bot_channel(BOT_CHANNEL_ID)
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
    @admin_only(ADMIN_ROLE_ID)
    @bot_channel(BOT_CHANNEL_ID)
    async def backup(ctx):
        #backup the world
        msg = handle_commands.backup(proc)
        await ctx.send(msg)
    
    #rollback command 
    @bot.command(aliases=["restore"])
    @admin_only(ADMIN_ROLE_ID)
    @bot_channel(BOT_CHANNEL_ID)
    async def rollback(ctx):
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
    @admin_only(ADMIN_ROLE_ID)
    @bot_channel(BOT_CHANNEL_ID)
    async def save(ctx):
        #save the world
        msg = handle_commands.save(proc)
        await ctx.send(msg)

    #exit command 
    @bot.command()
    @admin_only(ADMIN_ROLE_ID)
    @bot_channel(BOT_CHANNEL_ID)
    async def exit(ctx):
        #exit the world
        msg = handle_commands.exit(proc)
        await ctx.send(msg)
    
    #settle command 
    @bot.command()
    @admin_only(ADMIN_ROLE_ID)
    @bot_channel(BOT_CHANNEL_ID)
    async def settle(ctx):
        #settle the world's water
        msg = handle_commands.settle(proc)
        await ctx.send(msg)

    #help command
    @bot.command()
    @admin_only(ADMIN_ROLE_ID)
    @bot_channel(BOT_CHANNEL_ID)
    async def help(ctx):
        #create the embed with title, desc, and color
        embed=discord.Embed(title="Help Commands", description="shows all of the help commands", color=0x2ec27e)

        #set all of the commands
        embed.add_field(name=f"{PREFIX}kick <USERNAME>", value="Kicks a player from the server.")
        embed.add_field(name=f"{PREFIX}ban <USERNAME>", value="Bans a player from the server.")
        embed.add_field(name=f"{PREFIX}backup", value="Backup up the world.")
        embed.add_field(name=f"{PREFIX}rollback (/restore)", value="rollback to a backup from a list of recent backups.")
        embed.add_field(name=f"{PREFIX}save", value="Save the world.")
        embed.add_field(name=f"{PREFIX}exit", value="Save and exit the world.")
        embed.add_field(name=f"{PREFIX}settle", value="Settle the moving water.")
        embed.add_field(name=f"{PREFIX}help", value="Shows the help message.")
        
        #send the embed
        await ctx.send(embed=embed)

    #run the bot
    bot.run(TOKEN)
