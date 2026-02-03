import re
import pathlib
import subprocess
from os import path
from datetime import datetime

#store the logs paths
LOG_FOLDER = f"{pathlib.Path.home()}/logs/"
PLAYER_LOG = path.join(LOG_FOLDER, "player.log")
CHAT_LOG = path.join(LOG_FOLDER, "chat.log")
OTHER_LOG = path.join(LOG_FOLDER, "other.log")

#regex filters (ChatGPT wrote them cause I'll never understand regex)
#filter for only the username and IP
user_IP_regex = re.compile(r':?\s*([^\s(]+)\s*\((\d{1,3}(?:\.\d{1,3}){3}):\d{1,5}\)')

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