import discord
from discord.ext import commands
from asyncio import sleep


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.command(aliases=["purge"])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=0):
        """
        This command is used to delete multiple messages 
        """
        if amount < 1:
            await ctx.message.delete()
            await ctx.send('Please provide any amount to delete messages.', delete_after=5)
        else:
            await ctx.message.delete()
            await ctx.channel.purge(limit=amount)
            await ctx.send(f'{amount} messages deleted successfully.', delete_after=5)

    @commands.command(name="sm")
    @commands.has_permissions(manage_roles=True)
    async def setdelay(self, ctx, seconds: int):
        """
        This command is used to add/remove slowmode in chat
        """

        await ctx.channel.edit(slowmode_delay=seconds, reason=f"{ctx.author} changed slowmode to {seconds}")
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

        if ctx.guild.default_role not in channel.overwrites:
            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(send_messages=False)
            }
            await channel.edit(overwrites=overwrites, reason=f"channel lock by {ctx.author}")
            await ctx.send(f"I have put {channel.name} on lockdown.")
        elif (
                channel.overwrites[ctx.guild.default_role].send_messages is True
                or channel.overwrites[ctx.guild.default_role].send_messages is None
        ):
            overwrites = channel.overwrites[ctx.guild.default_role]
            overwrites.send_messages = False
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites, reason=f"channel lock by {ctx.author}")
            await ctx.send(f"I have put {channel.mention} on lockdown.")
        else:
            overwrites = channel.overwrites[ctx.guild.default_role]
            overwrites.send_messages = None
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites, reason=f"channel unlock by {ctx.author}")
            await ctx.send(f"I have removed {channel.mention} from lockdown.")

    @commands.command(aliases=["m"])
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member = None, *, reason="no reason provided "):
        """
        This is a mute command which mutes the User
        """

        if member.mention == ctx.author.mention:
            await ctx.send('you cannot mute your self **DUMB**!', delete_after=10)
            return
        elif member.guild_permissions.administrator or member.guild_permissions.ban_members:
            await ctx.send(f":x: I CANT Moderate AN ADMINISTRATOR/ MOD  {ctx.author.mention} :x:", delete_after=10)
            return
        elif member.top_role >= ctx.author.top_role:
            await ctx.send(f"You can only moderate members below your role", delete_after=10)
            return

        role = discord.utils.get(ctx.guild.roles, name="Muted")
        if role == None:
            role = await ctx.guild.create_role(name='Muted ', reason="bot muted role")

        await member.add_roles(role, reason=f"Muted by:{ctx.author}, reason: {reason}")
        await ctx.send(f"**{member.name}#{member.discriminator} Has Been Muted**")
        channel = self.client.get_channel(863000643303374920)
        mute_msg = f"{member.mention} Has Been Muted By {ctx.author.name}#{ctx.author.discriminator} \n Reason : {reason}"
        await channel.send(mute_msg)

    @commands.command(aliases=["um"])
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member = None, *, reason="No reason provided"):
        """
        this command unmutes a member
        """

        if member.guild_permissions.administrator:
            await ctx.send(f":x: I CANT UNMUTE AN ADMINISTRATOR he is already unmuted {ctx.author.mention} :x:",
                           delete_after=10)
        else:
            role = discord.utils.get(ctx.guild.roles, name="Muted")
            await member.remove_roles(role, reason=f"Unmuted by:{ctx.author}, reason: {reason}")

            await ctx.send(f"**{member.display_name}#{member.discriminator} Has Been Unmuted**")
            channel = self.client.get_channel(863000643303374920)
            mute_msg = f"{member.mention} Has Been Unuted By {ctx.author.name}#{ctx.author.discriminator} \n Reason : {reason}"
            await channel.send(mute_msg)

    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(ban_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """
        this command Kicks a member
        """
        if member.mention == ctx.author.mention:
            await ctx.send(f"you cannot kick your self dumb", delete_after=10)
        elif member.guild_permissions.administrator or member.guild_permissions.ban_members:
            await ctx.send(f":x: I CANT Moderate AN ADMINISTRATOR/ MOD  {ctx.author.mention} :x:", delete_after=10)
            return
        elif member.top_role >= ctx.author.top_role:
            await ctx.send(f"You can only moderate members below your role", delete_after=10)
            return

        await ctx.guild.kick(user=member, reason=f"kick by:{ctx.author}, reason: {reason}")
        embed = discord.Embed(
            title=f"{ctx.author.name} kicked: {member.name}", description=reason
        )
        log_channel = self.client.get_channel(863000643303374920)
        await log_channel.send(embed=embed)
        await ctx.send(f"**{member.name} Has Been Kicked!**")

    @commands.command()
    @commands.has_guild_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """
        A command which bans a given user
        """
        if member.mention == ctx.author.mention:
            await ctx.send(f"you cannot Ban your self dumb", delete_after=10)

        elif member.guild_permissions.administrator or member.guild_permissions.ban_members:
            await ctx.send(f":x: I CANT Moderate AN ADMINISTRATOR/ MOD  {ctx.author.mention} :x:", delete_after=10)
            return
        elif member.top_role >= ctx.author.top_role:
            await ctx.send(f"You can only moderate members below your role", delete_after=10)
            return

        await ctx.guild.ban(user=member, reason=f"Muted by:{ctx.author}, reason: {reason}")

        embed = discord.Embed(
            title=f"{ctx.author.name} banned: {member.name}", description=reason
        )
        log_channel = self.client.get_channel(863000643303374920)
        await log_channel.send(embed=embed)
        await ctx.send(f"**{member.name}** Has Been Banned!")

    @commands.command(name='unban', aliases=['ub'], description="Unbans a given user from the server")
    @commands.check_any(commands.is_owner(), commands.has_permissions(ban_members=True))
    async def _unban(self, ctx, member: discord.User = None, *, reason=None):
        if reason is None:
            reason = f"Unbanned by {ctx.author}"
        else:
            reason = f"Unbanned by {ctx.author}, with reason:- {reason}"

        bandec = f"Name:- {member} \nID:- {member.id} \nResponsible Moderator:- {ctx.author}"
        embed = discord.Embed(title="Unban Case", description=bandec)

        await ctx.guild.unban(member, reason=f"Unban by:{ctx.author} , for {reason}")
        log_channel = self.client.get_channel(863000643303374920)
        await log_channel.send(embed=embed)
        await sleep(1)
        await ctx.send(f"**{member.name}** Has Been Unbanned!")


def setup(client):
    client.add_cog(Moderation(client))
