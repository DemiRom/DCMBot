import os
import discord
import requests

from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

class SendLog(commands.Cog):
    def __init__(self, client): 
        self.client = client

        #Load env vars
        self.DELETE_TIMEOUT = int(os.getenv("DELETE_TIMEOUT"))

    @commands.hybrid_command(name="sendlog", description="Sends the entire log to the user that calls the command")
    async def sendlog(self, ctx): 
        try: 
            await self.client.change_presence(activity=discord.Game("Thinking..."))
            await ctx.send("Thinking...", delete_after=self.DELETE_TIMEOUT)

            with open("discord.log", "r") as f: 
                lines = f.readlines()
                await ctx.author.send(f"```{"\n".join(lines)}```")

        except discord.HTTPException as e:
            await ctx.send(f"An error occurred while trying to delete messages")
            self.client.logger.error(f"HTTP Exception: {e}")
        except Exception as e: 
            await ctx.send("A general error has occurred!")
            self.client.logger.error(f"General error for SendLog {e}")

        await self.client.change_presence(activity=None)



async def setup(client: commands.Bot): 
    await client.add_cog(SendLog(client))