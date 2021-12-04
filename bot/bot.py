import discord
from discord.ext import commands
from path import Path
import json
from json.decoder import JSONDecodeError
import sys
import traceback
import logging

# These cogs are interdepent/aware of each other
extended_cogs = (
    'cogs.admin',
    'cogs.agent',
    'cogs.ping'
)

class MafiaBot(commands.AutoShardedBot):
    def __init__(self):
        # State
        self.has_loaded_once = False

        # Logging
        logger = logging.getLogger('discord')
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(filename='logs/discord.log', encoding='utf-8', mode='w')
        handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        logger.addHandler(handler)
        self.logger = logger

        # Config
        config_path = Path("conf/bot_config.json")

        if not config_path.exists():
            print(f"Error: File {config_path} does not exist!")
            exit()
        
        config = ''
        
        try:
            config = json.loads(config_path.read_text())
        except JSONDecodeError:
            print(f"Error: The JSON in {config_path} is not formatted correctly.")
            exit()
        
        self.bot_config = config

        # Intents
        intents = discord.Intents(
            guilds=True,
            members=True,
            reactions=True
        )

        super().__init__(
            command_prefix = self.bot_config['default_command_prefix'],
            description = self.bot_config['description'],
            bot_public = self.bot_config['bot_public'],
            intents=intents
        )

        # Cogs
        for extension in extended_cogs:
            try:
                self.load_extension(extension)
            except Exception as e:
                print(f"Failed to load extension: {extension}.", file=sys.stderr)
                traceback.print_exc()
                exit()
    
    async def on_ready(self):
        for cog_name in self.cogs:
            cog = self.get_cog(cog_name)
            await cog.finalize()
        
        self.has_loaded_once = True
        print("Mafia Bot ready.")