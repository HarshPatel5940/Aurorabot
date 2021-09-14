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
    await message.reply(
        f"{exception}\nCorrect Usage: ```\n{message.prefix}{message.command.qualified_name} {message.command.signature}\n```")
    raise exception


class BotSettings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild = self.bot.get_guild(799974967504535572)
        self._last_result = None

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,
                                                                    name='PunisherYT'))

    @commands.command(name="prefix")
    @commands.has_permissions(administrator=True)
    async def change_prefix(self, ctx, new: str):
        if len(new) > 5:
            await ctx.send("The prefix can not be more than 5 characters in length.")

        else:
            await self.bot.db.execute("UPDATE guild SET prefix = $1 WHERE server_id = $2", new, ctx.guild.id)
            self.bot.prefix[ctx.guild.id] = new
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
                self.bot.reload_extension(i)
                embed.description += f"{i} reloaded successfully.\n"
            await ctx.send(embed=embed)
            return
        self.bot.reload_extension(f"cogs.{cog}")

        await ctx.send(f"{cog} reloaded successfully.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def load(self, ctx, cog):
        """
        This command is Used to UnLoad a cog
        """
        self.bot.load_extension(f"cogs.{cog}")
        await ctx.send(f"{cog} unloaded successfully.")

    @commands.command(hidden=True)
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

    @commands.command(hidden=True)
    async def sql(self, ctx, *, query: str):
        """Run some SQL."""

        # the imports are here because I imagine some people would want to use
        # this cog as a base for their other cog, and since this one is kinda
        # odd and unnecessary for most people, I will make it easy to remove
        # for those people.
        class plural:
            def __init__(self, value):
                self.value = value

            def __format__(self, format_spec):
                v = self.value
                singular, sep, plural = format_spec.partition('|')
                plural = plural or f'{singular}s'
                if abs(v) != 1:
                    return f'{v} {plural}'
                return f'{v} {singular}'

        class TabularData:
            def __init__(self):
                self._widths = []
                self._columns = []
                self._rows = []

            def set_columns(self, columns):
                self._columns = columns
                self._widths = [len(c) + 2 for c in columns]

            def add_row(self, row):
                rows = [str(r) for r in row]
                self._rows.append(rows)
                for index, element in enumerate(rows):
                    width = len(element) + 2
                    if width > self._widths[index]:
                        self._widths[index] = width

            def add_rows(self, rows):
                for row in rows:
                    self.add_row(row)

            def render(self):
                """Renders a table in rST format.
                Example:
                +-------+-----+
                | Name  | Age |
                +-------+-----+
                | Alice | 24  |
                |  Bob  | 19  |
                +-------+-----+
                """

                sep = '+'.join('-' * w for w in self._widths)
                sep = f'+{sep}+'

                to_draw = [sep]

                def get_entry(d):
                    elem = '|'.join(f'{e:^{self._widths[i]}}' for i, e in enumerate(d))
                    return f'|{elem}|'

                to_draw.append(get_entry(self._columns))
                to_draw.append(sep)

                for row in self._rows:
                    to_draw.append(get_entry(row))

                to_draw.append(sep)
                return '\n'.join(to_draw)

        import time

        query = self.cleanup_code(query)

        is_multistatement = query.count(';') > 1
        if is_multistatement:
            # fetch does not support multiple statements
            strategy = self.bot.db.execute
        else:
            strategy = self.bot.db.fetch

        try:
            start = time.perf_counter()
            results = await strategy(query)
            dt = (time.perf_counter() - start) * 1000.0
        except Exception:
            return await ctx.send(f'```py\n{traceback.format_exc()}\n```')

        rows = len(results)
        if is_multistatement or rows == 0:
            return await ctx.send(f'`{dt:.2f}ms: {results}`')

        headers = list(results[0].keys())
        table = TabularData()
        table.set_columns(headers)
        table.add_rows(list(r.values()) for r in results)
        render = table.render()

        fmt = f'```\n{render}\n```\n*Returned {plural(rows):row} in {dt:.2f}ms*'
        if len(fmt) > 2000:
            fp = io.BytesIO(fmt.encode('utf-8'))
            await ctx.send('Too many results...', file=discord.File(fp, 'results.txt'))
        else:
            await ctx.send(fmt)


def setup(bot):
    bot.add_cog(BotSettings(bot))
