import sys
import envs
import time
import asyncio
import threading
import subprocess
import output_controller

#store the server binary location with args
SERVER_CMD = sys.argv[1:]

#check the amount of players every few seconds and clear the online list
def check_players(proc):
    while True:
        time.sleep(envs.PLAYER_CHECK_FREQ)
        proc.stdin.write("playing\n")
        proc.stdin.flush()
        envs.ONLINE = []

#func to read the user's input
def read_input(proc):
    for line in sys.stdin:
        proc.stdin.write(line)
        proc.stdin.flush()

#func to read the user's output
def read_output(proc):
    for raw in proc.stdout:
        #clean up the line
        line = raw.rstrip("\n")

        #control what happens based on the output
        output_controller.control_output(line, proc)


async def start_server():
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
    threading.Thread(target=check_players, args=(proc,), daemon=True).start()

    code = proc.wait()

    #restart the server if it crash
    if code != 0:
        envs.RESTART = True


#run the server forever unless told not to
while True:
    asyncio.run(start_server())

    if not envs.RESTART:
        break