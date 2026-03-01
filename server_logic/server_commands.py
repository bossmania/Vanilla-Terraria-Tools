import envs
import logger

#wrapper function to easily say a message in the game chat
def say(msg, proc):
    proc.stdin.write(f"say {msg}\n")
    proc.stdin.flush()

def kick(line, proc):
    #get the username
    user = envs.kick_regex.sub("", line)
    
    #kick the user and say that they're kicked
    proc.stdin.write(f"kick {user}\n")
    msg = f"Kicked {user} from the server!"
    say(msg, proc)
    
    return msg
