#!/usr/bin/env bash

#make it fail on error
set -eu 


#store the paths
ROOT="/home/terraria"
WORLDS="${ROOT}/worlds"
BACKUP="${ROOT}/worlds_backup"

#get the timestamp and use it as the backup name
TIMESTAMP="$(date +"%Y-%m-%d__%H_%M_%S")"
COPY="${BACKUP}/${TIMESTAMP}"

#copy and paste the world folder to the backup
cp -rL "$WORLDS" "$COPY"

#inform that it was made 
echo "Sucessfully made a backup @ ${TIMESTAMP}"
