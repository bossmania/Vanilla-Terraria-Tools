import re
import sys
import os

#prepare to get the IPs (regex by ChatGPT)
user_IP_regex = re.compile(r'^(.+?)\s*\[(\d{1,3}(?:\.\d{1,3}){3})\]$')
IPs = []

def get_ips(player_file, banned_player):
    #open the player list and get all of the players
    with open(player_file, "r", buffering=1) as player_log:
        players = player_log.read().splitlines()

        for player in players:
            #get the username & IP for that player
            results = user_IP_regex.search(player)
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
    
    #infrom about the banning
    if len(IPs) > 0:
        print(f"Sucessfully banned {banned_player}!")
    else:
        print(f"{banned_player} is already banned from the server!")

#func to easily ban someone
def ban_player(player_file, ban_file, banned_player):
    get_ips(player_file, banned_player)
    remove_banned_IPs(ban_file, banned_player)
    update_ban_list(ban_file, banned_player)

if __name__ == "__main__":
    #get the arguments
    player_file = sys.argv[1]
    ban_file = sys.argv[2]
    banned_player = sys.argv[3]

    #ban the player
    ban_player(player_file, ban_file, banned_player)