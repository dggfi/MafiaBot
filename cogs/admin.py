from discord.commands import slash_command
from cogs.ext import ExtCog


class Admin(ExtCog):
    def __init__(self, bot):
        self.bot = bot
        self._actions = {}
    
    @slash_command(guild_ids=[843921354516332574], description="A test command. Don't be afraid to say hi!")
    async def hello(self, ctx, name: str = None):
        name = name or ctx.author.name
        await ctx.respond(f"Hello, {name}!")


def setup(bot):
    bot.add_cog(Admin(bot))