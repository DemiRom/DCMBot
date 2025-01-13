import discord

from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

class Echo(commands.Cog, name="echo"):
    def __init__(self, client): 
        self.client = client

    @commands.hybrid_command(name="echo", descrtion="Echo the users input")
    async def echo(self, ctx: Context, *, text: str, optional: int = 0): 
        await ctx.send(f"{ctx.message.content}")
        try:   
            # if not args: 
            #     await ctx.send(embed=discord.Embed(
            #         title=f"Usage: {PREFIX}echo <text to echo>",
            #         description="This command will just echo back whatever you put as an argument!",
            #         color=discord.Color.blue()
            #     ), delete_after=10)
            #     return
            print(ctx)
            print(text)

            if text != "":
                await ctx.send(f"Something something: {text}") 
            else: 
                print("NO ARGS")
        except Exception as e: 
            print(f"An error has occured {e}")

async def setup(client: commands.Bot): 
    await client.add_cog(Echo(client))