#!/usr/bin/env bash

#basic script that will create all of the needed folders and files
cd ~
mkdir worlds_backup tools config admin
mkdir -p ~/.local/share/Terraria/Worlds/
ln -s ~/.local/share/Terraria/Worlds/ worlds
touch ~/admin/{banlist.txt,ApprovedIPs.txt}
touch ~/paths.txt

#auto create a folder that will store all of the paths for the server to function properly
cat <<EOF > "~/paths.txt"
chat_logs=~/logs/chat.log
player_logs=~/logs/player.log
other_logs=~/logs/other.log
banlist=~/admin/banlist.txt
approved_IPs=~/admin/ApprovedIPs.txt
world_save=~/.local/share/Terraria/Worlds
world_backup=~/world_backups
EOF