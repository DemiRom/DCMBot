import os
import discord
import requests

from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

class Jesus(commands.Cog):
    def __init__(self, client): 
        self.client = client

        #Load env vars
        self.DELETE_TIMEOUT = int(os.getenv("DELETE_TIMEOUT"))

    @commands.hybrid_command(name="jesus", description="Quotes a random bible verse")
    async def jesus(self, ctx): 
        try: 
            await self.client.change_presence(activity=discord.Game("Thinking..."))
            await ctx.send("Thinking...", delete_after=self.DELETE_TIMEOUT)

            r = requests.get("https://bible-api.com/data/web/random")

            if r.status_code == 200: 
                text = r.json()["random_verse"]["text"]
                await ctx.send(text)

            else: 
                await ctx.send("Couldn't fetch your jesus quote :(", delete_after=self.DELETE_TIMEOUT)
        except discord.HTTPException as e:
            await ctx.send(f"An error occurred while trying to delete messages")
            self.client.logger.error(f"HTTP Exception: {e}")
        except Exception as e: 
            await ctx.send("A general error has occurred!")
            self.client.logger.error(f"General error for Jesus {e}")

        await self.client.change_presence(activity=None)



async def setup(client: commands.Bot): 
    await client.add_cog(Jesus(client))