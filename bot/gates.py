from discord.ext import commands

# Command gates
def is_owner():
    def predicate(ctx):
        ctx.author.id == ctx.bot.config['owner_id']
    return commands.check(predicate)

def is_guild():
    def predicate(ctx):
        return ctx.guild is not None
    return predicate

def is_guild_owner():
    def predicate(ctx):
        return ctx.guild is not None and ctx.guild.owner_id == ctx.author.id
    return commands.check(predicate)