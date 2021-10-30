from datetime import datetime

import discord
import pytz
from discord.ext import commands


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.IST = pytz.timezone('Asia/Kolkata')

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.Cog.listener()
    async def on_message(self, message):
        # ignore yourself
        if message.author.id == self.bot.user.id:
            return
        if not message.guild:
            # await message.reply(
            #     "<a:Red_alert:863017113581256715> **For Any Assistance create ticket in <#861641048224038963>** <a:Red_alert:863017113581256715>")
            # await message.channel.send("If Urgent ping any staff in ticket")
            return

        if message.content == f"<@!{self.bot.user.id}>":
            await message.reply(f"My Prefix is `{self.bot.prefix[message.guild.id]}`, try running `>help`")

        elif message.content.lower() == "hi":
            await message.reply(f"Hey buddy! Wat's Up?")

    @commands.Cog.listener()
    async def on_command_error(self, message, exception):
        if isinstance(exception, commands.CommandNotFound) or isinstance(exception, commands.NotOwner) or isinstance(message.channel, discord.DMChannel):
            return
        if isinstance(exception, commands.DisabledCommand):
            await message.channel.send(f"{message.command.qualified_name} is Disabled!!!")
            return
        if isinstance(exception, commands.errors.MemberNotFound):
            await message.channel.send(f"No Member Found")
            return
        if isinstance(exception, commands.MissingPermissions):
            await message.channel.send(f"{message.author.mention} You Lack Permissions !!")
            return
        if isinstance(exception, commands.BotMissingPermissions):
            await message.channel.send(f"Bot is Lack Permissions !!")
            return
        if isinstance(exception, commands.MissingRequiredArgument):
            await message.reply(f"You are missing {exception.param.name}\nCorrect Usage: ```\n{message.prefix}{message.command.qualified_name} {message.command.signature}\n```")
            return
        await message.reply(f"{exception}")
        raise exception  # help for error handling

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        self.bot.prefix[guild.id] = ">"
        # await self.bot.db.execute("INSERT INTO guild")

        embed1 = discord.Embed(title="Joined New Guild", colour=discord.Color.green(
        ), timestamp=datetime.now(self.IST))
        embed1.add_field(name="Server Details",
                         value=f"Name {guild.name}\nId {guild.id}")
        embed1.add_field(name="Member count",
                         value=f"{len(guild.members)}")
        embed1.set_thumbnail(url=guild.icon.url)

        channel = self.bot.get_channel(896301418955276338)
        await channel.send(embed=embed1)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        del self.bot.prefix[guild.id]
        embed1 = discord.Embed(title="Left A Guild", colour=discord.Color.green(
        ), timestamp=datetime.now(self.IST))
        embed1.add_field(name="Server Details",
                         value=f"Name {guild.name}\nId {guild.id}")
        embed1.add_field(name="Member count",
                         value=f"{len(guild.members)}")
        embed1.set_thumbnail(url=guild.icon.url)

        channel = self.bot.get_channel(896301418955276338)
        await channel.send(embed=embed1)

    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        if before.name != after.name:
            embed = discord.Embed(title=f"Username change",
                                  colour=discord.Color.magenta(),
                                  timestamp=datetime.now(self.IST))
            embed.add_field(name="Member name & id  :",
                            value=f"{before.name} ({before.id})")
            fields = [("Before", before.name, False),
                      ("After", after.name, False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            log_channel = self.bot.get_channel(863000479889096724)
            await log_channel.send(embed=embed)

        if before.discriminator != after.discriminator:
            embed = discord.Embed(title=f"Discriminator change",
                                  colour=discord.Color.magenta(),
                                  timestamp=datetime.now(self.IST))
            embed.add_field(name="Member name & id  :",
                            value=f"{before.name} ({before.id})")
            fields = [("Before", before.discriminator, False),
                      ("After", after.discriminator, False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            log_channel = self.bot.get_channel(863000479889096724)
            await log_channel.send(embed=embed)

        if before.avatar.url != after.avatar.url:
            embed = discord.Embed(title=f"Avatar change",
                                  description="New image is below, old to the thumbnail.",
                                  colour=discord.Color.magenta(),
                                  timestamp=datetime.now(self.IST))
            embed.add_field(name="Member name & id  :",
                            value=f"{before.name} ({before.id})")
            embed.set_thumbnail(url=before.avatar.url)
            embed.set_image(url=after.avatar.url)
            log_channel = self.bot.get_channel(863000479889096724)
            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.display_name != after.display_name:
            embed = discord.Embed(title=f"Nickname change",
                                  colour=discord.Color.magenta(),
                                  timestamp=datetime.now(self.IST))
            embed.add_field(name="Member name & id  :",
                            value=f"{before.name} ({before.id})")
            fields = [("Before", before.display_name, False),
                      ("After", after.display_name, False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            log_channel = self.bot.get_channel(863000479889096724)
            await log_channel.send(embed=embed)

        elif before.roles != after.roles:
            embed = discord.Embed(title=f"Role updates",
                                  colour=discord.Color.magenta(),
                                  timestamp=datetime.now(self.IST))
            embed.add_field(name="Member name & id  :",
                            value=f"{before.name} ({before.id})")
            fields = [("Before", ", ".join([r.mention for r in before.roles]), False),
                      ("After", ", ".join([r.mention for r in after.roles]), False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            log_channel = self.bot.get_channel(863000479889096724)
            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.content != after.content:
            embed = discord.Embed(title="Message edit",
                                  description=f"Sent by {after.author.name} , id = {after.author.id}",
                                  colour=discord.Color.orange(),
                                  timestamp=datetime.now(self.IST))
            fields = [("Before", before.content, False),
                      ("After", after.content, False)]
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            embed.add_field(name="Message link",
                            value=f"[click here]({after.jump_url})")
            log_channel = self.bot.get_channel(863000479889096724)
            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if not message.author.bot:
            embed = discord.Embed(title="Message deletion",
                                  description=f"Sent by {message.author.name} , id = {message.author.id}",
                                  colour=discord.Color.orange(),
                                  timestamp=datetime.now(self.IST))
            embed.add_field(name="Message Content",
                            value=f"{message.channel.mention}: {message.content}")
            log_channel = self.bot.get_channel(863000479889096724)
            await log_channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Events(bot))
