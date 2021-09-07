import datetime
import json
import os
import time
from pathlib import Path
from cogs.help import HelpCommand
import discord
from discord.ext import commands

start_time = time.time()

# client
intents = discord.Intents.all()
client = commands.Bot(command_prefix='>', case_insensitive=True, owner_ids=[448740493468106753, 798584468998586388],
                      intents=intents, help_command=HelpCommand())


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

version = "10.1"


@client.command()
async def uptime(ctx):
    current_time = time.time()
    difference = int(round(current_time - start_time))
    text = str(datetime.timedelta(seconds=difference))
    embed = discord.Embed(colour=discord.Color.green())
    embed.add_field(name="Uptime", value=text)
    embed.set_footer(text="FRNz Aurora Uptime")
    try:
        await ctx.reply(embed=embed)
    except discord.HTTPException:
        await ctx.send("Current uptime: " + text)


if __name__ == "__main__":
    for file in os.listdir("cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            client.load_extension(f"cogs.{file[:-3]}")

    client.run(client.config_token)
