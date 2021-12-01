from asyncio import Queue
from discord.ext.commands.bot import AutoShardedBot, Bot
from path import Path
from cogs.ext import ExtCog
from uuid import uuid4 as uuidv4
from servman.helpers import ServmanAgent
import json
from json.decoder import JSONDecodeError

class Connection(ServmanAgent, ExtCog):
    """
        An agent which communicates with Servman process,
        which itself acts as the process manager for Mafia game instances.
    """
    def __init__(self, bot):
        # Config
        conf_path = Path("conf/connection_config.json")

        if not conf_path.exists():
            print(f"Error: File {conf_path} does not exist!")
            exit()

        config = ''

        try:
            config = json.loads(conf_path.read_text())
        except JSONDecodeError:
            print(f"Error: The JSON in {conf_path} is not formatted correctly.")
            exit()

        # Initialize ServmanAgent
        super().__init__(config)

        self.bot: AutoShardedBot or Bot = bot
        
        self.consumer_task = None
        self.producer_task = None


    @ServmanAgent.action
    async def send_dm_message(self, parcel):
        pass


    @ServmanAgent.action
    async def send_channel_message(self, parcel):
        pass


    @ServmanAgent.action
    async def send_guild_message(self, parcel):
        pass


    # Overrides / ServmanAgent


    # Overrides / Cog
    def cog_unload(self):
        if self.consumer_task:
            self.consumer_task.cancel()
        if self.producer_task:
            self.producer_task.cancel()


    async def finalize(self):
        self.consumer_task = self.bot.loop.create_task(self.consume())
        self.producer_task = self.bot.loop.create_task(self.produce())

        for cog_name in self.bot.cogs:
            cog_actions = getattr(self.bot.get_cog(cog_name), '_actions', None)
            if cog_actions:
                self._actions.update(cog_actions)
            else:
                print(f"Warning: No actions found on cog {cog_name}.")


def setup(bot: AutoShardedBot or Bot):
    bot.add_cog(Connection(bot))