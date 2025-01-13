import os
import discord

from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

class Echo(commands.Cog, name="echo"):
    def __init__(self, client): 
        self.client = client

    @commands.hybrid_command(name="echo", description="Echo the users input")
    async def echo(self, ctx: Context, *, text: str): 
        try:   
            if text != "":
                await ctx.send(text) 
            else: 
                await ctx.send(embed=discord.Embed(
                    title=f"Usage: /echo <text to echo>",
                    description="This command will just echo back whatever you put as an argument!",
                    color=discord.Color.blue()
                ), delete_after=os.getenv("HELP_DELETE_TIMEOUT"))
                return
        except Exception as e: 
            print(f"An error has occured {e}")

async def setup(client: commands.Bot): 
    await client.add_cog(Echo(client))