import sys
import envs
import asyncio
import threading
import subprocess
import background_tasks

#store the server binary location with args
SERVER_CMD = sys.argv[1:]

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
    threading.Thread(target=background_tasks.read_output, args=(proc,), daemon=True).start()
    threading.Thread(target=background_tasks.read_input, args=(proc,), daemon=True).start()
    threading.Thread(target=background_tasks.check_players, args=(proc,), daemon=True).start()
    threading.Thread(target=background_tasks.auto_backup_world, daemon=True).start()
    threading.Thread(target=background_tasks.check_storage, daemon=True).start()

    code = proc.wait()

    #restart the server if it crash
    if code != 0:
        envs.RESTART = True


#run the server forever unless told not to
while True:
    asyncio.run(start_server())

    if not envs.RESTART:
        break