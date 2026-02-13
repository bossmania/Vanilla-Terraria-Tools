# Terraria Vanilla Tools 

This a Terraria vanilla server wrapper where it can add additional tools to help moderate your vanilla server. Note that this can only perform actions that a human can do from the server's console. It can't do extreme things like sever side characters ([Tshock](https://github.com/Pryaxis/TShock) is still needed for that). However what this can do is add in better logs and / commands that can be executed from the game, with the right permission (Yes, that makes this a *"little bit"* janky).

## Features
- Saves the server's console as 3 separate log files.
	- `chat.log`: logs the chat messages with timestamps.
	- `player.log`: logs the players who joined the world.
	- `other.log`: logs the other info from the server's console with timestamps.
- Multiple [/ commands](#Commands) that can be executed from within game (See step 8 of [the setup](#Setup) in order to limit the commands to only approved IPs)
- Ban griefers who are offline. 
- auto backup the world every 15 mins (configurable).
- easy way to manually backup and restore the world .
- Auto restart server if wasn't properly exited.
- Monitor and control the server from a optional discord bot.
	- *Almost* the [same commands set](#Discord_commands) as in game. 
	- *Almost* live player count as the bot's status.
	- Monitor the server's chat log in a dedicated channel.
	- Notify when the server started, stopped, and restarted.
	
## Dependencies
- A Linux server (this has been only tested on Linux. Windows and Mac might work, but your mileage may vary).
- The `unzip` package.
- Python 3.12.3+ and python3.12-venv (earlier versions may work, but your mileage may vary).

## Setup
1. Download the [latest's zip file](https://github.com/bossmania/Vanilla-Terraria-Tools/releases/latest) and unzip it. 
2. Run the `setup.sh` file to setup the folder structure 
3. Tweak the `.env` file to your preference, if needed.
	- Note that for the `BACKUP_DURATION` field, the value should be in seconds.
4. Run the `download_server.sh` with the server version you want (without periods)
	- EX: `./download_server.sh 1450` to automatically download the server on version 1.4.5.0. 
5. Run `./start_server.sh` with the server version
	- EX: `./start_server.sh 1450` to start the server on version 1.4.5.0.
6. Create the world that you want.
7. Stop the server via either typing in `exit`, or pressing `CTRL + C`.
8. modify the config file for the server at `~/admin/config.txt`. 
	- Replace `[USERNAME]` with the linux user's username, and `[WORLD_NAME]` with the name of the world.
9. modify the `~/admin/approved_ips.txt` file to be a list of IPs (separated by new line) for the people who are allowed to use the / commands. The following is an example of what it should look like.
  ```
  127.0.0.1
  192.168.1.1
  10.0.0.1
  ```
10. start the server again (`./start_server.sh`) and it should automatically use the config file to auto load the world.

## Discord Bot Setup
0. [Setup the server wrapper](#Setup).
1. Follow the Discord's guide on [creating a bot](https://docs.discord.com/developers/quick-start/getting-started#step-1-creating-an-app).
2. open the `.env` from the project's folder, and put the bot's token in there.
3. Inside the Discord server, create the channels for interacting with the bot, read the server's chat, and getting notify from the bot.
	- There should be three channels created.
4. Go to User setting -> Advanced -> enable Developer mode.
5. Right click on each of the newly created channels, Copy channel ID, and paste in into the `.env` where it belongs to.
6. Run `python -m venv venv` to create the python venv.
7. Run `source venv/bin/activate` to activate the venv.
8. Run `pip install -r requirements.txt` to install the dependencies.
9. start the server again (`./start_server.sh`) and the bot should become active.

## Commands
- `/kick <USERNAME>`: kicks a player from the server.
- `/ban <USERNAME>`: ban a player from the server (can ban offline people).
- `/backup`: backup the world right now.
- `/rollback (/restore)`: shows the last 8 backups.
- `/rollback (/restore) <NUMBER>`: restore the world to the backup corresponding with the number.
- `/save`: save the world at the current's state.
- `/exit`: exits (and saves) the server.
- `/exit-nosave`: exit the server without saving.
- `/settle`: settles all of the liquids in the world.
- `/admin:` shows this help message.

## Discord_commands
- `!kick <USERNAME>`: kicks a player from the server.
- `!ban <USERNAME>`: ban a player from the server.
- `!backup`: backup the world.
- `!rollback (!restore)`: rollback to a backup from a list of recent backups.
- `!save`: Save the world.
- `!exit`: Save and exit the world.
- `{PREFIX}exit-nosave ({PREFIX}exit_nosave)`: Exit the world without saving.
- `!settle`: Settle the moving water.
- `!help`: Shows the help message.

### Other bash files
There are the `ban_player.sh` and the `world_backup.sh` bash files that wasn't mention so far. They can be used to ban (offline) players, via `./ban_player <USERNAME>`, and the `./world_backup.sh` to manually backup the world.

## AI disclaimer
For the stakes of transparency, I have used ChatGPT to generate me the basic skeleton of the server controller script, the skeleton of the discord bot, and to generate me the regex syntax. Everything else was written by me.
