import os
import discord

from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

class Rm(commands.Cog, name="rm"):
    def __init__(self, client): 
        self.client = client

        self.DELETE_TIMEOUT = int(os.getenv("DELETE_TIMEOUT"))
        self.MAX_DELETE = int(os.getenv("DISCORD_MAX_DELETE"))
        self.HELP_DELETE_TIMEOUT = int(os.getenv("HELP_DELETE_TIMEOUT"))

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
            # Count + 1 because it will delete the last bot message without deleting the previous message as intended
            return await ctx.channel.purge(limit=count + 1)
        except Exception as e: 
            raise e

    async def delete_by_user(self, ctx, user_id: str, count: int) -> list[discord.Message]: 
        try: 
            member = await ctx.bot.fetch_user(user_id)

            return await ctx.channel.purge(limit=count, check=lambda m: m.author == member)
        except discord.NotFound: 
            await ctx.send("User does not exist!")
        except Exception as e: 
            raise e
        
        return [] 
    
    async def show_help(self, ctx): 
        await ctx.send(embed=discord.Embed(
                    title=f"Usage: {os.getenv("DISCORD_PREFIX")}rm <args>",
                    description="This command will remove messages based on switch flags and arguments passed to the command!",
                    color=discord.Color.blue()
                )
                .add_field(name="Delete By Emoji", value="rm -e <emoji>\n\nSearches for the first instance of the emoji then keeps deleting until reaching another instance of that emoji or the configured limit!\n", inline=False)
                .add_field(name="Delete By Count", value="rm -c <count>\n\nDeletes any number of messages up to the configured limit starting with the newest ones!\n", inline=False)
                .add_field(name="Delete By Username", value="rm -u @<user> <count>\n\nDeletes any number of messages up to the configured limit starting with the newest ones from a specific user!\n", inline=False)

                , delete_after=self.HELP_DELETE_TIMEOUT)

    @commands.hybrid_command(name="rm", description="Removes messages")
    async def rm(self, ctx: Context, *, switch: str, emoji: str = None, count: int = 0, user: discord.User = None): 
        try: 
            messages = []   
            await self.client.change_presence(activity=discord.Game("Thinking..."))
            await ctx.send("Deleting...", delete_after=self.DELETE_TIMEOUT)

            if switch == "-e": 
                if not emoji: 
                    await self.show_help()
                    return
                
                messages = await self.delete_by_emoji(ctx, emoji)

            elif switch == "-c": 
                if count == 0 or count > self.MAX_DELETE or count < 0: 
                    await self.show_help(ctx)
                    return

                messages = await self.delete_by_count(ctx, count)

                # all elements except the first one to have an accurate deleted message count.
                assert len(messages) > 1
                messages = messages[1:]

            elif switch == "-u":
                if not user: 
                    await self.show_help(ctx)
                    return
                
                if count == 0 or count > self.MAX_DELETE or count < 0:
                    count = self.MAX_DELETE

                messages = await self.delete_by_user(ctx, user.id, count)
            else:
                await self.show_help(ctx)
                return

            await ctx.send(f"Deleted {len(messages)} messages!", delete_after=self.DELETE_TIMEOUT)

            for message in messages: 
                self.client.logger.info(f"Deleted: {message.content} from Display Name: {message.author.display_name} id: {message.author.id} UTC: {message.created_at}")
            
        except discord.Forbidden:
            self.client.logger.error("Permission denied!")
            await ctx.send("I don't have permission to delete messages in this channel.", delete_after=self.DELETE_TIMEOUT)

        except discord.HTTPException as e:
            self.client.logger.error(f"An error occurred while trying to delete messages {e}")
            await ctx.send(f"An error occurred while trying to delete messages")

        except Exception as e: 
            self.client.logger.error(f"A general error occured while trying to delete users messages {e}")
            await ctx.send(f"A general error occurred while trying to delete messages")

        await self.client.change_presence(activity=None)

async def setup(client: commands.Bot): 
    await client.add_cog(Rm(client))