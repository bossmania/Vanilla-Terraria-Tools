#!/usr/bin/env bash

#basic script that will create all of the needed folders and files
cd ~
mkdir worlds_backup tools config admin
mkdir -p ~/.local/share/Terraria/Worlds/
ln -s ~/.local/share/Terraria/Worlds/ worlds
touch ~/admin/{banlist.txt,ApprovedIPs.txt}