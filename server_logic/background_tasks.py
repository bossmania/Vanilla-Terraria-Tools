import os
import sys
import envs
import time
import shutil
import logger
import output_controller
from commands import world_controller

#func to read the user's input
def read_input(proc):
    #add itself to the threads list
    envs.RUNNING_THREADS.append("read_input")

    # dont wait for a stdin input
    os.set_blocking(sys.stdin.fileno(), False)
    
    #infinite loop
    while True:
        try:
            #stop when told so
            if envs.STOP_THREADS:
                envs.RUNNING_THREADS.remove("read_input")
                return

            #get the line and send it to the proc
            line = sys.stdin.readline()
            if line:
                proc.stdin.write(line)
                proc.stdin.flush()
        
        #theres no data yet, so try again
        except BlockingIOError:
            time.sleep(0.05)

#func to read the user's output
def read_output(proc):
    for raw in proc.stdout:
        #clean up the line
        line = raw.rstrip("\n")
        line = line.removeprefix(": ")

        #control what happens based on the output
        output_controller.control_output(line, proc)


#check the amount of players every few seconds and clear the online list
def check_players(proc):
    #add itself to the running thread list
    envs.RUNNING_THREADS.append("check_players")
    while True:
        #check every 0.1 seconds for if the thread should die
        for _ in range(envs.PLAYER_CHECK_FREQ * 10):
            #remove itself from the list and stop running when told so
            if envs.STOP_THREADS:
                envs.RUNNING_THREADS.remove("check_players")
                return

            time.sleep(0.1)

        #get the player list and reset the online queue
        proc.stdin.write("playing\n")
        proc.stdin.flush()
        envs.ONLINE = []

#func to auto backup the world
def auto_backup_world():
    #prep the backup timer
    BACKUP_TIMER_DURATION = envs.BACKUP_TIMER
    BACKUP = False

    while True:
        if BACKUP:
            #backup the world 
            timestamp = world_controller.backup_world()
            timestamp = world_controller.timestamp_cleaner(timestamp)
            
            #say that it got backup in console
            msg = logger.timestamp(f"Just saved the world at {timestamp}!")
            print(msg)

            #reset the backup timer
            BACKUP = False
            BACKUP_TIMER_DURATION = 10
        else:
            #check if anyone's online before starting the backup timer
            if len(envs.ONLINE) > 0:
                #decrease the backup timer by one second
                time.sleep(1)
                BACKUP_TIMER_DURATION -= 1

                #start the backup when enough time has passed
                if BACKUP_TIMER_DURATION <= 0:
                    BACKUP = True

def check_storage():
    while True:
        #wait for the cooldown for the storage
        time.sleep(envs.STORAGE_NOTIFY_COOLDOWN)

        #see how much of the storage is used
        total, used, free = shutil.disk_usage("/")
        percent_used = round((used / total) * 100, 1)

        #check if the storage is above the threshold and shold notify
        if percent_used > envs.STORAGE_NOTIFY_THRESHOLD and envs.STORAGE_NOTIFY:
            #get and send the message to the right place
            msg = f"The server's storage is at {percent_used}% used. Go delete some unused backups to make space."
            print(msg)