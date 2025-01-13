import os
import discord

from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

class Clear(commands.Cog):
    def __init__(self, client): 
        self.client = client

        self.DELETE_TIMEOUT = int(os.getenv("DELETE_TIMEOUT"))
        self.MAX_DELETE = int(os.getenv('DISCORD_MAX_DELETE'))

    @commands.hybrid_command(name="clear", description="Clears up to the configured amount of messages")
    async def Clear(self, ctx: Context): 
        try:
            await ctx.send("Deleting...", delete_after=self.DELETE_TIMEOUT)  
            deleted_msgs = await ctx.channel.purge(limit=self.MAX_DELETE) 
            await ctx.send(f"Deleted {len(deleted_msgs)} messages.", delete_after=self.DELETE_TIMEOUT)
        except discord.Forbidden:
            await ctx.send("I don't have permission to delete messages in this channel.", delete_after=self.DELETE_TIMEOUT)
        except discord.HTTPException as e:
            await ctx.send(f"An error occurred while trying to delete messages.", delete_after=self.DELETE_TIMEOUT)
        except Exception as e: 
            print(f"An general error has occured while trying to delete messages", delete_after=self.DELETE_TIMEOUT)

async def setup(client: commands.Bot): 
    await client.add_cog(Clear(client))