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
        embed = discord.Embed(
            title=f"Welcome To FRNz Official Server.",
            description=f"**Member :** {member.mention}\n **Invited by: {inviter.name}#{inviter.discriminator}**",
            color=0x14a00f,
            timestamp=datetime.now(self.IST)
        )
        embed.set_thumbnail(url=member.avatar.url)
        embed.set_author(name=member.name, icon_url=member.avatar.url)
        embed.set_footer(text=member.guild.name, icon_url=member.guild.icon.url)

        await member.send(f"Hi {member.mention} Welcome to our FRNz Official community.\n<a:Heart:815506676533690390>You can promote your channel, videos  or blog in <#800291409726144513>\n<a:Heart:815506676533690390>Remember to Read Rules in <#799978440492449842>\n<a:Heart:815506676533690390>Take Self roles in <#799978698064265226>\n\n<a:Heart:815506676533690390>Have a great time here in {guild.name}.")
        await asyncio.sleep(1)
        await channel.send(embed=embed)

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
