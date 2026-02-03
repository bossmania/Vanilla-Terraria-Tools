import re
import logger
import pathlib
import threading
import offline_ban
from os import path

#regex filters (ChatGPT wrote them cause I'll never understand regex)
#regex for removing everything but the username in the /kick command
kick_regex = re.compile(r".*/kick\s+")
#regex for removing everything but the username in the /ban command
ban_regex = re.compile(r".*/ban\s+")
#regex to delete everything except for the username
user_regex = re.compile(r"(?<=<)[^<>]+(?=>)")

#file that stores the IPs that are allowed to run / commands
approved_IPs_file = path.join(path.join(pathlib.Path.home(), "admin", "ApprovedIPs.txt"))

#get the users 
def check_if_allowed(player_file, line):
    #get the user and prep the IP search
    talked_user = user_regex.search(line).group()
    print(talked_user)
    IPs = []
    
    #open the player list and get all of the players
    with open(player_file, "r", buffering=1) as player_log:
        players = player_log.read().splitlines()

        for player in players:
            #get the username & IP for that player
            results = offline_ban.user_IP_regex.search(player)
            if not results:
                raise Exception("The player file is not formatted properly!")
            
            #save the IP if the current user is the talked user
            user, IP = results.groups()
            if user == talked_user:
                IPs.append(IP)

    #get all of the approved IPs
    with open(approved_IPs_file, "r", buffering=1) as IP_log:
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
    user = kick_regex.sub("", line)
    
    #kick the user and say that they're kicked
    proc.stdin.write(f"kick {user}\n")
    proc.stdin.write(f"say Kicked {user} from the server!\n")
    proc.stdin.flush()

def ban(line, proc, BANLIST):
    #get the username
    user = ban_regex.sub("", line)

    #banned the player and show it to the chat
    response = offline_ban.ban_player(logger.PLAYER_LOG, BANLIST, user)
    print(logger.timestamp(f"FROM OFFLINE_BAN: {response}"))

    #kick them from the server
    proc.stdin.write(f"kick {user}\n")
    proc.stdin.write(f"say Banned {user} from the server!\n")
    proc.stdin.flush()

def save(proc):
    #save the world
    proc.stdin.write(f"save\n")
    proc.stdin.write(f"say Sucessfully saved the world!\n")
    proc.stdin.flush()

def exit(proc):
    #exit the server
    proc.stdin.write(f"exit\n")
    proc.stdin.flush()

def settle(proc):
    #settle all of the world in the world
    proc.stdin.write(f"settle\n")
    proc.stdin.write(f"say Sucessfully settled all of the water in the world!\n")
    proc.stdin.flush()