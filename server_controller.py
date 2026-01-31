import subprocess
import sys
import threading
from datetime import datetime
import pathlib
from os import path
import re

#store the log and server binary location
LOG_FOLDER = f"{pathlib.Path.home()}/logs/"
SERVER_CMD = [f"{pathlib.Path.home()}/server_versions/1453/TerrariaServer.bin.x86_64"]  # change if needed

#add the timestamp to the line
def timestamp(line):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"[{timestamp}] {line}"

#write to the chat file
def write_chat(line):
    with open(path.join(LOG_FOLDER, "chat.log"), "a", buffering=1) as logfile:
        logfile.write(line  + "\n")
        logfile.flush()

#write to the other file
def write_other(line):
    with open(path.join(LOG_FOLDER, "other.log"), "a", buffering=1) as logfile:
        logfile.write(line  + "\n")
        logfile.flush()

#placeholder automation logic
def handle_line(line, proc):
    """
    Put your automation logic here
    """
    if "joined" in line:
        proc.stdin.write("say Welcome!\n")
        proc.stdin.flush()


def read_output(proc):
    #get stdout
    for raw in proc.stdout:
        #clean up the line
        line = raw.rstrip("\n")

        #timestamp the stdout line
        stamped = timestamp(line)

        # print to console
        print(stamped)

        # Match anything with <...> in it
        chat_regex = re.compile(r'^<[^<>]+>')

        #check to save the line to chat or other log
        if chat_regex.search(line):
            write_chat(stamped)
        else:
            write_other(stamped)


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

    #wait for the server to stop before stopping the script
    proc.wait()


if __name__ == "__main__":
    main()
