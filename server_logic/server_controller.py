import sys
import envs
import time
import logger
import asyncio
import threading
import subprocess
import discord_bot
import handle_commands
import world_controller
from datetime import datetime

#store the server binary location with args
SERVER_CMD = sys.argv[1:]

#store the last time the status has been updated
LAST_UPDATE_STATUS = datetime.now()
PLAYER_CHECK_FREQ = 7
USE_DISCORD = False

#check the amount of players every 7 seconds
def check_players(proc):
    while True:
        time.sleep(PLAYER_CHECK_FREQ)
        proc.stdin.write("playing\n")
        proc.stdin.flush()

def get_player_count(line):
    #get the duration of when the last time the status has been updated
    global LAST_UPDATE_STATUS
    duration = (datetime.now() - LAST_UPDATE_STATUS).total_seconds()
    
    #prep the player check
    player_count = None
    
    #check how many players are online
    if "player connected." in line:
        player_count = int(envs.number_regex.search(line).group())
    elif "No players connected." in line:
        player_count = 0

    #check if it sucessfully got the player count, and enough time has passed
    if player_count != None and duration > PLAYER_CHECK_FREQ:
        #update the player count adn reset the update status timer
        asyncio.run_coroutine_threadsafe(discord_bot.player_count(player_count), discord_bot.bot.loop)
        LAST_UPDATE_STATUS = datetime.now()

#func to auto backup the world
def auto_backup_world(proc):
    while True:
        #wait for the sleep to end
        time.sleep(envs.BACKUP_TIMER)

        #backup and show the time to the console
        timestamp = world_controller.backup_world()
        timestamp = world_controller.timestamp_cleaner(timestamp)
        handle_commands.say(f"Just saved the world at {timestamp}!", proc)

#only use the discord bot when there is a token provided
def use_discord_bot(proc):
    global USE_DISCORD
    
    #if there is a token, then use the discord bot
    if (len(envs.TOKEN) > 0):
        USE_DISCORD = True
        discord_bot.start_bot(proc)

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

        #handle /exit-nosave command    
        if "/exit-nosave" in line:
            handle_commands.exit_nosave(proc)

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

        #notify on discord that the server is up if it's using discord
        if USE_DISCORD and "Server started" in line:
            asyncio.run_coroutine_threadsafe(discord_bot.notify("The server has booted up!"), discord_bot.bot.loop)

        #check if the line matches a regex filter for the log file to store at
        if envs.chat_regex.search(line):
            #log the chat message
            logger.write_log(stamped, envs.CHAT_LOG)

            #send the chat message to discord if using it
            if USE_DISCORD:
                asyncio.run_coroutine_threadsafe(discord_bot.chat_log(line), discord_bot.bot.loop)
            
            #check if the line was a command, and execute on it
            command_checker(line, proc)
        elif envs.IP_regex.search(line):
            logger.write_player(line)
        else:
            logger.write_log(stamped, envs.OTHER_LOG)

        #attempt to get the player count for discord if using it
        if USE_DISCORD:
            get_player_count(line)


#read the keyboard input and send it
def read_input(proc):
    for line in sys.stdin:
        proc.stdin.write(line)
        proc.stdin.flush()

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
        threading.Thread(target=auto_backup_world, args=(proc,), daemon=True).start()
        threading.Thread(target=use_discord_bot, args=(proc,), daemon=True).start()

        #wait for the server to stop before stopping the script
        code = proc.wait()

        #notify on discord that the server is restarting
        if envs.RESTARTING == True and USE_DISCORD:
            asyncio.run_coroutine_threadsafe(discord_bot.notify("Restarting the server!"), discord_bot.bot.loop)

        #don't restart the sever if it sucessfully ended and it isn't set to restart
        if code == 0 and envs.RESTARTING == False:
            #notify on discord if using it
            if USE_DISCORD:
                asyncio.run_coroutine_threadsafe(discord_bot.notify("Shutting down the server!"), discord_bot.bot.loop)        
                
                #give it time to send the msg before killing the loop
                time.sleep(5)
                
            break


if __name__ == "__main__":
    main()
