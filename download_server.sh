#!/usr/bin/env bash

#make it fail on error
set -eu 

#download the sever zip file
cd ~/server_versions
wget "https://terraria.org/api/download/pc-dedicated-server/terraria-server-${1}.zip"
unzip "terraria-server-${1}.zip"
rm "terraria-server-${1}.zip"

#prepare the server binary
cd $1
rm -r Mac Windows
mv Linux/* .
rmdir Linux
chmod +x TerrariaServer TerrariaServer.bin.x86_64

#say it's done
echo "Sucessfully installed and setup ${1}"
