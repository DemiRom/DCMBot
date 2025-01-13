import os
import discord

from discord.ext import commands
from discord.ext.commands import Context

class Horny(commands.Cog):
    def __init__(self, client): 
        self.client = client

        #Load env vars
        self.DELETE_TIMEOUT = int(os.getenv("DELETE_TIMEOUT"))

    @commands.hybrid_command(name="horny", description="Posts a go to horny jail bonk gif")
    async def Horny(self, ctx: Context): 
        try: 
            await self.client.change_presence(activity=discord.Game("Thinking..."))
            await ctx.send(file=discord.File("assets/gifs/gotohornyjail.gif"))

        except Exception as e: 
            await ctx.send("A general error has occurred.", delete_after=self.DELETE_TIMEOUT)
            self.client.logger.error(f"A general error has occurred {e}")

        await self.client.change_presence(activity=None)


async def setup(client: commands.Bot): 
    await client.add_cog(Horny(client))