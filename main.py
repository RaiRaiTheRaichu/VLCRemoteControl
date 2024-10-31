import discord
from discord.ext import commands
import utils
import custom_commands as custom_commands


# Getting config + constants
config = utils.FetchConfig('config.jsonc')
TOKEN = config['DISCORD_TOKEN']
ALLOWED_ROLES = config['ALLOWED_ROLES']

# Setting bot intents, registering commands with the following intents
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix='vlc!', intents=intents)

# When bot starts, run this code
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

# When an error occurs from a command, reply to the user informing them they lack permissions
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.reply('You do not have the correct role for this command.')

# Register all commands from commands.py (found in the array at the end of the file)
for command_to_register in custom_commands.command_list:
    bot.add_command(command_to_register)

# Run the bot using its token.
bot.run(TOKEN)
