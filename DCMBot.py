import os
import discord
import asyncio
import requests

from discord.ext import commands
from dotenv import load_dotenv


load_dotenv(override=True)
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('DISCORD_PREFIX')
MAX_DELETE = os.getenv('DISCORD_MAX_DELETE')
DELETE_TIMEOUT = os.getenv('DELETE_TIMEOUT')
HELP_DELETE_TIMEOUT = os.getenv('HELP_DELETE_TIMEOUT')
INTERACTION_ROLE = os.getenv('DISCORD_BOT_INTERACTION_ROLE')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

def init():
    global MAX_DELETE
    global DELETE_TIMEOUT
    global HELP_DELETE_TIMEOUT

    assert TOKEN is not None or TOKEN != ""
    assert PREFIX is not None or PREFIX != ""  
    assert MAX_DELETE is not None or MAX_DELETE != "" 
    assert DELETE_TIMEOUT is not None or DELETE_TIMEOUT != ""
    assert HELP_DELETE_TIMEOUT is not None or HELP_DELETE_TIMEOUT != ""
    assert INTERACTION_ROLE is not None or INTERACTION_ROLE != "" 

    try: 
        MAX_DELETE = int(MAX_DELETE) 
        DELETE_TIMEOUT = int(DELETE_TIMEOUT) 
        HELP_DELETE_TIMEOUT = int(HELP_DELETE_TIMEOUT) 
    except Exception as e: 
        print(e)
        exit()

def is_me(m): 
    return m.author == bot.user

async def print_cowsay_help(ctx): 
    await ctx.send(embed=discord.Embed(
        title=f"Usage: {PREFIX}cowsay <text>",
        description="Draws a pretty picture of a cow with text",
        color=discord.Color.blue()
    ), delete_after=HELP_DELETE_TIMEOUT)

async def delete_by_emoji(ctx, args): 
    messages = []
    try:
        #This should add messages newest first to a list (messages) starting with the first one to have a down arrow 
        # emoji reaction, it will keep adding until it reaches the up arrow emoji 
        deleting = False
        async for message in ctx.channel.history(limit=MAX_DELETE):
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

        , delete_after=HELP_DELETE_TIMEOUT)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

###
## Command routes
### 
@bot.command()
@discord.ext.commands.has_role(INTERACTION_ROLE) # TODO Move to slash commands due to error handling
async def clear(ctx): 
    try: 
        deleted_msgs = await ctx.channel.purge(limit=MAX_DELETE) # TODO send this to a log file / audit file
        await ctx.send(f"Deleted {len(deleted_msgs)} messages.", delete_after=DELETE_TIMEOUT)
    except discord.Forbidden:
        await ctx.send("I don't have permission to delete messages in this channel.", delete_after=DELETE_TIMEOUT)
    except discord.HTTPException as e:
        print(f"An error occurred while trying to delete messages: {e}")

@bot.command() 
@discord.ext.commands.has_role(INTERACTION_ROLE) # TODO Move to slash commands due to error handling
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
@discord.ext.commands.has_role(INTERACTION_ROLE) # TODO Move to slash commands due to error handling
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
        await ctx.send(f"Deleted {len(messages)} messages!", delete_after=DELETE_TIMEOUT)

    except discord.Forbidden:
        await ctx.send("I don't have permission to delete messages in this channel.", delete_after=DELETE_TIMEOUT)
    except discord.HTTPException as e:
        print(f"An error occurred while trying to delete messages: {e}")

@bot.command()
@discord.ext.commands.has_role(INTERACTION_ROLE) # TODO Move to slash commands due to error handling
async def catgirl(ctx, *args):
    try: 
        await ctx.message.delete()
        
        r = requests.get("https://nekos.moe/api/v1/random/image")
        if r.status_code == 200: 
            image_id = r.json()["images"][0]["id"]

            image_request = requests.get(f"https://nekos.moe/image/{image_id}")
            
            if image_request.status_code != 200: 
                await ctx.send("Couldn't fetch your catgirls image :'(", delete_after=DELETE_TIMEOUT)
                return
            
            assert image_request.content is not None

            with open("catgirl.png", "wb") as f: 
                f.write(image_request.content)

            await ctx.send(file=discord.File("catgirl.png"))

            if os.path.exists("catgirl.png"): 
                os.remove("catgirl.png")

        else: 
            await ctx.send("Couldn't fetch your catgirl :(", delete_after=DELETE_TIMEOUT)
    except discord.HTTPException as e:
        print(f"An error occurred while trying to delete messages: {e}")
    except Exception as e: 
        print(e)

@bot.command()
@discord.ext.commands.has_role(INTERACTION_ROLE) # TODO Move to slash commands due to error handling
async def cowsay(ctx, *args): 
    try: 
        await ctx.message.delete()

        if not args: 
            await print_cowsay_help(ctx)
            return
        
        text = " ".join(args)
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
    except: 
        pass

if __name__ == "__main__":
    init()
    bot.run(TOKEN)