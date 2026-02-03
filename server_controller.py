import re
import sys
import time
import logger
import pathlib
import threading
import subprocess
import offline_ban
from os import path
import handle_commands

#store the banlist and server binary location with args
BANLIST = path.join(path.join(pathlib.Path.home(), "banlist.txt"))
SERVER_CMD = sys.argv[1:]

#regex filters (ChatGPT wrote them cause I'll never understand regex)
# Match anything with <...> or : <...> in it
chat_regex = re.compile(r'^:?\s*<[^<>]+>')
#match anything with a (IP:Port)
IP_regex = re.compile(r'\(\b\d{1,3}(?:\.\d{1,3}){3}:\d{1,5}\b\)')

#check the amount of players every 7 seconds
def check_players(proc):
    while True:
        time.sleep(7)
        proc.stdin.write("playing\n")
        proc.stdin.flush()

#command handler
def command_checker(line, proc):
    #handle /kick command
    if "/kick" in line:
        handle_commands.kick(line, proc)
    
    #handle /ban command
    if "/ban" in line:
        handle_commands.ban(line, proc, BANLIST)

    #handle /save command
    if "/save" in line:
        handle_commands.save(proc)
        
    #handle /exit command    
    if "/exit" in line:
        handle_commands.exit(proc)
        
    #handle /settle command    
    if "/settle" in line:
        handle_commands.settle(proc)


def read_output(proc):
    #get stdout
    for raw in proc.stdout:
        #clean up the line
        line = raw.rstrip("\n")

        #check if the line was a command, and execute on it
        command_checker(line, proc)

        #timestamp the stdout line
        stamped = logger.timestamp(line)

        # print to console
        print(stamped)

        #check if the line matches a regex filter for the log file to store at
        if chat_regex.search(line):
            logger.write_log(stamped, logger.CHAT_LOG)
        elif IP_regex.search(line):
            logger.write_player(line)
        else:
            logger.write_log(stamped, logger.OTHER_LOG)


#read the keyboard input and send it
def read_input(proc):
    for line in sys.stdin:
        proc.stdin.write(line)
        proc.stdin.flush()


def main():
    #start the server
    proc = subprocess.Popen(
        SERVER_CMD,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    #start controlling the stdin and stdout of the server
    threading.Thread(target=read_output, args=(proc,), daemon=True).start()
    threading.Thread(target=read_input, args=(proc,), daemon=True).start()
    threading.Thread(target=check_players, args=(proc,), daemon=True).start()

    #wait for the server to stop before stopping the script
    proc.wait()


if __name__ == "__main__":
    main()
