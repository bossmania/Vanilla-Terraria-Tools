import os
import sys
import envs
import time
import shutil
import pathlib 
from datetime import datetime

#reformat the timestamp to make it easier to read
def timestamp_cleaner(timestamp):
    timestamp_formatted = timestamp.replace("-", "/").replace("__", " ").replace("_", ":")
    return f"{timestamp_formatted} {datetime.now().astimezone().strftime("%Z")}"

def backup_world():
    # timestamp like: 2026-02-04__14_32_10
    timestamp = datetime.now().strftime("%Y-%m-%d__%H_%M_%S")
    copy_path = os.path.join(envs.WORLD_BACKUP_DIR, timestamp)

    # ensure backup directory exists
    pathlib.Path.mkdir(pathlib.Path(envs.WORLD_BACKUP_DIR), parents=True, exist_ok=True)

    # copy recursively, following symlinks (-L behavior)
    shutil.copytree(envs.WORLD_SAVE, copy_path, symlinks=False)
    
    #return the timestamp
    return timestamp
    
def get_restore_points(amount, cleanup=True):
    #prep the backup list 
    backups = []

    #get the list of backups and add them to the list
    for backup in os.listdir(envs.WORLD_BACKUP_DIR):
        #clean of the timestamp if needed
        if (cleanup):
            backup = timestamp_cleaner(backup)
        
        backups.append(backup)
    
    #sort the backup list in desc order and only show 8
    backups.sort(reverse=True)
    return backups[0:amount]

def restore_backup(amount, index, proc):
    #get the specific backup and the path to it
    backup = get_restore_points(amount, cleanup=False)[index]
    backup_folder = os.path.join(envs.WORLD_BACKUP_DIR, backup)

    for file in os.listdir(backup_folder):
        #get the new and old world files path
        old_file = os.path.join(envs.WORLD_SAVE, file)
        new_file = os.path.join(backup_folder, file)

        #over write them
        shutil.copy2(new_file, old_file)

    #tell the server to restart
    envs.RESTARTING = True

    #exit the server without saving
    proc.stdin.write(f"say Rolling back the server to {timestamp_cleaner(backup)} now\n")
    proc.stdin.write("exit-nosave\n")
    proc.stdin.flush()
    