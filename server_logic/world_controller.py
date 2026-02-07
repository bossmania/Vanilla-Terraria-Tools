import os
import sys
import shutil
import pathlib 
import path_grabber
from datetime import datetime

#get the folder where the worlds are saved at
WORLDS = os.path.join(pathlib.Path.home(), ".local/share/Terraria/Worlds")

#reformat the timestamp to make it easier to read
def timestamp_cleaner(timestamp):
    return timestamp.replace("-", "/").replace("__", " ").replace("_", ":")

def backup_world():
    # timestamp like: 2026-02-04__14_32_10
    timestamp = datetime.now().strftime("%Y-%m-%d__%H_%M_%S")
    copy_path = os.path.join(path_grabber.WORLD_BACKUP_DIR, timestamp)

    # ensure backup directory exists
    pathlib.Path.mkdir(pathlib.Path(path_grabber.WORLD_BACKUP_DIR), parents=True, exist_ok=True)

    # copy recursively, following symlinks (-L behavior)
    shutil.copytree(WORLDS, copy_path, symlinks=False)
    
    #return the timestamp in a better format
    return timestamp_cleaner(timestamp)

def get_restore_points(amount):
    #prep the backup list 
    backups = []

    #get the list of backups and add them to the list
    for backup in os.listdir(path_grabber.WORLD_BACKUP_DIR):
        backups.append(timestamp_cleaner(backup))
    
    #sort the backup list in desc order and only show the amount needed 
    backups.sort(reverse=True)
    return backups[0:amount]