import pathlib
from os import path

#prepare to get the paths
PATH_FILE = path.join(pathlib.Path.home(), "paths.txt")
BANLIST = ""
APPROVED_IP_FILE = ""
PLAYER_LOG = ""
CHAT_LOG = ""
OTHER_LOG = ""

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