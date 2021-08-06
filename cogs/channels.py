import discord
from discord.ext import commands



class Channels(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.command(name = "sm")
    @commands.has_permissions(manage_roles=True)
    async def setdelay(self, ctx, seconds: int):
        """
        This command is used to add/remove slowmode in chat
        """
        await ctx.message.delete()
        await ctx.channel.edit(slowmode_delay=seconds)
        if seconds == 0:
            await ctx.send(f"Slowmode disabled for {ctx.channel.mention}")
        else:
            await ctx.send(f"Channel {ctx.channel.mention} slowmode set to {seconds} seconds.")

    @commands.command(aliases=["lock", "l"])
    @commands.has_permissions(manage_channels=True)
    async def lockdown(self, ctx, channel: discord.TextChannel = None):
        """
        This Command is used to Lock Or Unlock a Channel
        """
        channel = channel or ctx.channel
        await ctx.message.delete()
        if ctx.guild.default_role not in channel.overwrites:
            # This is the same as the elif except it handles agaisnt empty overwrites dicts
            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(send_messages=False)
            }
            await channel.edit(overwrites=overwrites)
            await ctx.send(f"I have put {channel.name} on lockdown.")
        elif (
            channel.overwrites[ctx.guild.default_role].send_messages == True
            or channel.overwrites[ctx.guild.default_role].send_messages == None
        ):
            overwrites = channel.overwrites[ctx.guild.default_role]
            overwrites.send_messages = False
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
            await ctx.send(f"I have put {channel.mention} on lockdown.")
        else:
            overwrites = channel.overwrites[ctx.guild.default_role]
            overwrites.send_messages = True
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
            await ctx.send(f"I have removed {channel.mention} from lockdown.")

def setup(client):
    client.add_cog(Channels(client))