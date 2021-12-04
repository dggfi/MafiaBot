from discord.ext import commands
from servman.helpers import Agent

class ExtCog(commands.Cog):
    """
        The Cog class is extended to become aware of its neighbors
        once all cogs are loaded in.
    """

    async def finalize(self):
        pass


class AgentCog(Agent, ExtCog):
    pass