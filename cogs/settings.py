import io
import textwrap
import traceback
from contextlib import redirect_stdout
from lib.db import db
import discord
from discord.ext import commands
from datetime import datetime as dt


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
        self._last_result = None

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")
        await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,
                                                                    name='PunisherYT'))

    @commands.command(name="prefix")
    @commands.has_permissions(manage_guild=True)
    async def change_prefix(self, ctx, new: str):
        if len(new) > 5:
            await ctx.send("The prefix can not be more than 5 characters in length.")

        else:
            db.execute("UPDATE guilds SET Prefix = ? WHERE GuildID = ?", new, ctx.guild.id)
            await ctx.send(f"Prefix set to {new}.")

    @change_prefix.error
    async def change_prefix_error(self, ctx, exc):
        if isinstance(exc, commands.CheckFailure):
            await ctx.send("You need the Manage Server permission to do that.")

    @staticmethod
    def cleanup_code(content):
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        # remove `foo`
        return content.strip('` \n')

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, cog):
        """
        This Command Is used to Reload all cogs
        """
        if cog == 'all':
            embed = discord.Embed(title='Reloading Cogs...', description='', color=discord.Color.teal())
            extensions = [
                "cogs.help",
                "cogs.moderation",
                "cogs.other",
                "cogs.settings",
                "cogs.stats",
                "cogs.events",
                "cogs.invites",
                "cogs.automod"
            ]
            for i in extensions:
                self.client.reload_extension(i)
                embed.description += f"{i} reloaded successfully.\n"
            await ctx.send(embed=embed)
            return
        self.client.reload_extension(f"cogs.{cog}")

        await ctx.send(f"{cog} reloaded successfully.")

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, cog):
        """
        This command is Used to UnLoad a cog
        """
        self.client.load_extension(f"cogs.{cog}")
        await ctx.send(f"{cog} unloaded successfully.")

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, cog):
        """
        This command is Used to UnLoad a cog
        """
        self.client.unload_extension(f"cogs.{cog}")
        await ctx.send(f"{cog} unloaded successfully.")

    @commands.command()
    @commands.is_owner()
    async def eval(self, ctx, *, code: str):
        """Evaluate a code block"""
        env = {
            'client': self.client,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            'command': ctx.command,
            'datetime': dt,
            '_': self._last_result
        }

        env.update(globals())

        body = self.cleanup_code(code)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.reply(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.reply(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2705')
            except:
                pass

            if ret is None:
                if value:
                    await ctx.reply(f'```py\n{value}\n```')
            else:
                self._last_result = ret
                await ctx.reply(f'```py\n{value}{ret}\n```')


def setup(client):
    client.add_cog(BotSettings(client))
