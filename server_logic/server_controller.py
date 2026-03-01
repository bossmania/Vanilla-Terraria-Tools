import sys
import threading
import subprocess

#func to read the user's input
def read_input(proc):
    for line in sys.stdin:
        proc.stdin.write(line)
        proc.stdin.flush()

#func to read the user's output
def read_output(proc):
    for raw in proc.stdout:
        line = raw.strip("\n")
        print(line)

#store the server binary location with args
SERVER_CMD = sys.argv[1:]

#create the server's process
proc = subprocess.Popen(
    SERVER_CMD,
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1
)

#read the server's input and output 
threading.Thread(target=read_output, args=(proc,), daemon=True).start()
threading.Thread(target=read_input, args=(proc,), daemon=True).start()

code = proc.wait()