import subprocess
import sys
import threading
from datetime import datetime
import pathlib

#store the log and server binary location
LOG_FILE = f"{pathlib.Path.home()}/logs/server.log"
SERVER_CMD = [f"{pathlib.Path.home()}/server_versions/1453/TerrariaServer.bin.x86_64"]  # change if needed

#get the timestamp
def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


#placeholder automation logic
def handle_line(line, proc):
    """
    Put your automation logic here
    """
    if "joined" in line:
        proc.stdin.write("say Welcome!\n")
        proc.stdin.flush()


def read_output(proc, logfile):
    #get stdout
    for raw in proc.stdout:
        line = raw.rstrip("\n")

        #timestamp the stdout line
        stamped = f"[{timestamp()}] {line}"

        # print to console
        print(stamped)

        # write to log
        logfile.write(stamped + "\n")
        logfile.flush()

        handle_line(line, proc)


#read the keyboard input and send it
def read_input(proc):
    for line in sys.stdin:
        proc.stdin.write(line)
        proc.stdin.flush()


def main():
    #open the log file
    with open(LOG_FILE, "a", buffering=1) as logfile:
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
        threading.Thread(target=read_output, args=(proc, logfile), daemon=True).start()
        threading.Thread(target=read_input, args=(proc,), daemon=True).start()

        #wait for the server to stop before stopping the script
        proc.wait()


if __name__ == "__main__":
    main()
