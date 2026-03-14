import envs
import logger
import asyncio
from commands import server_commands
from discord_bot import discord_bot_notify

def control_output(line, proc):
    #timestamp the stdout line and print it
    stamped = logger.timestamp(line)
    print(stamped)

    #organize the messages for logging
    organize_log_messages(line, stamped, proc)

    #check if the output was a command
    command_checker(line, proc)

    #get the list of online players
    get_online_players(line)

    #check if the world is currently saving
    check_if_saving(line)

    #function to check the world status
    check_world_status(line)

    #notify when a player joins the world
    player_notify(line)

def organize_log_messages(line, stamped, proc):
    #log the player's IP
    if envs.IP_regex.search(line):
        logger.write_player(line)

    #log the chat message
    elif envs.chat_regex.search(line):
        #log the chat message
        logger.write_log(stamped, envs.CHAT_LOG)

        #send the chat message to discord if using it
        if len(envs.TOKEN) > 0:
            asyncio.run_coroutine_threadsafe(discord_bot_notify.chat_log(line), envs.BOT.bot.loop)

    #log everything else
    else:
        logger.write_log(stamped, envs.OTHER_LOG)

def get_online_players(line):
    #filter the line and check if it's valid 
    result = envs.user_IP_regex.search(line)
    if not result:
        return None

    #get the username
    username, _ = result.groups()

    #add the username to the online list
    envs.ONLINE.append(username)

#func to check if the world is currently saving
def check_if_saving(line):
    if "Saving world data:" in line:
        envs.CURRENTLY_SAVING = True
    elif "Backing up world file" in line:
        envs.CURRENTLY_SAVING = False

def check_world_status(line):
        #set the world status to be laoded when the server is up
        if "Server started" in line:
            envs.WORLD_LOADED = True

            #notify on discord that the server is up if it's using discord
            if len(envs.TOKEN) > 0:
                asyncio.run_coroutine_threadsafe(discord_bot_notify.notify("The server has booted up!"), envs.BOT.bot.loop)
                asyncio.run_coroutine_threadsafe(discord_bot_notify.bot_activity("0 players online!"), envs.BOT.bot.loop)

def player_notify(line):
    #check if player joined/left, and can notify about it
    notify = False
    if "has joined" in line and envs.PLAYER_JOIN_NOTIFY: 
        notify = True
    if "has left" in line and envs.PLAYER_LEAVE_NOTIFY:
        notify = True
    
    #notify about the player joining/leaving
    if notify:
        asyncio.run_coroutine_threadsafe(discord_bot_notify.notify(line), envs.BOT.bot.loop)

def check_user_permission(line):
    #get the user and prep the IP search
    results = envs.user_regex.search(line)

    #get the user if it's valid
    if not results:
        return
    talked_user = results.group()
    
    IPs = []

    #get the list of players
    envs.PLAYER_LOG.seek(0)
    players = envs.PLAYER_LOG.read().splitlines()

    for player in players:
        #get the username & IP for that player
        results = envs.User_IP_log_regex.search(player)
        if not results:
            raise Exception("The player file is not formatted properly!")
        
        #save the IP if the current user is the talked user
        user, IP = results.groups()
        if user == talked_user:
            IPs.append(IP)

    #get all of the approved IPs
    envs.APPROVED_IP.seek(0)
    approved_IPs = envs.APPROVED_IP.read().splitlines()

    #go through each approved IP, and the IPs match by the chatter
    for approved_IP in approved_IPs:
        for IP in IPs:
            #stop if the IP is in the approved list
            if IP == approved_IP:
                return True

    #if the IP wasn't found in the list, then return false    
    return False

def command_checker(line, proc):
    #check if the player has permission to run commands
    if check_user_permission(line):
        #lowercase the command line for auto caps
        line = line.lower()

        #/kick command
        if "/kick" in line:
            server_commands.kick(line, proc)
        
        #/ban command
        elif "/ban" in line:
            server_commands.ban(line, proc)

        #/backup command
        elif "/backup" in line:
            server_commands.backup(proc)

        #/restore (or /rollback) command
        elif "/restore" in line or "/rollback" in line:
            server_commands.restore(line, proc)

        #/exit-nosave command    
        elif "/exit-nosave" in line:
            server_commands.exit_nosave(proc)

        #/save command
        elif "/save" in line:
            server_commands.save(proc)

        #/exit command    
        elif "/exit" in line:
            server_commands.exit(proc)

        #/settle command    
        elif "/settle" in line:
            server_commands.settle(proc)

        #/admin command
        elif "/admin" in line:
            server_commands.help(proc)