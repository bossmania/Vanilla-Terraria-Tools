#!/usr/bin/env bash

#make it fail on error
set -eu 

#wrapper for baning the player with specific paths
python3 server_logic/offline_ban.py ~/logs/player.log ~/admin/banlist.txt $1