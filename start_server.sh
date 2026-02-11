#!/usr/bin/env bash

#make it fail on error
set -eu 

# put the user in the venv if they're not already
source venv/bin/activate

# wrapper for starting the server on provided version
python3 server_logic/server_controller.py ~/server_versions/$1/TerrariaServer.bin.x86_64 -disableannouncementbox -banlist ~/admin/banlist.txt -config ~/admin/config.txt
