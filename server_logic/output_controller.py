import envs
import logger
import server_commands

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

def check_user_permission(line):
    #get the user and prep the IP search
    results = envs.user_regex.search(line)

    if not results:
        return

    talked_user = results.group()
    IPs = []
    
    #open the player list and get all of the players
    with open(envs.PLAYER_LOG, "r", buffering=1) as player_log:
        players = player_log.read().splitlines()

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
    with open(envs.APPROVED_IP_FILE, "r", buffering=1) as IP_log:
        approved_IPs = IP_log.read().splitlines()

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

        #handle /kick command
        if "/kick" in line:
            server_commands.kick(line, proc)