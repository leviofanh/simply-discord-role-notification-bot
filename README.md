# Simply discord role notification bot

### Description

This Discord bot allows you to customize a special message that will be sent to users when they get a new role on the server.

### Setup

#### Prerequisites
- Python 3.x installed on your system.
- Discord.py library installed.

### Setup
1. Clone this repository.
2. Create a new app on the Discord developer portal.
3. Set up bot permissions on the Discord Developer Portal.
4. Create a key.txt file and paste your Discord bot token inside it.
5. Run the bot script:
   ##### python main.py
6. Set up bot permissions on the Discord Developer Portal.
7. Invite the bot to your Discord server using the OAuth2 URL generated from the Discord Developer Portal.

### Commands
The first thing to do is to customize the message.
There's a command for that:
#### //?setmsg your mesage

The following variables can be used in the command:
- {USER} - The user in the message will be mentioned.
- {ROLE} - It will be written which role was issued.
- {SERVER} - The name of the server will be mentioned in the server message.

There is an option to add roles to the exception. When issuing a role that is in exceptions, the user will not be notified.

Add to exception:
#### //?exrole @ROLE

Remove from the exception:
#### //?unerole @ROLE
