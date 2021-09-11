import datetime
import time
import discord
from discord.ext import commands


class BotInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.help_command.cog = self

    @commands.command(aliases=["pong"])
    async def ping(self, ctx):
        """
        This command is used to calculate latency of bot.
        """
        embed = discord.Embed(title="Bot Status",
                              description=f"Pong! :ping_pong: \nResponse Time: {round(self.bot.latency * 1000)}ms",
                              color=discord.Color.blurple())

        await ctx.reply(embed=embed)

    @commands.command()
    async def uptime(self, message):
        current_time = time.time()
        difference = int(round(current_time - self.bot.start_time))
        text = str(datetime.timedelta(seconds=difference))
        embed = discord.Embed(colour=discord.Color.green())
        embed.add_field(name="Uptime", value=text)
        embed.set_footer(text="FRNz Aurora Uptime")
        try:
            await message.reply(embed=embed)
        except discord.HTTPException:
            await message.send("Current uptime: " + text)


def setup(bot):
    bot.add_cog(BotInfo(bot=bot))


class HelpCommand(commands.DefaultHelpCommand):
    def __init__(self):
        super().__init__(command_attrs={"help": "Shows this message",
                                        "aliases": ["commands"]})

    async def send(self, **kwargs):
        await self.get_destination().send(**kwargs)

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title=f"{self.context.me.name} Help", description="", color=discord.Color.blurple(),
                              timestamp=datetime.datetime.utcnow())
        for cog, command in mapping.items():
            filtered = await self.filter_commands(commands=command)
            cog_name = getattr(cog, 'qualified_name', "No Category")
            cog_desc = getattr(cog, 'description', "")
            if cog_name not in ["Invites", "Events", "Automod"]:
                embed.add_field(name=f"{cog_name} [{len(cog.get_commands() if cog else '.')}]",
                                value=f"{cog_desc}\n`{'`  `'.join([i.name for i in filtered])}`")
        embed.set_footer(text=f"See {self.context.prefix}help [command] for more info",
                         icon_url=self.context.me.avatar.url)
        await self.send(embed=embed)

    async def send_command_help(self, command):
        if command.hidden:
            return
        embed = discord.Embed(title=command.qualified_name, description=command.help,
                              color=discord.Color.blurple(), timestamp=datetime.datetime.utcnow())
        embed.add_field(name='Usage',
                        value=f"**{self.context.prefix}{command.name} {command.signature}**\n{command.brief if command.brief is not None else ''}")
        if command.aliases != []:
            embed.add_field(name='Aliases', value=f"```\n{', '.join(command.aliases)}\n```", inline=False)
        embed.set_footer(text="[] - optional, <> - required")
        await self.send(embed=embed)

    async def send_cog_help(self, cog):
        pass

    async def send_group_help(self, group):
        pass