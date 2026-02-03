#!/usr/bin/env bash

#make it fail on error
set -eu 

# wrapper for starting the server on provided version
python3 server_controller.py ~/server_versions/$1/TerrariaServer.bin.x86_64 -disableannouncementbox -banlist ~/banlist.txt