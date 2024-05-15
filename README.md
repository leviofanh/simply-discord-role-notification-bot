# Simply discord role notification bot

### Description

This Discord bot enables you to personalize a custom message that will be sent to users upon receiving a new role on the server.
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
6. Invite the bot to your Discord server using the OAuth2 URL generated from the Discord Developer Portal.

### Commands
The first thing to do is to customize the message.
There's a command for that:
#### //?setmsg your message

You can utilize the following variables in the command:
- {USER} - Mentions the user in the message.
- {ROLE} - Specifies the issued role.
- {SERVER} - Mentions the name of the server in the message.

Additionally, you can manage exception roles. When a role listed in the exceptions is issued, the user will not receive a notification.

Add to exception:
#### //?exrole @ROLE

Remove from the exception:
#### //?unexrole @ROLE
