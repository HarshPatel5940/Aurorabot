import datetime
import json
import os
import time
from pathlib import Path

import discord
from discord.ext import commands

start_time = time.time()

# client
intents = discord.Intents.all()
client = commands.Bot(command_prefix='>', case_insensitive=True, owner_ids=[448740493468106753, 798584468998586388],
                      intents=intents)
client.remove_command("help")

cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----")

with open("secret.json") as f:
    data = json.load(f)
    client.config_token = data["token"]
    f.close()


@client.event
async def on_ready():
    # stuff
    print("Bot is alive")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="PunisherYT"))


client.version = "7"


@client.command()
@commands.is_owner()
async def load(ctx, cog):
    """
    This Command is Used to Load a Cog
    """
    client.load_extension(f"cogs.{cog}")
    await ctx.message.delete()
    await ctx.send(f"{cog} loaded successfully")


@client.command()
@commands.is_owner()
async def unload(ctx, cog):
    """
    This command is Used to UnLoad a cog
    """
    client.unload_extension(f"cogs.{cog}")
    await ctx.message.delete()
    await ctx.send(f"{cog} unloaded successfully.")


@client.command()
async def uptime(ctx):
    current_time = time.time()
    difference = int(round(current_time - start_time))
    text = str(datetime.timedelta(seconds=difference))
    embed = discord.Embed(colour=ctx.message.author.colour)
    embed.add_field(name="Uptime", value=text)
    embed.set_footer(text="FRNz Aurora Uptime")
    await ctx.message.delete()
    try:
        await ctx.send(embed=embed)
    except discord.HTTPException:
        await ctx.send("Current uptime: " + text)


@client.command()
@commands.is_owner()
async def logout(ctx):
    """
    This command is used to ShutDown the Bot
    """
    await ctx.send(f'Hey! {ctx.author.mention} I am now logging out :wave: ')
    await client.logout()


@logout.error
async def logout_error(ctx, error):
    if isinstance(error, commands.CheckFailure):

        await ctx.send(f"you lack on permissions to use this command or you do not ouwn the bot")
    else:
        print("something is wrong pls check")


if __name__ == "__main__":
    for file in os.listdir("cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            client.load_extension(f"cogs.{file[:-3]}")

    # Keep_alive()
    client.run(client.config_token)
