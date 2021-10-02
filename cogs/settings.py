import io
import textwrap
import traceback
from contextlib import redirect_stdout
from datetime import datetime as dt

import discord
from discord.ext import commands


async def on_command_error(message, exception):
    if isinstance(exception, commands.CommandNotFound) or isinstance(exception, commands.NotOwner) or isinstance(message.channel, discord.DMChannel): 
        return
    if isinstance(exception, commands.MissingPermissions):
        message.channel.send(f"{message.author.mention} You Lack Permissions !!") 
        return
    if isinstance(exception, commands.BotMissingPermissions):
        message.channel.send(f"Bot is Lack Permissions !!") 
        return
    if isinstance(exception, commands.MissingRequiredArgument): #Comparing the error to commands.MissingRequiredArgument
        await ctx.send(f"You are missing {exception.param.name}")
    await message.reply(
        f"{exception}\nCorrect Usage: ```\n{message.prefix}{message.command.qualified_name} {message.command.signature}\n```")
    raise exception


class BotSettings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.command(name="prefix")
    @commands.has_permissions(administrator=True)
    async def change_prefix(self, ctx, new: str):
        if len(new) > 5:
            await ctx.send("The prefix can not be more than 5 characters in length.")

        else:
            await self.bot.db.execute("UPDATE guild SET prefix = $1 WHERE server_id = $2", new, ctx.guild.id)
            self.bot.prefix[ctx.guild.id] = new
            await ctx.send(f"Prefix set to {new}.")


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
                "cogs.automod",
                "cogs.clan"
            ]
            for i in extensions:
                self.bot.reload_extension(i)
                embed.description += f"{i} reloaded successfully.\n"
            await ctx.send(embed=embed)
            return
        self.bot.reload_extension(f"cogs.{cog}")

        await ctx.send(f"{cog} reloaded successfully.")

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, cog):
        """
        This command is Used to UnLoad a cog
        """
        self.bot.load_extension(f"cogs.{cog}")
        await ctx.send(f"{cog} loaded successfully.")

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, cog):
        """
        This command is Used to UnLoad a cog
        """
        self.bot.unload_extension(f"cogs.{cog}")
        await ctx.send(f"{cog} unloaded successfully.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def eval(self, ctx, *, code: str):
        """Evaluate a code block"""
        env = {
            'bot': self.bot,
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


def setup(bot):
    bot.add_cog(BotSettings(bot))
