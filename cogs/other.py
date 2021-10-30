import typing
import asyncio
import discord
from discord.ext import commands


class Others(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    class nitroButtons(discord.ui.View):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.value: str = None

        @discord.ui.button(label="⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀Claim⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀", style=discord.ButtonStyle.success)
        async def nitroButton(self, button: discord.ui.Button, interaction: discord.Interaction):

            await interaction.response.send_message(content="Oh no it was a fake", ephemeral=True)
            await asyncio.sleep(2)
            await interaction.edit_original_message(content="Prepare to get rickrolled...(it's a good song anyway)")
            await asyncio.sleep(2)
            await interaction.edit_original_message(content="https://i.imgur.com/NQinKJB.gif")

            button.disabled = True
            button.style = discord.ButtonStyle.secondary
            button.label = "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀Claimed⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀"

            embed = discord.Embed(title="You received a gift, but...",
                                  description="The gift link has either expired or has been\nrevoked.", color=3092790)
            embed.set_thumbnail(url="https://i.imgur.com/w9aiD6F.png")

            await interaction.message.edit(view=self, embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.command(brief="based on pog bot's nitro command")
    async def nitro(self, ctx):
        """
        Fun Nitro Command
        """
        embed = discord.Embed(title="You've been gifted a subscription!",
                              description="You've been gifted Nitro for **1 month!**\nExpires in **24 hours**", color=3092790)
        embed.set_thumbnail(url="https://i.imgur.com/w9aiD6F.png")

        view = self.nitroButtons(timeout=180.0)
        await ctx.send(embed=embed, view=view)

    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(manage_messages=True)
    @commands.bot_has_guild_permissions(manage_messages=True)
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
    @commands.guild_only()
    @commands.has_guild_permissions(manage_roles=True, manage_messages=True)
    async def embed(self, ctx, channel: typing.Optional[discord.TextChannel] = None, *, message):
        """
        This Command is used to send a Embed Through Bot in a channel
        """
        channel = channel or ctx.channel
        embed = discord.Embed(description=message, color=discord.Color.teal())
        await channel.send(embed=embed)
        await ctx.message.add_reaction("✅")

    @commands.command(name="editemb")
    @commands.guild_only()
    @commands.has_guild_permissions(manage_messages=True)
    async def edit_embed(self, ctx, channel: discord.TextChannel, id_: int, *, message):
        """
        This Command is used to Edit Exsisting Embed
        """
        msg1 = 0
        try:
            msg1 = await channel.fetch_message(id_)
        except:
            await ctx.send("The channel or ID mentioned was incorrect")

        new_embed = discord.Embed(
            description=message, color=discord.Color.teal())
        await msg1.edit(embed=new_embed)
        await ctx.message.add_reaction("✅")

    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(manage_messages=True)
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
    @commands.guild_only()
    @commands.has_guild_permissions(manage_messages=True)
    async def dm_embed(self, ctx, user: discord.Member, *, message):
        """
        This Command is used to send a Embed Through Bot in a channel
        """
        embed = discord.Embed(description=message, color=discord.Color.teal())
        await user.send(embed=embed)
        await ctx.message.add_reaction("✅")


    @commands.command(
        name="test",
        description="This a test cmd")
    async def blast(self, ctx):
        embed = discord.Embed(
            title="Please tell me what you want me to repeat!",
            description="||This request will timeout after 1 minute.||",
        )
        sent = await ctx.send(embed=embed)

        try:
            msg = await self.bot.wait_for(
                "message",
                timeout=60,
                check=lambda message: message.author == ctx.author
                and message.channel == ctx.channel,
            )
            if msg:
                await sent.delete()
                await msg.delete()
                await ctx.send(msg.content)
        except asyncio.TimeoutError:
            await sent.delete()
            await ctx.send("Cancelling", delete_after=10)
    

def setup(bot):
    bot.add_cog(Others(bot))
