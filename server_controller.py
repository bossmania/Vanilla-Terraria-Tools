import re
import time
import sys
import pathlib
import threading
import subprocess
from os import path
from datetime import datetime
from offline_ban import ban_player

#store the logs and server binary location with args
LOG_FOLDER = f"{pathlib.Path.home()}/logs/"
PLAYER_LOG = path.join(LOG_FOLDER, "player.log")
CHAT_LOG = path.join(LOG_FOLDER, "chat.log")
OTHER_LOG = path.join(LOG_FOLDER, "other.log")
BANLIST = path.join(path.join(pathlib.Path.home(), "banlist.txt"))
SERVER_CMD = sys.argv[1:]

#regex filters (ChatGPT wrote them cause I'll never understand regex)
# Match anything with <...> or : <...> in it
chat_regex = re.compile(r'^:?\s*<[^<>]+>')
#match anything with a (IP:Port)
IP_regex = re.compile(r'\(\b\d{1,3}(?:\.\d{1,3}){3}:\d{1,5}\b\)')
#filter for only the username and IP
user_IP_regex = re.compile(r':?\s*([^\s(]+)\s*\((\d{1,3}(?:\.\d{1,3}){3}):\d{1,5}\)')
#regex for removing everything but the username in the /kick command
kick_regex = re.compile(r".*/kick\s+")
#regex for removing everything but the username in the /ban command
ban_regex = re.compile(r".*/ban\s+")

#add the timestamp to the line
def timestamp(line):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"[{timestamp}] {line}"

#format the line to be "username [IP]"
def format_user_ip(line):
    #filter the line and check if it's valid 
    result = user_IP_regex.search(line)
    if not result:
        return None
    
    #format the results
    username, ip = result.groups()
    return f"{username} [{ip}]"

#write to the a log file
def write_log(line, log):
    with open(path.join(LOG_FOLDER, log), "a", buffering=1) as logfile:
        logfile.write(line  + "\n")
        logfile.flush()

#save the player to the player log if needed
def write_player(line):
    with open(PLAYER_LOG, "a", buffering=1) as logfile:
        #format the line and check if they're not in the log
        formated_player = format_user_ip(line)
        if not player_in_log(formated_player):

            #write to the log
            logfile.write(formated_player  + "\n")
            logfile.flush()

#check if the player is already in the log to prevent spam 
def player_in_log(person):
    with open(PLAYER_LOG, "r", buffering=1) as logfile:
        #get the players from the file
        players = logfile.read().splitlines()
        for player in players:

            #check if the player is in the list
            if person in player:
                return True

        return False

#check the amount of players every 7 seconds
def check_players(proc):
    while True:
        time.sleep(7)
        proc.stdin.write("playing\n")
        proc.stdin.flush()

#command handler
def command_checker(line, proc):
    #handle /kick command
    if "/kick" in line:
        #get the username
        user = kick_regex.sub("", line)
        
        #kick the user and say that they're kicked
        proc.stdin.write(f"kick {user}\n")
        proc.stdin.write(f"say Kiced {user} from the server!\n")
        proc.stdin.flush()
    
    #handle /ban command
    if "/ban" in line:
        #get the username
        user = ban_regex.sub("", line)

        #banned the player and show it to the chat
        response = ban_player(PLAYER_LOG, BANLIST, user)
        print(timestamp(f"FROM OFFLINE_BAN: {response}"))

        #kick them from the server
        proc.stdin.write(f"kick {user}\n")
        proc.stdin.write(f"say Banned {user} from the server!\n")
        proc.stdin.flush()



def read_output(proc):
    #get stdout
    for raw in proc.stdout:
        #clean up the line
        line = raw.rstrip("\n")

        #check if the line was a command, and execute on it
        command_checker(line, proc)

        #timestamp the stdout line
        stamped = timestamp(line)

        # print to console
        print(stamped)

        #check if the line matches a regex filter for the log file to store at
        if chat_regex.search(line):
            write_log(stamped, CHAT_LOG)
        elif IP_regex.search(line):
            write_player(line)
        else:
            write_log(stamped, OTHER_LOG)


#read the keyboard input and send it
def read_input(proc):
    for line in sys.stdin:
        proc.stdin.write(line)
        proc.stdin.flush()


def main():
    #start the server
    proc = subprocess.Popen(
        SERVER_CMD,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    #start controlling the stdin and stdout of the server
    threading.Thread(target=read_output, args=(proc,), daemon=True).start()
    threading.Thread(target=read_input, args=(proc,), daemon=True).start()
    threading.Thread(target=check_players, args=(proc,), daemon=True).start()

    #wait for the server to stop before stopping the script
    proc.wait()


if __name__ == "__main__":
    main()
