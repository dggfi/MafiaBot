import os
from path import Path
import json

# bot_config.json
bot_config_file = Path("./conf/bot_config.json")

if bot_config_file.exists():
    bot_config_file.remove()

bot_defaults = {
    'token': 'yourtokenhere',
    'description': 'a description for the bot',
    'default_command_prefix': '!',
    'owner_id': 'youridhere',
    'bot_public': True,
    'suppress_configuration_warnings': False,
    'host': 'localhost',
    'port': 443
}
txt = json.dumps(bot_defaults, indent=4)
bot_config_file.write_text(txt)

# server_config.json
server_config_file = Path("conf/server_config.json")

if server_config_file.exists():
    server_config_file.remove()

server_defaults = {
    'host': 'localhost',
    'port': '8000'
}
txt = json.dumps(server_defaults, indent=4)
server_config_file.write_text(txt)