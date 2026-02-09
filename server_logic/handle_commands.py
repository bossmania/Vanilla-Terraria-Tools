import re
import envs
import logger
import pathlib
import threading
import offline_ban
from os import path
import world_controller
from datetime import datetime

#get the users 
def check_if_allowed(player_file, line):
    #get the user and prep the IP search
    talked_user = envs.user_regex.search(line).group()
    IPs = []
    
    #open the player list and get all of the players
    with open(player_file, "r", buffering=1) as player_log:
        players = player_log.read().splitlines()

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
    with open(envs.APPROVED_IP_FILE, "r", buffering=1) as IP_log:
        approved_IPs = IP_log.read().splitlines()

        #go through each approved IP, and the IPs match by the chatter
        for approved_IP in approved_IPs:
            for IP in IPs:
                #stop if the IP is in the approved list
                if IP == approved_IP:
                    return True

        #if the IP wasn't found in the list, then return false    
        return False

def kick(line, proc):
    #get the username
    user = envs.kick_regex.sub("", line)
    
    #kick the user and say that they're kicked
    proc.stdin.write(f"kick {user}\n")
    msg = f"Kicked {user} from the server!"
    proc.stdin.write(f"say {msg}\n")
    proc.stdin.flush()
    
    return msg

def ban(line, proc):
    #get the username
    user = envs.ban_regex.sub("", line)

    #banned the player and show it to the chat
    response = offline_ban.ban_player(envs.PLAYER_LOG, envs.BANLIST, user)
    print(logger.timestamp(f"FROM OFFLINE_BAN: {response}"))

    #kick them from the server
    proc.stdin.write(f"kick {user}\n")

    #say that they got kicked
    msg = f"Banned {user} from the server!"
    proc.stdin.write(f"say {msg}\n")
    proc.stdin.flush()

    return msg

def backup(proc):
    #backup the world create the msg
    timestamp = world_controller.timestamp_cleaner(world_controller.backup_world())
    msg = f"Sucessfully backup the world @ {timestamp}!"

    #say when it was backed
    proc.stdin.write(f"say {msg}!\n")
    proc.stdin.flush()

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
            proc.stdin.write(f"say {index+1}: {backup}\n")
        proc.stdin.flush()
        

def save(proc):
    #save the world
    proc.stdin.write(f"save\n")
    msg = f"Sucessfully saved the world"
    proc.stdin.write(f"say {msg}!\n")
    proc.stdin.flush()
    return msg

def exit(proc):
    #exit the server
    msg = f"Shutting down the world now!"
    proc.stdin.write(f"say {msg}\n")
    proc.stdin.write(f"exit\n")
    proc.stdin.flush()
    return msg

def settle(proc):
    #settle all of the world in the world
    proc.stdin.write(f"settle\n")
    msg = f"Sucessfully settled all of the water in the world!"
    proc.stdin.write(f"say {msg}\n")
    proc.stdin.flush()
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
    /settle: settles all of the liquids in the world.
    /admin: shows this help message. 
    """

    #split the help msg into multi lines and go through them
    msg_lines = msg.splitlines()
    for line in msg_lines:
        #strip the leading whitespaces and print the line
        line = line.lstrip()
        proc.stdin.write(f"say {line}\n")
    proc.stdin.flush()