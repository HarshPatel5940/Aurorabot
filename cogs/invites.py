import asyncio
import discord
import DiscordUtils
from discord.ext import commands
from datetime import datetime
import pytz


class Invites(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.IST = pytz.timezone('Asia/Kolkata')
        self.tracker = DiscordUtils.InviteTracker(bot)

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
        inviter = await self.tracker.fetch_inviter(member)
        general = self.bot.get_channel(799974968921292812)
        channel = self.bot.get_channel(799978267293646868)
        guild = self.bot.get_guild(799974967504535572)
        desc = f"**Member :** {member.mention}"

        if inviter is None:
            desc = f"**Member :** {member.mention}\n **Invited by: Inviter not found**"
        else:
            desc = f"**Member :** {member.mention}\n **Invited by: {inviter.name}#{inviter.discriminator}**"

        embed1 = discord.Embed(
            title=f"Welcome To FRNz Official Server.",
            description=desc,
            color=discord.Color.green(),
            timestamp=datetime.now(self.IST)
        )
        embed1.add_field(
            f"account creation : {member1.created_at.strftime('%d/%m/%y %H:%M:%S')}")
        embed1.set_thumbnail(url=member.avatar.url)
        embed1.set_author(name=member.name, icon_url=member.avatar.url)
        embed1.set_footer(text=member.guild.name,
                          icon_url=member.guild.icon.url)

        x1 = f"{member.mention} Welcome to our FRNz Official community"
        x3 = f"{member.mention} Welcome to our FRNz Official community.\n since Dms off sent here"
        x2 = f"""
<a:Heart:815506676533690390>You can promote your channel, videos  or blog in <#800291409726144513>
<a:Heart:815506676533690390>Remember to Read Rules in <#799978440492449842>
<a:Heart:815506676533690390>Take Self roles in <#799978698064265226>
<a:Heart:815506676533690390>Have a great time here in {guild.name} """
        embed2 = discord.Embed(
            title="Welcome To FRNz Official Server",
            description=x2,
            color=discord.Color.green(),
            timestamp=datetime.now(self.IST)
        )
        embed2.set_thumbnail(url=member.guild.icon.url)
        embed2.set_author(name=member.name, icon_url=member.avatar.url)
        embed2.set_footer(text=member.guild.name,
                          icon_url=member.guild.icon.url)
        try:
            await member.send(x1, embed=embed2)
        except:
            await general.send(x3, embed=embed2)
        await asyncio.sleep(1)
        await channel.send(embed=embed1)

    @commands.Cog.listener()
    async def on_member_remove(self, member):

        channel = self.bot.get_channel(799978817459453963)

        embed = discord.Embed(
            title="A Member Just Left :( ",
            description="Goodbye from all of us..",
            color=discord.Color.red(),
            timestamp=datetime.now(self.IST)
        )
        embed.set_thumbnail(url=member.avatar.url)
        embed.set_author(name=member.name, icon_url=member.avatar.url)
        embed.set_footer(text=member.guild.name,
                         icon_url=member.guild.icon.url)
        await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Invites(bot))
