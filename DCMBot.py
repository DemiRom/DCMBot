import os
import discord
import asyncio

# from CommandParser import CommandParser
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('DISCORD_PREFIX')

assert TOKEN is not None or TOKEN != ""
assert PREFIX is not None or PREFIX != ""  

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

def is_me(m): 
    return m.author == bot.user

async def delete_by_emoji(ctx, args): 
    messages = []
    try:
        #This should add messages newest first to a list (messages) starting with the first one to have a down arrow 
        # emoji reaction, it will keep adding until it reaches the up arrow emoji 
        deleting = False
        async for message in ctx.channel.history(limit=250):
            if deleting:
                await message.delete()
                messages.append(message) 

            if any(reaction.emoji == args[0] for reaction in message.reactions):
                await message.delete()
                messages.append(message) 
                deleting = True
            elif any(reaction.emoji == args[0] for reaction in message.reactions) and deleting:
                await message.delete()
                messages.append(message) 
                deleting = False
                break
    except: 
        pass

    return messages

async def delete_by_count(ctx, args): 
    try: 
        return await ctx.channel.purge(limit=int(args[0]))
    except: 
        pass

    return []

async def delete_by_user(ctx, args): 
    try: 
        username = await ctx.bot.fetch_user(args[0].strip("<@>"))

        return await ctx.channel.purge(limit=int(args[1]), check=lambda m: m.author == username)
    except Exception as e: 
        print(f"Error: {e}")
    
    return [] 

async def print_rm_help(ctx): 
    await ctx.send(embed=discord.Embed(
            title=f"Usage: {PREFIX}rm <args>",
            description="This command will remove messages based on switch flags and arguments passed to the command!",
            color=discord.Color.blue()
        )
        .add_field(name="Delete By Emoji", value="rm -e <emoji>\n\nSearches for the first instance of the emoji then keeps deleting until reaching another instance of that emoji or the configured limit!\n", inline=False)
        .add_field(name="Delete By Count", value="rm -c <count>\n\nDeletes any number of messages up to the configured limit starting with the newest ones!\n", inline=False)
        .add_field(name="Delete By Username", value="rm -u @<user> <count>\n\nDeletes any number of messages up to the configured limit starting with the newest ones from a specific user!\n", inline=False)

        , delete_after=25)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command()
async def clear(ctx): 
    try: 
        deleted_msgs = await ctx.channel.purge(limit=100) # TODO send this to a log file / audit file
        await ctx.send(f"Deleted {len(deleted_msgs)} messages.", delete_after=5)
    except discord.Forbidden:
        await ctx.send("I don't have permission to delete messages in this channel.", delete_after=5)
    except discord.HTTPException as e:
        print(f"An error occurred while trying to delete messages: {e}")

@bot.command() 
async def echo(ctx, *args):
    try: 
        await ctx.message.delete()

        if not args: 
            await ctx.send(embed=discord.Embed(
                title=f"Usage: {PREFIX}echo <text to echo>",
                description="This command will just echo back whatever you put as an argument!",
                color=discord.Color.blue()
            ), delete_after=10)
            return

        await ctx.send(" ".join(args)) 
    except: 
        print("An error has occured :kappa:")

@bot.command()
async def rm(ctx, *args):
    print(f'Args: {args}')

    messages = []
    try:
        await ctx.message.delete()

        if not args: 
            await print_rm_help(ctx)
            return

        switch = args[0]
        args = args[1:]

        if switch == "-e": 
            messages = await delete_by_emoji(ctx, args)
        elif switch == "-c": 
            try: 
                int(args[0])
            except ValueError or TypeError: 
                await print_rm_help(ctx)
                return
            
            messages = await delete_by_count(ctx, args)
        elif switch == "-u": 
            try: 
                int(args[1])
            except ValueError or TypeError: 
                await print_rm_help(ctx)
                return
            
            messages = await delete_by_user(ctx, args)
        else: 
            await print_rm_help(ctx)
            return

        # TODO Dump deleted messages into a log file
        await ctx.send(f"Deleted {len(messages)} messages!", delete_after=5)

    except discord.Forbidden:
        await ctx.send("I don't have permission to delete messages in this channel.", delete_after=5)
    except discord.HTTPException as e:
        print(f"An error occurred while trying to delete messages: {e}")


if __name__ == "__main__":
    bot.run(TOKEN)