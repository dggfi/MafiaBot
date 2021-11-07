from discord.ext import commands
from path import Path
import json
from json.decoder import JSONDecodeError
import sys
import traceback
import asyncio
from bot.typings import IConfig

# These cogs are interdepent/aware of each other
extended_cogs = (

)

class MafiaBot(commands.AutoShardedBot):
    def __init__(self):
        self.has_loaded_once = False

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
        
        self.config: IConfig = config

        super().__init__(
            command_prefix = self.config['default_command_prefix'],
            description = self.config['description'],
            bot_public = self.config['bot_public']
        )

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
            cog.finalize()
        
        self.has_loaded_once = True