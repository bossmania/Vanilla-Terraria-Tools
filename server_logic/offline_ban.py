import re
import os
import sys
import envs

#prepare to get the IPs
IPs = []

#func to check if the player has even joined the server before
def check_if_ever_joined(player_file, banned_player):
    found = False

    #open the player list and get all of the players
    with open(player_file, "r", buffering=1) as player_log:
        players = player_log.read().splitlines()

        for player in players:
            #get the username & IP for that player
            results = envs.User_IP_log_regex.search(player)
            if not results:
                raise Exception("The player file is not formatted properly!")
            
            #stop when founed the player in the list
            user, IP = results.groups()
            if user == banned_player:
                found = True
                return True
    
    #inform that the player can't be found
    if not found:
        return False

def get_ips(player_file, banned_player):
    #open the player list and get all of the players
    with open(player_file, "r", buffering=1) as player_log:
        players = player_log.read().splitlines()

        for player in players:
            #get the username & IP for that player
            results = envs.User_IP_log_regex.search(player)
            if not results:
                raise Exception("The player file is not formatted properly!")
            
            #save the IP if the current user is the bad guy
            user, IP = results.groups()
            if user == banned_player:
                IPs.append(IP)
    
def remove_banned_IPs(ban_file, banned_player):
    #open the ban filistle if it exists
    if os.path.isfile(ban_file):
        with open(ban_file, "r", buffering=1) as ban_log:
            #read all of the lines in there
            lines = ban_log.read().splitlines()

            #if a IP is already in the ban list, then remove it from the list
            for line in lines:
                for IP in IPs:
                    if line == IP:
                        IPs.remove(IP)

def update_ban_list(ban_file, banned_player):
    #open the ban list
    with open(ban_file, "a", buffering=1) as ban_log:
        #format the ban text for every IP
        for IP in IPs:
            output = (
                f"//{banned_player}\n"
                f"{IP}\n"
            )

            #write the ban list
            ban_log.write(output + "\n")
            ban_log.flush()
    
    #return the banning response
    if len(IPs) > 0:
        return f"Sucessfully banned {banned_player}!"
    else:
        return f"{banned_player} is already banned from the server!"

#func to easily ban someone
def ban_player(player_file, ban_file, banned_player):
    response = ""

    #checked if the player has joined the server before
    joined = check_if_ever_joined(player_file, banned_player)
    if not joined:
        response = f"{banned_player} has never joined the server before!"
    else:
        #ban the player
        get_ips(player_file, banned_player)
        remove_banned_IPs(ban_file, banned_player)
        response = update_ban_list(ban_file, banned_player)

    #show and return the response
    print(response)
    return response

def main():
    #get the arguments
    player_file = sys.argv[1]
    ban_file = sys.argv[2]
    banned_player = sys.argv[3]

    ban_player(player_file, ban_file, banned_player)

if __name__ == "__main__":
    main()