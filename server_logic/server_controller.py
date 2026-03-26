import sys
import envs
import time
import logger
import signal
import asyncio
import threading
import subprocess
import background_tasks
from functools import partial
from commands import server_commands
from discord_bot import discord_bot_notify

#store the server binary location with args
SERVER_CMD = sys.argv[1:]

def graceful_shutdown(proc, signum, frame):
    #say that it got the signal
    logger.write_log(logger.timestamp(f"Received a signal of {signum}, shutting down the server now!"))
    
    #save and exit the world
    server_commands.exit(proc)
    
def start_server():
    #reset the values
    envs.RESTART = False
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

    #start the server's background tasks
    threading.Thread(target=background_tasks.read_output, args=(proc,), daemon=True).start()
    threading.Thread(target=background_tasks.read_input, args=(proc,), daemon=True).start()
    threading.Thread(target=background_tasks.check_players, args=(proc,), daemon=True).start()
    threading.Thread(target=background_tasks.auto_backup_world, daemon=True).start()
    threading.Thread(target=background_tasks.check_storage, daemon=True).start()
    threading.Thread(target=background_tasks.flush_logs_timer, daemon=True).start()
    threading.Thread(target=background_tasks.start_bot, args=(proc,), daemon=True).start()
    threading.Thread(target=background_tasks.get_player_count, daemon=True).start()

    # create a pertial function with the proc for the SIGTERM signal handler
    graceful_shutdown_proc = partial(graceful_shutdown, proc)
    signal.signal(signal.SIGTERM, graceful_shutdown_proc)

    #wait for the process to finish and get the exit code
    code = proc.wait()

    #restart the server if it crash
    if code != 0:
        envs.RESTART = True

    #notify of a server restart on discord, if using it
    if envs.RESTART and len(envs.TOKEN) > 0:
        asyncio.run_coroutine_threadsafe(discord_bot_notify.notify("Restarting the server!"), envs.BOT.bot.loop)

    #stop the discord bot, if running one
    if len(envs.TOKEN) > 0:
        envs.BOT.stop_bot()

    #stop the threads
    envs.STOP_THREADS = True

    #wait for all of the threads to stop
    print (logger.timestamp("Stoppping the server and all of the background tasks. Please wait a moment!"))
    while len(envs.RUNNING_THREADS) > 0:
        time.sleep(0.1)

#run the server forever unless told not to
while True:
    start_server()

    #stop the server when not restarting it
    if not envs.RESTART:
        #close all of the open files
        envs.PLAYER_LOG.close()
        envs.CHAT_LOG.close()
        envs.OTHER_LOG.close()
        envs.BANLIST.close()
        envs.APPROVED_IP.close()
        break