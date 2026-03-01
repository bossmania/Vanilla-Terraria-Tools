import envs
import logger
import offline_ban

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