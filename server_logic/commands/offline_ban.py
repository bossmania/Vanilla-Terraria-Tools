import re
import os
import sys
import envs

#func to check if the player has even joined the server before
def check_if_ever_joined(banned_player):
    #get all of the players
    envs.PLAYER_LOG.seek(0)
    players = envs.PLAYER_LOG.read().splitlines()

    for player in players:
        #get the username & IP for that player
        results = envs.User_IP_log_regex.search(player)
        if not results:
            raise Exception("The player file is not formatted properly!")
        
        #stop when founed the player in the list
        user, IP = results.groups()
        if user.lower() == banned_player.lower():
            return True
    
    #inform that the player can't be found
    return False

def get_ips(banned_player, IPs):
    #get all of the players
    envs.PLAYER_LOG.seek(0)
    players = envs.PLAYER_LOG.read().splitlines()

    for player in players:
        #get the username & IP for that player
        results = envs.User_IP_log_regex.search(player)
        if not results:
            raise Exception("The player file is not formatted properly!")
        
        #save the IP if the current user is the bad guy
        user, IP = results.groups()
        if user.lower() == banned_player.lower():
            IPs.append(IP)

    return IPs
    
def clean_IP_list(IPs):
    #read all of the lines in there
    envs.BANLIST.seek(0)
    lines = envs.BANLIST.read().splitlines()

    #if a IP is already in the ban list, then remove it from the list
    for line in lines:
        for IP in IPs:
            if line == IP:
                IPs.remove(IP)

    #removed duplicated IPs from the list
    IPs = (set(IPs))

    return IPs

def update_ban_list(banned_player, IPs):
    #format the ban text for every IP
    for IP in IPs:
        output = (
            f"//{banned_player}\n"
            f"{IP}\n"
        )

        #write the ban list
        envs.BANLIST.write(output + "\n")
    
    #return the banning response
    if len(IPs) > 0:
        return f"Sucessfully banned {banned_player} from the server!"
    else:
        return f"{banned_player} is already banned from the server!"

#func to easily ban someone
def ban_player(banned_player):
    response = ""

    #checked if the player has joined the server before
    joined = check_if_ever_joined(banned_player)
    if not joined:
        response = f"{banned_player} has never joined the server before!"
    else:        
        #get the ip list
        IPs = []
        IPs = get_ips(banned_player, IPs)
        IPs = clean_IP_list(IPs)
        
        #ban the player
        response = update_ban_list(banned_player, IPs)

    #return the response
    return response

def main():
    #get the arguments
    player_file = sys.argv[1]
    ban_file = sys.argv[2]
    banned_player = sys.argv[3]

    ban_player(player_file, ban_file, banned_player)

if __name__ == "__main__":
    main()