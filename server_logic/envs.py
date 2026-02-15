import os
import re
from pathlib import Path
from dotenv import load_dotenv

#get the info from the .env file
load_dotenv()

#get the path logs and replace ~ with the absolute path
PLAYER_LOG = Path(os.getenv("PLAYER_LOGS")).expanduser()
CHAT_LOG = Path(os.getenv("CHAT_LOGS")).expanduser()
OTHER_LOG = Path(os.getenv("OTHER_LOGS")).expanduser()
BANLIST = Path(os.getenv("BANLIST")).expanduser()
APPROVED_IP_FILE = Path(os.getenv("APPROVED_IPS")).expanduser()
WORLD_SAVE = Path(os.getenv("WORLD_SAVE")).expanduser()
WORLD_BACKUP_DIR = Path(os.getenv("WORLD_BACKUP")).expanduser()

#check if the discord bot is being used to get the other info
TOKEN = os.getenv("TOKEN")
if (len(TOKEN) > 0):
    ADMIN_ROLE_ID = int(os.getenv("ADMIN_ROLE_ID"))
    BOT_CHANNEL_ID = int(os.getenv("BOT_CHANNEL_ID"))
    CHAT_CHANNEL_ID = int(os.getenv("CHAT_CHANNEL_ID"))
    NOTIFY_CHANNEL_ID = int(os.getenv("NOTIFY_CHANNEL_ID"))

#get the server settings
BACKUP_TIMER = int(os.getenv("BACKUP_DURATION"))
BACKUP_NOTIFY = eval(os.getenv("BACKUP_NOTIFY"))
PLAYER_JOIN_NOTIFY = eval(os.getenv("PLAYER_JOIN_NOTIFY"))
PLAYER_LEAVE_NOTIFY = eval(os.getenv("PLAYER_LEAVE_NOTIFY"))

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

#filter to only show numbers
number_regex = re.compile(r'\d+')

#tell the server to restart
RESTARTING = False