# Terraria Vanilla Tools 

This a Terraria vanilla server wrapper where it can add additional tools to help moderate your vanilla server. Note that this can only perform actions that a human can do from the server's console. It can't do extreme things like sever side characters ([Tshock](https://github.com/Pryaxis/TShock) is still needed for that). However what this can do is add in better logs and / commands that can be executed from the game, with the right permission (Yes, that makes this a *"little bit"* janky). 

## Features
- Saves the server's console as 3 separate log files.
	- `chat.log`: logs the chat messages with timestamps.
	- `player.log`: logs the players who joined the world.
	- `other.log`: logs the other info from the server's console with timestamps.
- Multiple [/ commands](#Commands) that can be executed from within game (See step 8 of [the setup](#Setup) in order to limit the commands to only approved IPs)
- Ban griefers who are offline. 
- auto backup the world every 15 mins
- easy way to manually backup and restore the world 
- Auto restart server if wasn't properly exited
## Dependencies
- A Linux server (this has been only tested on Linux. Windows and Mac might work, but your mileage may vary)
- Python 3.12.3+ (earlier versions may work, but your mileage may vary)	￼-
- the `unzip` package
## Setup
1. Clone the repo via `git clone https://github.com/bossmania/Vanilla-Terraria-Tools`
2. Run the `setup.sh` file to setup the folder structure 
	- Modify the folder paths in the script beforehand if you want to change the defaults. 
	- DON'T modify the path to the `paths.txt` file, or else the script won't work.
3. Run the `download_server.sh` with the server version you want (without periods)
	- EX: `./download_server.sh 1450` to automatically download the server on version 1.4.5.0. 
4. Run `./start_server.sh` with the server version
	- EX: `./start_server.sh 1450` to start the server on version 1.4.5.0.
5. Create the world that you want.
6. Stop the server via either typing in `exit`, or pressing `CTRL + C`.
7. modify the config file for the server at `~/admin/config.txt`. Use the following as a template on what to add: *Replace <USERNAME> with your linux's username, and <WORLD_NAME> with the name of the actual world*
```toml
world=/home/<USERNAME>/worlds/<WORLD_NAME>.wld
maxplayers=16
port=7777
password=
motd="Welcome to this server!"
language=en-US
secure=0
banlist=~/admin/banlist.txt
```
8. modify the `~/admin/ApprovedIPs.txt` file to be a list of IPs (separated by new line) for the people who are allowed to use the / commands. The following is an example of what it should look like.
  ```
  127.0.0.1
  192.168.1.1
  10.0.0.1
  ```
9. start the server again (`./start_server.sh`) and it should automatically use the config file to auto load the world.

## Commands
- `/kick <USERNAME>`: kicks a player from the server.
- `/ban <USERNAME>`: ban a player from the server (can ban offline people).
- `/save`: save the world at the current's state.
- `/backup`: backup the world right now.
- `/restore (/rollback)`: shows the last 8 backups.
- `/restore (/rollback) <NUMBER>`: restore the world to the backup corresponding with the number.
- `/exit`: exits (and saves) the server.
- `/settle`: settles all of the liquids in the world.
- `/admin:` shows this help message.

### Other bash files
There are the `ban_player.sh` and the `world_backup.sh` bash files that wasn't mention so far. They can be used to ban (offline) players, via `./ban_player <USERNAME>`, and the `./world_backup.sh` to manually backup the world.

## AI disclaimer
For the stakes of transparency, I have used ChatGPT to generate me the basic skeleton of the script, and to generate me the regex syntax. Everything else was written by me.
