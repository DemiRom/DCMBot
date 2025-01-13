import os
import discord

from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

class Cowsay(commands.Cog):
    def __init__(self, client): 
        self.client = client

        self.HELP_DELETE_TIMEOUT = int(os.getenv("HELP_DELETE_TIMEOUT"))
        self.DELETE_TIMEOUT = int(os.getenv("DELETE_TIMEOUT"))

    @commands.hybrid_command(name="cowsay", description="Prints ascii art of a cow with a speech bubble")
    async def Cowsay(self, ctx, *, text: str): 
        try:   
            await self.client.change_presence(activity=discord.Game("Thinking..."))
            await ctx.send("Thinking...", delete_after=self.DELETE_TIMEOUT)

            if not text: 
                await ctx.send(embed=discord.Embed(
                    title=f"Usage: cowsay <text>",
                    description="Draws a pretty picture of a cow with text",
                    color=discord.Color.blue()
                ), delete_after=self.HELP_DELETE_TIMEOUT)
                return

            header = "_"*(len(text)+4)
            footer = "-"*(len(text)+4)
            spaces = " "*(len(text)+4)

            await ctx.send(f'''```
            {header} 
            < {text} >  
            {footer} 
            {spaces}\\ 
            {spaces}\\   ^__^  
            {spaces}\\  (oo)\\_______
            {spaces}    (__)\\       )\\/\\
            {spaces}        ||----w |
            {spaces}        ||     ||```''')

        except Exception as e: 
            await ctx.send("A general error occurred", delete_afer=self.DELETE_TIMEOUT)
            self.client.logger.erro(f"A general error has occured {e}")

        await self.client.change_presence(activity=None)


async def setup(client: commands.Bot): 
    await client.add_cog(Cowsay(client))