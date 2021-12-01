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
    'guild_ids': [],
    'suppress_configuration_warnings': False,
    'host': 'localhost',
    'port': 443
}
txt = json.dumps(bot_defaults, indent=4)
bot_config_file.write_text(txt)

# servman_config.json
# The server for game instances
servman_config_file = Path("conf/servman_config.json")
if servman_config_file.exists():
    servman_config_file.remove()

servman_defaults = {
    'host': 'localhost',
    'port': 8000
}

txt = json.dumps(servman_defaults, indent=4)
servman_config_file.write_text(txt)

# agent_config.json
# this represents your connection to the Servman server
agent_config_file = Path("conf/agent_config.json")

if agent_config_file.exists():
    agent_config_file.remove()

server_defaults = {
    'host': 'localhost',
    'port': '8000'
}

txt = json.dumps(server_defaults, indent=4)
agent_config_file.write_text(txt)