from discord.ext.commands.bot import AutoShardedBot, Bot
from path import Path
from cogs.ext import AgentCog
from uuid import uuid4 as uuidv4
from servman.helpers import ServmanAgent, Agent
import json
from json.decoder import JSONDecodeError


class Agent(AgentCog):
    """
        An agent which communicates with Servman process,
        which itself acts as the process manager for Mafia game instances.
    """
    def __init__(self, bot):
        super().__init__()

        # Config
        conf_path = Path("conf/agent_config.json")

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
        self.bot: AutoShardedBot or Bot = bot
        self.tasks = []
        self.servman_agent = ServmanAgent(connection_config=config)
        self.service_pool_identifier = 'mafia'

    # Overrides / Cog
    def cog_unload(self):
        for task in self.tasks:
            task.cancel()
        self.tasks = []


    async def finalize(self):
        connect_task = self.bot.loop.create_task(self.servman_agent.connect())
        consumer_task = self.bot.loop.create_task(self.servman_agent.consume())
        producer_task = self.bot.loop.create_task(self.servman_agent.produce())

        self.tasks = [connect_task, consumer_task, producer_task]

        print("Mafia Bot agent connecting to servman...")
        await self.servman_agent.wait_until_connected()
        print("Mafia Bot agent connected to servman.")

        for cog_name in self.bot.cogs:
            cog = self.bot.get_cog(cog_name)
            if isinstance(cog, AgentCog):
                self.servman_agent.inject_actions(cog, graft=True)
            else:
                print(f'{cog_name} is not an Agent')


def setup(bot: AutoShardedBot or Bot):
    bot.add_cog(Agent(bot))