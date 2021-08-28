import discord
from discord.ext import commands
import platform

from main import version


class Stats(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.command(name="emojiinfo", aliases=["ei"])
    async def emoji_info(self, ctx, emoji: discord.Emoji = None):
        if not emoji:
            return await ctx.invoke(self.client.get_command("help"), entity="emojiinfo")

        try:
            emoji = await emoji.guild.fetch_emoji(emoji.id)
        except discord.NotFound:
            return await ctx.send("I could not find this emoji in the given guild.")

        is_managed = "Yes" if emoji.managed else "No"
        is_animated = "Yes" if emoji.animated else "No"
        requires_colons = "Yes" if emoji.require_colons else "No"
        creation_time = emoji.created_at.strftime("%I:%M %p %B %d, %Y")
        can_use_emoji = (
            "Everyone"
            if not emoji.roles
            else " ".join(role.name for role in emoji.roles)
        )

        description = f"""
        **General:**
        **- Name:** {emoji.name}
        **- Id:** {emoji.id}
        **- URL:** [Link To Emoji]({emoji.url})
        **- Author:** {emoji.user.mention}
        **- Time Created:** {creation_time}
        **- Usable by:** {can_use_emoji}
        
        **Other:**
        **- Animated:** {is_animated}
        **- Managed:** {is_managed}
        **- Requires Colons:** {requires_colons}
        **- Guild Name:** {emoji.guild.name}
        **- Guild Id:** {emoji.guild.id}
        """

        embed = discord.Embed(
            title=f"**Emoji Information for:** `{emoji.name}`",
            description=description,
            colour=0xADD8E6,
        )
        embed.set_thumbnail(url=emoji.url)
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.lower() == ">bot info":

            pythonVersion = platform.python_version()
            dpyVersion = discord.__version__
            serverCount = len(self.client.guilds)
            memberCount = len(set(self.client.get_all_members()))
            mem1=self.client.get_user(854230635425693756)
            embed = discord.Embed(
                title=f"{mem1.name} Stats | Prefix is >",
                description="get the info of the bot in short",
                colour=message.author.colour,
                timestamp=message.created_at,
            )

            embed.add_field(name="Bot Version:", value=version)
            embed.add_field(name="Python Version:", value=pythonVersion)
            embed.add_field(name="Discord.Py Version", value=dpyVersion)
            embed.add_field(name="Total Guilds:", value=serverCount)
            embed.add_field(name="Total Users:", value=memberCount)
            embed.add_field(name="Bot Made By:", value="<@448740493468106753>")

            embed.set_footer(text=f"FRNz Official Community | {self.client.user.name}")
            embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar.url)
            embed.set_thumbnail(url=self.client.user.avatar.url)
            await message.channel.send(embed=embed)

    @commands.command(name="channelstats", aliases=["cs"])
    async def channel_stats(self, ctx, channel: discord.TextChannel = None):
        """
        This Command Provides us the stats of the channel
        """
        channel = channel or ctx.channel
        embed = discord.Embed(
            title=f"Stats for **{channel.name}**",
            description=f"{'Category: {}'.format(channel.category.name) if channel.category else 'This channel is not in a category'}",
            color=0x2ECC71,
        )
        embed.add_field(name="Channel Guild", value=ctx.guild.name, inline=False)
        embed.add_field(name="Channel Id", value=channel.id, inline=False)
        embed.add_field(
            name="Channel Topic",
            value=f"{channel.topic if channel.topic else 'No topic.'}",
            inline=False,
        )
        embed.add_field(name="Channel Position", value=channel.position, inline=False)
        embed.add_field(
            name="Channel Slowmode Delay", value=channel.slowmode_delay, inline=False
        )
        embed.add_field(name="Channel is nsfw?", value=channel.is_nsfw(), inline=False)
        embed.add_field(name="Channel is news?", value=channel.is_news(), inline=False)
        embed.add_field(
            name="Channel Creation Time", value=channel.created_at, inline=False
        )
        embed.add_field(
            name="Channel Permissions Synced",
            value=channel.permissions_synced,
            inline=False,
        )
        embed.add_field(name="Channel Hash", value=hash(channel), inline=False)

        await ctx.message.delete()
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Stats(client))
