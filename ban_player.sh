#!/usr/bin/env bash

#make it fail on error
set -eu 

#wrapper for baning the player with specific paths
python3 offline_ban.py ~/logs/player.log ~/banlist.txt $1