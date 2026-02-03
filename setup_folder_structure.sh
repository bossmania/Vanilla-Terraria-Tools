#!/usr/bin/env bash

#basic script that will create all of the needed folders
cd ~
mkdir worlds_backup tools config
mkdir -p ~/.local/share/Terraria/Worlds/
ln -s ~/.local/share/Terraria/Worlds/ worlds