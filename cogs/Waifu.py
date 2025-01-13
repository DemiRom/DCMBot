import os
import discord
import requests

from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

class Waifu(commands.Cog):
    def __init__(self, client): 
        self.client = client

        #Load env vars
        self.DELETE_TIMEOUT = int(os.getenv("DELETE_TIMEOUT"))

    @commands.hybrid_command(name="waifu", description="Posts a picture of a waifu nsfw selectable")
    async def waifu(self, ctx, *, nsfw: bool): 
        try: 
            await self.client.change_presence(activity=discord.Game("Thinking..."))
            await ctx.send("Thinking...", delete_after=self.DELETE_TIMEOUT)

            r = requests.get("https://api.waifu.pics/nsfw/waifu") if nsfw else requests.get("https://api.waifu.pics/sfw/waifu")

            if r.status_code == 200: 
                image_url = r.json()["url"]

                await ctx.send(image_url)

                if os.path.exists("waifu.png"): 
                    os.remove("waifu.png")
            else: 
                await ctx.send("Couldn't fetch your waifu :(", delete_after=self.DELETE_TIMEOUT)
        except discord.HTTPException as e:
            self.client.logger.error("An error occurred while trying to delete messages: {e}")
            await ctx.send(f"An error occurred while trying to delete messages: {e}")
        except Exception as e: 
            self.client.logger.error(f"A general error has occurred {e}")
            await ctx.send("General error has occurred")

        await self.client.change_presence(activity=None)


async def setup(client: commands.Bot): 
    await client.add_cog(Waifu(client))