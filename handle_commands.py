import re
import logger
import threading
import offline_ban

#regex filters (ChatGPT wrote them cause I'll never understand regex)
#regex for removing everything but the username in the /kick command
kick_regex = re.compile(r".*/kick\s+")
#regex for removing everything but the username in the /ban command
ban_regex = re.compile(r".*/ban\s+")

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