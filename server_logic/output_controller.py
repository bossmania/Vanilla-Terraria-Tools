import envs
import logger
from commands import server_commands

def control_output(line, proc):
    #timestamp the stdout line and print it
    stamped = logger.timestamp(line)
    print(stamped)

    #organize the messages for logging
    organize_log_messages(line, stamped, proc)

    #check if the output was a command
    command_checker(line, proc)

    #get the list of online players
    get_online_players(line)

    #check if the world is currently saving
    check_if_saving(line)

def organize_log_messages(line, stamped, proc):
    #log the player's IP
    if envs.IP_regex.search(line):
        logger.write_player(line)

    #log the chat message
    elif envs.chat_regex.search(line):
        #log the chat message
        logger.write_log(stamped, envs.CHAT_LOG)

    #log everything else
    else:
        logger.write_log(stamped, envs.OTHER_LOG)

def get_online_players(line):
    #filter the line and check if it's valid 
    result = envs.user_IP_regex.search(line)
    if not result:
        return None

    #get the username
    username, _ = result.groups()

    #add the username to the online list
    envs.ONLINE.append(username)

#func to check if the world is currently saving
def check_if_saving(line):
    if "Saving world data:" in line:
        envs.CURRENTLY_SAVING = True
    elif "Backing up world file" in line:
        envs.CURRENTLY_SAVING = False

def check_user_permission(line):
    #get the user and prep the IP search
    results = envs.user_regex.search(line)

    #get the user if it's valid
    if not results:
        return
    talked_user = results.group()
    
    IPs = []

    #get the list of players
    envs.PLAYER_LOG.seek(0)
    players = envs.PLAYER_LOG.read().splitlines()

    for player in players:
        #get the username & IP for that player
        results = envs.User_IP_log_regex.search(player)
        if not results:
            raise Exception("The player file is not formatted properly!")
        
        #save the IP if the current user is the talked user
        user, IP = results.groups()
        if user == talked_user:
            IPs.append(IP)

    #get all of the approved IPs
    envs.APPROVED_IP.seek(0)
    approved_IPs = envs.APPROVED_IP.read().splitlines()

    #go through each approved IP, and the IPs match by the chatter
    for approved_IP in approved_IPs:
        for IP in IPs:
            #stop if the IP is in the approved list
            if IP == approved_IP:
                return True

    #if the IP wasn't found in the list, then return false    
    return False

def command_checker(line, proc):
    #check if the player has permission to run commands
    if check_user_permission(line):
        #lowercase the command line for auto caps
        line = line.lower()

        #/kick command
        if "/kick" in line:
            server_commands.kick(line, proc)
        
        #/ban command
        if "/ban" in line:
            server_commands.ban(line, proc)

        #/backup command
        if "/backup" in line:
            server_commands.backup(proc)

        #/restore (or /rollback) command
        if "/restore" in line or "/rollback" in line:
            server_commands.restore(line, proc)

        #/save command
        if "/save" in line:
            server_commands.save(proc)

        #/exit-nosave command    
        if "/exit-nosave" in line:
            server_commands.exit_nosave(proc)

        #/exit command    
        if "/exit" in line:
            server_commands.exit(proc)

        #/settle command    
        if "/settle" in line:
            server_commands.settle(proc)

        #/admin command
        if "/admin" in line:
            server_commands.help(proc)