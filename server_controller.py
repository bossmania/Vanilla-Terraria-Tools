import subprocess
import sys
import threading
from datetime import datetime
import pathlib
from os import path
import re
import time

#store the log and server binary location
LOG_FOLDER = f"{pathlib.Path.home()}/logs/"
SERVER_CMD = [f"{pathlib.Path.home()}/server_versions/1453/TerrariaServer.bin.x86_64"]  # change if needed

#regex filters
# Match anything with <...> in it
chat_regex = re.compile(r'^<[^<>]+>')
#match anything with a (IP:Port)
IP_regex = re.compile(r'\(\b\d{1,3}(?:\.\d{1,3}){3}:\d{1,5}\b\)')

#add the timestamp to the line
def timestamp(line):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"[{timestamp}] {line}"

#write to the a log file file
def write_log(line, log):
    with open(path.join(LOG_FOLDER, log), "a", buffering=1) as logfile:
        logfile.write(line  + "\n")
        logfile.flush()

#check the amount of players every 7 seconds
def check_players(proc):
    while True:
        time.sleep(7)
        proc.stdin.write("playing\n")
        proc.stdin.flush()

# #placeholder automation logic
# def handle_line(line, proc):
#     """
#     Put your automation logic here
#     """
#     if "joined" in line:
#         proc.stdin.write("say Welcome!\n")
#         proc.stdin.flush()

def read_output(proc):
    #get stdout
    for raw in proc.stdout:
        #clean up the line
        line = raw.rstrip("\n")

        #timestamp the stdout line
        stamped = timestamp(line)

        # print to console
        print(stamped)

        #check if the line matches a regex filter for the log file to store at
        if chat_regex.search(line):
            write_log(stamped, "chat.log")
        elif IP_regex.search(line):
            write_log(line, "player.log")
        else:
            write_log(stamped, "other.log")


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
