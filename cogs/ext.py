from discord.ext import commands

class ExtCog(commands.Cog):
    """
        The Cog class is extended to become aware of its neighbors
        once all cogs are loaded in.
    """

    def finalize(self):
        pass