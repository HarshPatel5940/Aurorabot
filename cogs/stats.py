import platform
from datetime import datetime
from typing import Optional

import discord
from discord.ext import commands


class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.command(name="emojiinfo", aliases=["ei"])
    async def emoji_info(self, ctx, emoji: discord.Emoji = None):
        if not emoji:
            return await ctx.invoke(self.bot.get_command("help"), entity="emojiinfo")

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
            colour=discord.Color.blurple(),
        )
        embed.set_thumbnail(url=emoji.url)
        await ctx.send(embed=embed)

    @commands.command(name="botinfo", aliases=["bi", "bot", "bot info"])
    async def info_bot(self, message):
        """
        This Command Provides us the info of the bot
        """
        pythonVersion = platform.python_version()
        dpyVersion = discord.__version__
        serverCount = len(self.bot.guilds)
        memberCount = len(set(self.bot.get_all_members()))
        mem1 = self.bot.get_user(854230635425693756)
        embed = discord.Embed(
            title=f"{mem1.name} Stats ",
            description="Aurora Bot is a [Open Source](https://github.com/HarshPatel5940/AuroraBot) project!! This is a multi-purpose bot which is easy to use",
            colour=discord.Color.blurple(),
            timestamp=datetime.utcnow(), )

        embed.add_field(name="Bot Version:", value=self.bot.version)
        embed.add_field(name="Python Version:", value=pythonVersion)
        embed.add_field(name="Discord.Py Version", value=dpyVersion)
        embed.add_field(name="Total Guilds:", value=serverCount)
        embed.add_field(name="Total Users:", value=memberCount)
        embed.add_field(name="Bot Made By:", value="<@448740493468106753>")

        embed.set_footer(text=f"{message.guild.name} | {self.bot.user.name}")
        embed.set_author(name=self.bot.user.name,
                         icon_url=self.bot.user.avatar.url)
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        await message.channel.send(embed=embed)

    @commands.command(name="userinfo", aliases=["ui", "memberinfo", "mi", "whois"])
    async def info_user(self, ctx, member: Optional[discord.Member]):
        """
        gets info of a user
        """
        member1 = member or ctx.author
        embed = discord.Embed(title="Member Information",
                              color=discord.Color.blurple(),
                              timestamp=datetime.utcnow())

        embed.add_field(name="ID", value=f"{member1.id}", inline=False)
        embed.add_field(
            name="Name", value=f"{member1.name}#{member1.discriminator}")
        embed.add_field(name="Top role", value=f"{member1.top_role.mention}")
        embed.add_field(name="status",
                        value=f"{str(member1.activity.type).split('.') if member1.activity else 'N/A'} {member1.activity.name if member1.activity else ''}")
        embed.add_field(
            name="created at", value=f"{member1.created_at.strftime('%d/%m/%y %H:%M:%S')}")
        embed.add_field(
            name="Joined at", value=f"{member1.joined_at.strftime('%d/%m/%y %H:%M:%S')}")
        embed.add_field(name="Boosted?", value=f"{member1.premium_since}")

        await ctx.reply(embed=embed)

    @commands.command(name="channelstats", aliases=["cs"])
    async def channel_stats(self, ctx, channel: discord.TextChannel = None):
        """
        This Command Provides us the stats of the channel
        """
        channel = channel or ctx.channel
        embed = discord.Embed(
            title=f"Stats for **{channel.name}**",
            description=f"{'Category: {}'.format(channel.category.name) if channel.category else 'This channel is not in a category'}",
            color=discord.Color.blurple(),
        )
        embed.add_field(name="Channel Guild",
                        value=ctx.guild.name, inline=False)
        embed.add_field(name="Channel Id", value=channel.id, inline=False)
        embed.add_field(
            name="Channel Topic",
            value=f"{channel.topic if channel.topic else 'No topic.'}",
            inline=False,
        )
        embed.add_field(name="Channel Position",
                        value=channel.position, inline=False)
        embed.add_field(
            name="Channel Slowmode Delay", value=channel.slowmode_delay, inline=False
        )
        embed.add_field(name="Channel is nsfw?",
                        value=channel.is_nsfw(), inline=False)
        embed.add_field(name="Channel is news?",
                        value=channel.is_news(), inline=False)
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

    @commands.command(name="serverinfo", aliases=["guildinfo", "si", "gi"])
    async def server_info(self, ctx):
        embed = discord.Embed(title="Server information",
                              color=discord.Color.blurple(),
                              timestamp=datetime.utcnow())

        embed.set_thumbnail(url=ctx.guild.icon.url)

        statuses = [len(list(filter(lambda m: str(m.status) == "online", ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status)
                        == "idle", ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == "dnd", ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == "offline", ctx.guild.members)))]

        fields = [("Owner & owner id", f"{ctx.guild.owner}, {ctx.guild.owner.id}", False),
                  ("Server ID", ctx.guild.id, True),
                  ("Created at", ctx.guild.created_at.strftime(
                      "%d/%m/%Y %H:%M:%S"), True),
                  ("Region", ctx.guild.region, True),
                  ("Members", len(ctx.guild.members), True),
                  ("Humans", len(list(filter(lambda m: not m.bot, ctx.guild.members))), True),
                  ("Bots", len(list(filter(lambda m: m.bot, ctx.guild.members))), True),
                  ("Banned members", len(await ctx.guild.bans()), True),
                  ("Statuses",
                   f"🟢 {statuses[0]} 🟠 {statuses[1]} 🔴 {statuses[2]} ⚪ {statuses[3]}", True),
                  ("Text channels", len(ctx.guild.text_channels), True),
                  ("Voice channels", len(ctx.guild.voice_channels), True),
                  ("Categories", len(ctx.guild.categories), True),
                  ("Roles", len(ctx.guild.roles), True),
                  ("Invites", len(await ctx.guild.invites()), True),
                  ("\u200b", "\u200b", True)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Stats(bot))
