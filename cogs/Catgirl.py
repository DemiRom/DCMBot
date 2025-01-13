import os
import discord
import requests

from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

class Catgirl(commands.Cog):
    def __init__(self, client): 
        self.client = client

        #Load env vars
        self.DELETE_TIMEOUT = os.getenv("DELETE_TIMEOUT")

    @commands.hybrid_command(name="catgirl", description="Posts a catgirl nsfw selectable")
    async def Catgirl(self, ctx, *, nsfw: bool): 
        try: 
            r = requests.get("https://nekos.moe/api/v1/random/image", params={"nsfw": "true" if nsfw else "false", "count": 1})
            
            if r.status_code == 200: 
                image_id = r.json()["images"][0]["id"]

                await ctx.send(f"https://nekos.moe/image/{image_id}")

                if os.path.exists("catgirl.png"): 
                    os.remove("catgirl.png")

            else: 
                await ctx.send("Couldn't fetch your catgirl :(", delete_after=self.DELETE_TIMEOUT)
        except discord.HTTPException as e:
            print(f"An error occurred while trying to delete messages: {e}")
        except Exception as e: 
            print(e)

async def setup(client: commands.Bot): 
    await client.add_cog(Catgirl(client))