# VLC Remote Control

A basic Discord bot written in Python to interact with VLC Media Player on a host machine.

Some configuration is necessary, and assumes you are familiar with creating a Discord bot via the Developer Portal, retrieve its private token, and generate a proper OAuth2 link for your server.

### How to use

1. Download this project's source code.
2. Ensure you have the 64-bit version of VLC Media Player installed and added to your host machine's PATH if necessary.
3. Install the prerequisite packages (using `pip`) - see below for a list of necessary packages.
4. Place video files in a `videos` folder next to these scripts.
5. Edit config.jsonc, add your bot token to the proper field, and set the names of the required roles to interact with the bot.
6. Run the program with main.py.

### Required permissions

In the OAuth2 URL Generator:
1. `bot`

In the Bot Permissions:
1. `Send Messages`
2. `Read Message History`
3. `View Channels`

### Known issues

The channel whitelist feature in config.jsonc currently is not implemented.

### Reference list

Required packages:
1. 64-bit Python (3.12.3)
2. discord.py (2.4.0) - `pip install discord.py`
3. jsoncomment (0.4.2) - `pip install jsoncomment`
4. python-vlc (3.0.21203) - `pip install python-vlc`

### Credits
RaiRaiTheRaichu
