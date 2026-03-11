import sys
import envs
import time
import threading
import subprocess
import background_tasks

#store the server binary location with args
SERVER_CMD = sys.argv[1:]

def start_server():
    #reset the values for stopping threads
    envs.STOP_THREADS = False
    envs.RUNNING_THREADS = []

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
    threading.Thread(target=background_tasks.read_output, args=(proc,), daemon=True).start()
    threading.Thread(target=background_tasks.read_input, args=(proc,), daemon=True).start()
    threading.Thread(target=background_tasks.check_players, args=(proc,), daemon=True).start()
    threading.Thread(target=background_tasks.auto_backup_world, daemon=True).start()
    threading.Thread(target=background_tasks.check_storage, daemon=True).start()

    #wait for the process to finish and get the exit code
    code = proc.wait()

    #restart the server if it crash
    if code != 0:
        envs.RESTART = True

    #stop the threads
    envs.STOP_THREADS = True
    
    #wait for all of the threads to stop
    while len(envs.RUNNING_THREADS) > 0:
        time.sleep(0.1)

#run the server forever unless told not to
while True:
    start_server()

    if not envs.RESTART:
        break