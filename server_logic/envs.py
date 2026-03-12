import os
import re
from pathlib import Path
from dotenv import load_dotenv

#check if the server should restart
RESTART = False

#check if the threads should be stooped
STOP_THREADS = False
RUNNING_THREADS = []

#list of online players
ONLINE = []

CURRENTLY_SAVING = False

#get the info from the .env file
load_dotenv()

#get the path logs
PLAYER_LOG_PATH = Path(os.getenv("PLAYER_LOGS")).expanduser()
CHAT_LOG_PATH = Path(os.getenv("CHAT_LOGS")).expanduser()
OTHER_LOG_PATH = Path(os.getenv("OTHER_LOGS")).expanduser()

#replace ~ with the absolute path
BANLIST_PATH = Path(os.getenv("BANLIST")).expanduser()
APPROVED_IP_PATH = Path(os.getenv("APPROVED_IPS")).expanduser()
WORLD_SAVE = Path(os.getenv("WORLD_SAVE")).expanduser()
WORLD_BACKUP_DIR = Path(os.getenv("WORLD_BACKUP")).expanduser()

#open the files needed
PLAYER_LOG = open(PLAYER_LOG_PATH, "a+", buffering=1)
CHAT_LOG = open(CHAT_LOG_PATH, "a+", buffering=1)
OTHER_LOG = open(OTHER_LOG_PATH, "a+", buffering=1)
BANLIST = open(BANLIST_PATH, "a+", buffering=1)
APPROVED_IP = open(APPROVED_IP_PATH, "r", buffering=1)

#get the server settings
PLAYER_JOIN_NOTIFY = eval(os.getenv("PLAYER_JOIN_NOTIFY"))
PLAYER_LEAVE_NOTIFY = eval(os.getenv("PLAYER_LEAVE_NOTIFY"))
PLAYER_CHECK_FREQ = int(os.getenv("PLAYER_CHECK_FREQ"))
BACKUP_NOTIFY = eval(os.getenv("BACKUP_NOTIFY"))
BACKUP_TIMER = int(os.getenv("BACKUP_DURATION"))
STORAGE_NOTIFY = eval(os.getenv("STORAGE_NOTIFY"))
STORAGE_NOTIFY_THRESHOLD = int(os.getenv("STORAGE_NOTIFY_THRESHOLD"))
STORAGE_NOTIFY_COOLDOWN = int(os.getenv("STORAGE_NOTIFY_COOLDOWN"))

#regex filters (ChatGPT wrote them cause I' cant wrap my brain around regex)
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
user_IP_regex = re.compile(r':?\s*(.*?)\s*\((\d{1,3}(?:\.\d{1,3}){3}):\d{1,5}\)')

#filter for the username and IP inside []
User_IP_log_regex = re.compile(r'^(.+?)\s*\[(\d{1,3}(?:\.\d{1,3}){3})\]$')

#filter to only show numbers
number_regex = re.compile(r'\d+')