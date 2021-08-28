import asyncio
import discord
from discord.ext import commands
import typing


async def on_command_error(message, exception):
    if isinstance(exception, commands.CommandNotFound) or isinstance(exception, commands.NotOwner) or isinstance(message.channel, discord.DMChannel):
        return
    await message.reply(
        f"{exception}\nCorrect Usage: ```\n{message.prefix}{message.command.qualified_name} {message.command.signature}\n```")
    raise exception  # this is basic error handling.. it'll send the runtime errors simply


class BotSettings(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.guild = self.client.get_guild(799974967504535572)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @staticmethod
    def cleanup_code(content):
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        # remove `foo`
        return content.strip('` \n')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def reload(self, ctx, cog):
        """
        This Command Is used to Reload all cogs
        """
        if cog == 'all':
            embed = discord.Embed(title='Reloading Cogs...', description='', color=discord.Color.green())
            extensions = [
                "cogs.events",
                "cogs.moderation",
                'cogs.giveaway',
                "cogs.settings",
                "cogs.invites",
                "cogs.automod",
                "cogs.stats",
                "cogs.help"
            ]
            for i in extensions:
                self.client.reload_extension(i)
                embed.description += f"{i} reloaded successfully.\n"
            await ctx.send(embed=embed)
            return
        self.client.reload_extension(f"cogs.{cog}")

        await ctx.send(f"{cog} reloaded successfully.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def load(self, ctx, cog):
        """
        This command is Used to UnLoad a cog
        """
        self.client.load_extension(f"cogs.{cog}")
        await ctx.send(f"{cog} unloaded successfully.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def unload(self, ctx, cog):
        """
        This command is Used to UnLoad a cog
        """
        self.client.unload_extension(f"cogs.{cog}")
        await ctx.send(f"{cog} unloaded successfully.")

    @commands.command()
    async def suggest(self, ctx, *, message):
        """
        This is command is used to send a suggestion in the suggestion channel
        """
        message1 = message
        emb=discord.Embed(title=f"Suggest from {ctx.author.name}#{ctx.author.discriminator}", description=f"Suggester: {ctx.author.mention} \nsuggestion : {message1}",color=0xff9200)
        channel = self.client.get_channel(799980922518372402)

        await ctx.message.delete()
        msg=await channel.send(embed=emb)
        await msg.add_reaction('👍')
        await msg.add_reaction('👎')
        await asyncio.sleep(1)
        await ctx.send(f"{ctx.author.mention} Suggestion sent!")

    @commands.command()
    @commands.check_any(commands.is_owner(), commands.has_permissions(administrator=True))
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


def setup(client):
    client.add_cog(BotSettings(client))
