import discord

from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

class Cowsay(commands.Cog):
    def __init__(self, client): 
        self.client = client

    @commands.hybrid_command(name="cowsay", descrtion="Prints ascii art of a cow with a speech bubble")
    async def Cowsay(self, ctx): 
        # await ctx.message.delete()
        try:   
            # if not args: 
            #     await ctx.send(embed=discord.Embed(
            #         title=f"Usage: {PREFIX}echo <text to echo>",
            #         description="This command will just echo back whatever you put as an argument!",
            #         color=discord.Color.blue()
            #     ), delete_after=10)
            #     return

            await ctx.send("Cow says moo") 
        except Exception as e: 
            print(f"An error has occured {e}")

async def setup(client: commands.Bot): 
    await client.add_cog(Cowsay(client))