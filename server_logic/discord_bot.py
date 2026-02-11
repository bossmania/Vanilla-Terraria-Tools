import envs
import discord
import handle_commands
import world_controller
from discord.ext import commands

#set the prefix used
PREFIX = "!"

#set the discrod bot to have default permission and the ability to read messages and see member info
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

#create the bot client and disable the built in help command
bot = commands.Bot(command_prefix=PREFIX, intents=intents)
bot.help_command = None

async def player_count(amount):
    #set the bot's activity to be X players online
    activity = discord.Activity(type=discord.ActivityType.watching, name=f"{amount} players online!")
    await bot.change_presence(activity=activity)

async def chat_log(msg):
    #get the chat channel and check if it's real
    channel = bot.get_channel(envs.CHAT_CHANNEL_ID)
    if channel:
        #get the username and message
        username = envs.user_regex.search(msg).group()
        message = msg.split(">")[1]

        #send the message as a embed
        embed = discord.Embed(title=username, description=message, color=0xeb7353)
        await channel.send(embed=embed)

async def notify(msg):
    #get the notify channel and check if it's real
    channel = bot.get_channel(envs.NOTIFY_CHANNEL_ID)
    if channel:
        #send the message
        await channel.send(msg)

def can_run_command():
    async def predicate(ctx):
        #check if the user has the admin role and is in the right channel
        for role in ctx.author.roles:
            if role.id == envs.ADMIN_ROLE_ID and ctx.channel.id == envs.BOT_CHANNEL_ID:
                return True

        #return false if they can't run the command
        return False

    #run the predicate on the command
    return commands.check(predicate)

def start_bot(proc):
    #say when the bot is online
    @bot.event
    async def on_ready():
        print(f"Logged in as {bot.user}")

    #kick command 
    @bot.command()
    @can_run_command()
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
    @can_run_command()
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
    @can_run_command()
    async def backup(ctx):
        #backup the world
        msg = handle_commands.backup(proc)
        await ctx.send(msg)
    
    #rollback command 
    @bot.command(aliases=["restore"])
    @can_run_command()
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
    @can_run_command()
    async def save(ctx):
        #save the world
        msg = handle_commands.save(proc)
        await ctx.send(msg)

    #exit command 
    @bot.command()
    @can_run_command()
    async def exit(ctx):
        #exit the world
        msg = handle_commands.exit(proc)
        await ctx.send(msg)

    #exit-nosave command 
    @bot.command(aliases=["exit-nosave"])
    @can_run_command()
    async def exit_nosave(ctx):
        #exit the world
        msg = handle_commands.exit_nosave(proc)
        await ctx.send(msg)
    
    #settle command 
    @bot.command()
    @can_run_command()
    async def settle(ctx):
        #settle the world's water
        msg = handle_commands.settle(proc)
        await ctx.send(msg)

    #help command
    @bot.command()
    @can_run_command()
    async def help(ctx):
        #create the embed with title, desc, and color
        embed=discord.Embed(title="Help Commands", description="shows all of the help commands", color=0x2ec27e)

        #set all of the commands
        embed.add_field(name=f"{PREFIX}kick <USERNAME>", value="Kicks a player from the server.",inline=False)
        embed.add_field(name=f"{PREFIX}ban <USERNAME>", value="Bans a player from the server.",inline=False)
        embed.add_field(name=f"{PREFIX}backup", value="Backup up the world.",inline=False)
        embed.add_field(name=f"{PREFIX}rollback ({PREFIX}restore)", value="rollback to a backup from a list of recent backups.",inline=False)
        embed.add_field(name=f"{PREFIX}save", value="Save the world.",inline=False)
        embed.add_field(name=f"{PREFIX}exit", value="Save and exit the world.",inline=False)
        embed.add_field(name=f"{PREFIX}exit-nosave ({PREFIX}exit_nosave)", value="Exit the world without saving.",inline=False)
        embed.add_field(name=f"{PREFIX}settle", value="Settle the moving water.",inline=False)
        embed.add_field(name=f"{PREFIX}help", value="Shows the help message.",inline=False)
        
        #send the embed
        await ctx.send(embed=embed)

    #run the bot
    bot.run(envs.TOKEN)
