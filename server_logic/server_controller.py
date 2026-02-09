import os
import sys
import envs
import time
import logger
import threading
import subprocess
import discord_bot
import handle_commands
import world_controller
from dotenv import load_dotenv

#store the server binary location with args
SERVER_CMD = sys.argv[1:]

#check the amount of players every 7 seconds
def check_players(proc):
    while True:
        time.sleep(7)
        proc.stdin.write("playing\n")
        proc.stdin.flush()

#func to auto backup the world every 15 mins 
def auto_backup_world():
    while True:
        time.sleep(envs.BACKUP_TIMER)
        world_controller.backup_world()

#command handler
def command_checker(line, proc):
    #check if the player has permission to run commands
    if handle_commands.check_if_allowed(envs.PLAYER_LOG, line):
        #handle /kick command
        if "/kick" in line:
            handle_commands.kick(line, proc)

        #handle /ban command
        if "/ban" in line:
            handle_commands.ban(line, proc)

        #handle /backup command
        if "/backup" in line:
            handle_commands.backup(proc)

        #handle /restore (or /rollback) command
        if "/restore" in line or "/rollback" in line:
            handle_commands.restore(line, proc)

        #handle /save command
        if "/save" in line:
            handle_commands.save(proc)

        #handle /exit command    
        if "/exit" in line:
            handle_commands.exit(proc)

        #handle /settle command    
        if "/settle" in line:
            handle_commands.settle(proc)

        if "/admin" in line:
            handle_commands.help(proc)

def read_output(proc):
    #get stdout
    for raw in proc.stdout:
        #clean up the line
        line = raw.rstrip("\n")
        #timestamp the stdout line
        stamped = logger.timestamp(line)

        # print to console
        print(stamped)

        #check if the line matches a regex filter for the log file to store at
        if envs.chat_regex.search(line):
            logger.write_log(stamped, envs.CHAT_LOG)
            
            #check if the line was a command, and execute on it
            command_checker(line, proc)
        elif envs.IP_regex.search(line):
            logger.write_player(line)
        else:
            logger.write_log(stamped, envs.OTHER_LOG)


#read the keyboard input and send it
def read_input(proc):
    for line in sys.stdin:
        proc.stdin.write(line)
        proc.stdin.flush()

#only use the discord bot when there is a token provided
def use_discord_bot(proc):
    #get the token from the .env file
    load_dotenv()
    TOKEN = os.getenv("TOKEN")

    #if there is a token, then use the discord bot
    if (len(TOKEN) > 0):
        discord_bot.start_bot(TOKEN, proc)

def main():
    envs.update_paths()

    #always restart the server unless told not to
    while True:
        envs.RESTARTING = False

        #start the server
        proc = subprocess.Popen(
            SERVER_CMD,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        #start controlling the server
        threading.Thread(target=read_output, args=(proc,), daemon=True).start()
        threading.Thread(target=read_input, args=(proc,), daemon=True).start()
        threading.Thread(target=check_players, args=(proc,), daemon=True).start()
        threading.Thread(target=auto_backup_world, daemon=True).start()
        threading.Thread(target=use_discord_bot, args=(proc,),daemon=True).start()

        #wait for the server to stop before stopping the script
        code = proc.wait()

        #don't restart the sever if it sucessfully ended and it isn't set to restart
        if code == 0 and envs.RESTARTING == False:
            break


if __name__ == "__main__":
    main()
