import os
import discord

from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

class Rm(commands.Cog, name="rm"):
    def __init__(self, client): 
        self.client = client

        self.DELETE_TIMEOUT = os.getenv("DELETE_TIMEOUT")
        self.MAX_DELETE = os.getenv("DISCORD_MAX_DELETE")
        self.HELP_DELETE_TIMEOUT = os.getenv("HELP_DELETE_TIMEOUT")

    async def delete_by_emoji(self, ctx, emoji: str) -> list[discord.Message]: 
        messages = []
        try:
            #This should add messages newest first to a list (messages) starting with the first one to have a down arrow 
            # emoji reaction, it will keep adding until it reaches the up arrow emoji 
            deleting = False
            async for message in ctx.channel.history(limit=self.MAX_DELETE):
                if deleting:
                    await message.delete()
                    messages.append(message) 

                if any(reaction.emoji == emoji for reaction in message.reactions):
                    await message.delete()
                    messages.append(message) 
                    deleting = True
                elif any(reaction.emoji == emoji for reaction in message.reactions) and deleting:
                    await message.delete()
                    messages.append(message) 
                    deleting = False
                    break
        except: 
            pass

        return messages

    async def delete_by_count(self, ctx, count: int) -> list[discord.Message]: 
        try: 
            return await ctx.channel.purge(limit=count)
        except: 
            pass

        return []
    
    async def delete_by_user(ctx, user_id:str, count: int) -> list[discord.Message]: 
        try: 
            username = await ctx.bot.fetch_user(user_id.strip("<@>"))

            return await ctx.channel.purge(limit=count, check=lambda m: m.author == username)
        except Exception as e: 
            print(f"Error: {e}")
        
        return [] 

    @commands.hybrid_command(name="rm", description="Removes messages")
    async def rm(self, ctx: Context, *, switch: str, emoji: str = None, count: int = 1, user: discord.User = None): 
        try: 
            messages = []   
            if switch == "-e": 
                messages = self.delete_by_emoji(ctx, emoji)
            elif switch == "-c": 
                messages = self.delete_by_count(ctx, count)
            elif switch == "-u": 
                messages = self.delete_by_user(ctx, user, count)
            else:
                await ctx.send(embed=discord.Embed(
                    title=f"Usage: {os.getenv("DISCORD_PREFIX")}rm <args>",
                    description="This command will remove messages based on switch flags and arguments passed to the command!",
                    color=discord.Color.blue()
                )
                .add_field(name="Delete By Emoji", value="rm -e <emoji>\n\nSearches for the first instance of the emoji then keeps deleting until reaching another instance of that emoji or the configured limit!\n", inline=False)
                .add_field(name="Delete By Count", value="rm -c <count>\n\nDeletes any number of messages up to the configured limit starting with the newest ones!\n", inline=False)
                .add_field(name="Delete By Username", value="rm -u @<user> <count>\n\nDeletes any number of messages up to the configured limit starting with the newest ones from a specific user!\n", inline=False)

                , delete_after=self.HELP_DELETE_TIMEOUT)
                return

            await ctx.send(f"Deleted {len(messages)} messages!", delete_after=self.DELETE_TIMEOUT)


        except Exception as e: 
            print(f"An error has occured {e}")
        except discord.Forbidden:
            await ctx.send("I don't have permission to delete messages in this channel.", delete_after=DELETE_TIMEOUT)
        except discord.HTTPException as e:
            print(f"An error occurred while trying to delete messages: {e}")

async def setup(client: commands.Bot): 
    await client.add_cog(Rm(client))