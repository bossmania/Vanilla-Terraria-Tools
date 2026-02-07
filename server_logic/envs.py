import re
import pathlib
from os import path

#prepare to get the paths
PATH_FILE = path.join(pathlib.Path.home(), "paths.txt")
BANLIST = ""
APPROVED_IP_FILE = ""
PLAYER_LOG = ""
CHAT_LOG = ""
OTHER_LOG = ""
WORLD_BACKUP_DIR = ""
WORLD_SAVE = ""

#regex filters (ChatGPT wrote them cause I'll never understand regex)
# Match anything with <...> or : <...> in it
chat_regex = re.compile(r'^:?\s*<[^<>]+>')

#match anything with a (IP:Port)
IP_regex = re.compile(r'\(\b\d{1,3}(?:\.\d{1,3}){3}:\d{1,5}\b\)')

#regex for removing everything but the username in the /kick command
kick_regex = re.compile(r".*/kick\s+")

#regex for removing everything but the username in the /ban command
ban_regex = re.compile(r".*/ban\s+")

#regex to delete everything except for the username
user_regex = re.compile(r"(?<=<)[^<>]+(?=>)")

#filter for only the username and IP
user_IP_regex = re.compile(r':?\s*([^\s(]+)\s*\((\d{1,3}(?:\.\d{1,3}){3}):\d{1,5}\)')

#filter for the username and IP inside []
User_IP_log_regex = re.compile(r'^(.+?)\s*\[(\d{1,3}(?:\.\d{1,3}){3})\]$')


def update_paths():
    #open the path files
    with open(PATH_FILE, "r", buffering=1) as path_file:
        paths = path_file.read().splitlines()

        #make sure to globaly edit the path varaibles
        global BANLIST
        global APPROVED_IP_FILE
        global PLAYER_LOG
        global CHAT_LOG
        global OTHER_LOG
        global WORLD_SAVE
        global WORLD_BACKUP_DIR

        for path in paths:
            #split the path into two parts, and replace ~ with the home path
            values = path.split("=")
            if "~" in values[1]:
                values[1] = values[1].replace("~", str(pathlib.Path.home()))

            #update the path value based on the input given
            match values[0]:
                case "chat_logs":
                    CHAT_LOG = values[1]
                case "player_logs":
                    PLAYER_LOG = values[1]
                case "other_logs":
                    OTHER_LOG = values[1]
                case "banlist":
                    BANLIST = values[1]
                case "approved_IPs":
                    APPROVED_IP_FILE = values[1]
                case "world_save":
                    WORLD_SAVE = values[1]
                case "world_backup":
                    WORLD_BACKUP_DIR = values[1]