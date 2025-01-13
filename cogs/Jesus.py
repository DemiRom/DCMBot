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
        self.DELETE_TIMEOUT = os.getenv("DELETE_TIMEOUT")

    @commands.hybrid_command(name="jesus", description="Quotes a random bible verse")
    async def Jesus(self, ctx): 
        try: 
            r = requests.get("https://bible-api.com/data/web/random")

            if r.status_code == 200: 
                text = r.json()["random_verse"]["text"]
                await ctx.send(text)

            else: 
                await ctx.send("Couldn't fetch your jesus quote :(", delete_after=self.DELETE_TIMEOUT)
        except discord.HTTPException as e:
            print(f"An error occurred while trying to delete messages: {e}")
        except Exception as e: 
            print(e)

async def setup(client: commands.Bot): 
    await client.add_cog(Jesus(client))