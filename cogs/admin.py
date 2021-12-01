from discord.commands import slash_command
from cogs.ext import ExtCog


class Admin(ExtCog):
    def __init__(self, bot):
        self.bot = bot
        self._actions = {}
    
    @slash_command()
    async def hello(self, ctx, name: str = None):
        name = name or ctx.author.name
        await ctx.respond(f"Hello, {name}!")


def setup(bot):
    bot.add_cog(Admin(bot))