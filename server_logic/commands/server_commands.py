import envs
import logger
import asyncio
from discord_bot import discord_bot_notify
from commands import offline_ban, world_controller

#wrapper function to easily say a message in the game chat
def say(msg, proc):
    proc.stdin.write(f"say {msg}\n")
    proc.stdin.flush()

def kick(line, proc):
    #get the username
    user = envs.kick_regex.sub("", line)
    
    #check if the user is online
    found = False
    for player in envs.ONLINE:
        if player.lower() == user.lower():
            found = True
            break

    if found:
        #kick the user and say that they're kicked
        proc.stdin.write(f"kick {user}\n")
        msg = f"Kicked {user} from the server!"
        say(msg, proc)
        return msg 
    else:
        #say that the user can't be kicked
        msg = f"Can't kick {user} cause they're not online"
        say(msg, proc)
        return msg 
    
def ban(line, proc):
    #get the username
    user = envs.ban_regex.sub("", line)

    #banned the player
    msg = offline_ban.ban_player(user)

    #kick them from the server in order for them to get banned
    proc.stdin.write(f"kick {user}\n")

    #say that they got kicked
    say(msg, proc)

    return msg

def backup(proc):
    #backup the world create the msg
    timestamp = world_controller.timestamp_cleaner(world_controller.backup_world())
    msg = f"Sucessfully backup the world @ {timestamp}!"

    #say when it was backed
    say(msg, proc)

    return msg

def restore(line, proc):
    #delete the username from the command
    line = envs.chat_regex.sub("", line)[1:]

    #the amount of backups to show in chat
    AMOUNT = 8
    
    #check if the command has an args
    args = line.split(" ")
    if (len(args) > 1):
        #rollback the world to that point
        rollback_ver = line.split(" ")[1]
        world_controller.restore_backup(AMOUNT, int(rollback_ver) - 1, proc)
    else:
        #get the list of backups
        backups = world_controller.get_restore_points(AMOUNT)

        #display the backups with their index
        for index, backup in enumerate(backups):
            backup = f"{index+1}: {backup}"
            say(backup, proc)
        
def save(proc):
    #save the world
    proc.stdin.write(f"save\n")
    msg = f"Sucessfully saved the world!"
    say(msg, proc)
    return msg

def exit(proc):
    #exit the server
    msg = f"Shutting down the world now!"
    say(msg, proc)

    #notify that the world is exiting on discord, if using it
    if len(envs.TOKEN) > 0:
        asyncio.run_coroutine_threadsafe(discord_bot_notify.notify(msg), envs.BOT.bot.loop)

    proc.stdin.write(f"exit\n")
    proc.stdin.flush()
    return msg

def exit_nosave(proc):
    #exit the server
    msg = f"Shutting down the world now without saving!"
    say(msg, proc)

    #notify that the world is exiting on discord, if using it
    if len(envs.TOKEN) > 0:
        asyncio.run_coroutine_threadsafe(discord_bot_notify.notify(msg), envs.BOT.bot.loop)

    proc.stdin.write(f"exit-nosave\n")
    proc.stdin.flush()
    return msg

def settle(proc):
    #settle all of the world in the world
    proc.stdin.write(f"settle\n")
    msg = f"Settling all of the water in the world!"
    say(msg, proc)
    return msg

def help(proc):
    #the help message
    msg = """/kick <USERNAME>: kicks a player from the server.
    /ban <USERNAME>: bansa player from the server (can ban offline people).
    /save: save the world at the current's state.
    /backup: backup the world right now.
    /rollback (/restore): shows the last 8 backups.
    /rollback (/restore) <NUMBER>: restore the world to the backup corresponding with the number.
    /exit: exits (and saves) the server.
    /exit-nosave: exit the server without saving.
    /settle: settles all of the liquids in the world.
    /admin: shows this help message. 
    """

    #split the help msg into multi lines and go through them
    msg_lines = msg.splitlines()
    for line in msg_lines:
        #strip the leading whitespaces and print the line
        line = line.lstrip()
        say(line, proc)