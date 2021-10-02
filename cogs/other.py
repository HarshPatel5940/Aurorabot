import discord
from discord.ext import commands
import typing


class Others(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def echo(self, ctx, channel: typing.Optional[discord.TextChannel] = None, *, message):
        """
        This Command is used to send a Message Through Bot in a channel
        """

        channel = ctx.channel if not channel else channel
        files = [await attachment.to_file() for attachment in
                 ctx.message.attachments] if ctx.message.attachments != [] else None
        message1 = message
        await ctx.message.delete()
        await channel.send(message1, files=files)

    @commands.command(aliases=["emb"])
    @commands.has_permissions(manage_roles=True)
    async def embed(self, ctx, channel: typing.Optional[discord.TextChannel] = None, *, message):
        """
        This Command is used to send a Embed Through Bot in a channel
        """
        channel = channel or ctx.channel
        embed = discord.Embed(description=message, color=discord.Color.teal())
        await channel.send(embed=embed)
        await ctx.message.add_reaction("✅")

    @commands.command(name="editemb")
    @commands.has_permissions(manage_roles=True)
    async def edit_embed(self, ctx, channel: discord.TextChannel, id_: int, *, message):
        """
        This Command is used to Edit Exsisting Embed
        """
        msg1 = 0
        try:
            msg1 = await channel.fetch_message(id_)
        except:
            await ctx.send("The channel or ID mentioned was incorrect")

        new_embed = discord.Embed(description=message, color=discord.Color.teal())
        await msg1.edit(embed=new_embed)
        await ctx.message.add_reaction("✅")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def dm(self, ctx, user: discord.Member, *, message):
        """
        This Command is used to send a Message Through Bot in a DM
        """
        files = [await attachment.to_file() for attachment in
                 ctx.message.attachments] if ctx.message.attachments != [] else None

        message1 = message
        await user.send(message1, files=files)
        await ctx.message.add_reaction("✅")

    @commands.command(aliases=["dmemb"])
    @commands.has_permissions(manage_roles=True)
    async def dm_embed(self, ctx, user: discord.Member, *, message):
        """
        This Command is used to send a Embed Through Bot in a channel
        """
        embed = discord.Embed(description=message, color=discord.Color.teal())
        await user.send(embed=embed)
        await ctx.message.add_reaction("✅")


def setup(bot):
    bot.add_cog(Others(bot))
