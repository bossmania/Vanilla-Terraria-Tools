#!/usr/bin/env bash

#create all of the needed folders and files
cd ~
mkdir worlds_backup logs config admin server_versions
mkdir -p ~/.local/share/Terraria/Worlds
ln -sfn ~/.local/share/Terraria/Worlds ~/worlds
touch ~/admin/{banlist.txt,approved_ips.txt,config.txt}

#generate the config template to use
cat > ~/admin/config.txt <<EOF
world=/home/[USERNAME]/worlds/[WORLD_NAME].wld
maxplayers=16
port=7777
password=
motd="Welcome to this server!"
language=en-US
secure=0
banlist=~/admin/banlist.txt
EOF