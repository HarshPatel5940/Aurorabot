import asyncio
import discord
import DiscordUtils
from discord.ext import commands
from datetime import datetime
import pytz


class Invites(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.IST = pytz.timezone('Asia/Kolkata')
        self.tracker = DiscordUtils.InviteTracker(client)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.tracker.cache_invites()

    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        await self.tracker.update_invite_cache(invite)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        await self.tracker.update_guild_cache(guild)

    @commands.Cog.listener()
    async def on_invite_delete(self, invite):
        await self.tracker.remove_invite_cache(invite)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        await self.tracker.remove_guild_cache(guild)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        inviter = await self.tracker.fetch_inviter(member)  # inviter is the member who invited

        if inviter is None:
            inviter.name = "Inviter Not Found"
            inviter.discriminator = " Link deleted "

        channel = self.client.get_channel(799978267293646868)
        guild = self.client.get_guild(799974967504535572)
        embed1 = discord.Embed(
            title=f"Welcome To FRNz Official Server.",
            description=f"**Member :** {member.mention}\n **Invited by: {inviter.name}#{inviter.discriminator}**",
            color=0x14a00f,
            timestamp=datetime.now(self.IST)
        )
        embed1.set_thumbnail(url=member.avatar.url)
        embed1.set_author(name=member.name, icon_url=member.avatar.url)
        embed1.set_footer(text=member.guild.name, icon_url=member.guild.icon.url)
        x1 = f"{member.mention} Welcome to our FRNz Official community"
        x2 = f"""
<a:Heart:815506676533690390>You can promote your channel, videos  or blog in <#800291409726144513>
<a:Heart:815506676533690390>Remember to Read Rules in <#799978440492449842>
<a:Heart:815506676533690390>Take Self roles in <#799978698064265226>
<a:Heart:815506676533690390>Have a great time here in {guild.name} """
        embed2 = discord.Embed(
            title="Welcome To FRNz Official Server",
            description=x2,
            color=0x17ffd9,
            timestamp=datetime.now(self.IST)
        )
        embed2.set_thumbnail(url=member.guild.icon.url)
        embed2.set_author(name=member.name, icon_url=member.avatar.url)
        embed2.set_footer(text=member.guild.name, icon_url=member.guild.icon.url)

        await member.send(x1, embed=embed2)
        await asyncio.sleep(1)
        await channel.send(embed=embed1)

    @commands.Cog.listener()
    async def on_member_remove(self, member):

        channel = self.client.get_channel(799978817459453963)

        embed = discord.Embed(
            title="A Member Just Left :( ",
            description="Goodbye from all of us..",
            color=0xE74C3C,
            timestamp=datetime.now(self.IST)          
        )
        embed.set_thumbnail(url=member.avatar.url)
        embed.set_author(name=member.name, icon_url=member.avatar.url)
        embed.set_footer(text=member.guild.name, icon_url=member.guild.icon.url)
        await channel.send(embed=embed)


def setup(client):
    client.add_cog(Invites(client))
