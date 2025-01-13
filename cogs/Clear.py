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
            await self.client.change_presence(activity=discord.Game("Thinking..."))
            await ctx.send("Deleting...", delete_after=self.DELETE_TIMEOUT)

            messages = await ctx.channel.purge(limit=self.MAX_DELETE) 
            
            for message in messages: 
                self.client.logger.info(f"Deleted: {message.content} from Display Name: {message.author.display_name} id: {message.author.id} UTC: {message.created_at}")
            
            await ctx.send(f"Deleted {len(messages)} messages.", delete_after=self.DELETE_TIMEOUT)

        except discord.Forbidden as e:
            await ctx.send("I don't have permission to delete messages in this channel.", delete_after=self.DELETE_TIMEOUT)
            self.client.logger.error(f"Permission denied to delete messages in channel! {e}")
        
        except discord.HTTPException as e:
            await ctx.send(f"An error occurred while trying to delete messages.", delete_after=self.DELETE_TIMEOUT)
            self.client.logger.error(f"An error occurred while trying to delete messages. {e}")
        
        except Exception as e: 
            await ctx.send("A general error has occurred!")
            self.client.logger.error(f"A general error has occured while trying to delete messages", delete_after=self.DELETE_TIMEOUT)

        await self.client.change_presence(activity=None)

async def setup(client: commands.Bot): 
    await client.add_cog(Clear(client))