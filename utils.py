import os
import discord
from discord.ext import commands
import jsoncomment

# Fetch the config from the given path.
def FetchConfig(path):
    with open(path, 'r') as configFile:
       parser = jsoncomment.JsonComment()
       configLocal = parser.load(configFile)
    return configLocal

# Check if the user has any of the following roles before allowing certain commands.
def CheckPrivilege(roles):
    def predicate(ctx):
        user_roles = [role.name for role in ctx.author.roles]
        return any(role in roles for role in user_roles)

    return commands.check(predicate)