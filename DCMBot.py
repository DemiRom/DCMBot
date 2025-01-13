import os
import asyncio
import logging

from dotenv import load_dotenv
from Client import Client
from LoggingFormatter import LoggingFormatter

load_dotenv(override=True)

TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('DISCORD_PREFIX')
MAX_DELETE = os.getenv('DISCORD_MAX_DELETE')
DELETE_TIMEOUT = os.getenv('DELETE_TIMEOUT')
HELP_DELETE_TIMEOUT = os.getenv('HELP_DELETE_TIMEOUT')
INTERACTION_ROLE = os.getenv('DISCORD_BOT_INTERACTION_ROLE')

logger = logging.getLogger("discord_bot")
logger.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(LoggingFormatter())
# File handler
file_handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
file_handler_formatter = logging.Formatter(
    "[{asctime}] [{levelname:<8}] {name}: {message}", "%Y-%m-%d %H:%M:%S", style="{"
)
file_handler.setFormatter(file_handler_formatter)

# Add the handlers
logger.addHandler(console_handler)
logger.addHandler(file_handler)

client = Client(PREFIX, logger)

if __name__ == "__main__":
    client.run(TOKEN)

# ###
# ## Command routes
# ### 
# @bot.command()
# @discord.ext.commands.has_role(INTERACTION_ROLE) # TODO Move to slash commands due to error handling
# async def rm(ctx, *args):
#     print(f'Args: {args}')

#     messages = []
#     try:
#         await ctx.message.delete()

#         if not args: 
#             await print_rm_help(ctx)
#             return

#         switch = args[0]
#         args = args[1:]

#         if switch == "-e": 
#             messages = await delete_by_emoji(ctx, args)
#         elif switch == "-c": 
#             try: 
#                 int(args[0])
#             except ValueError or TypeError: 
#                 await print_rm_help(ctx)
#                 return
            
#             messages = await delete_by_count(ctx, args)
#         elif switch == "-u": 
#             try: 
#                 int(args[1])
#             except ValueError or TypeError: 
#                 await print_rm_help(ctx)
#                 return
            
#             messages = await delete_by_user(ctx, args)
#         else: 
#             await print_rm_help(ctx)
#             return

#         # TODO Dump deleted messages into a log file
#         await ctx.send(f"Deleted {len(messages)} messages!", delete_after=DELETE_TIMEOUT)

#     except discord.Forbidden:
#         await ctx.send("I don't have permission to delete messages in this channel.", delete_after=DELETE_TIMEOUT)
#     except discord.HTTPException as e:
#         print(f"An error occurred while trying to delete messages: {e}")
