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