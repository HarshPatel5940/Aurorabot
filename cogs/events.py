from datetime import datetime
import asyncio
import pytz
import discord
from discord.ext import commands


class Events(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.IST = pytz.timezone('Asia/Kolkata')

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.Cog.listener()
    async def on_message(self, message):
        # ignore yourself
        if message.author.id == self.client.user.id:
            return
        if not message.guild:

            if len(message.content) < 20:
                await message.channel.send(
                    "Your message should be at least 20 characters in length to be sent to Staff.")
                return
            else:
                embed = discord.Embed(
                    title=f"Modmail For {message.author.display_name}#{message.author.discriminator}",
                    description=f"{message.content}",
                    color=0x00ff00,
                    timestamp=datetime.now(self.IST)
                )
                embed.add_field(name=f"reply with `>dm {message.author.id}", value="Reply to ur member", inline=False)

                embed.set_thumbnail(url=message.author.avatar_url)

                log_channel = self.client.get_channel(863000430203895808)
                await log_channel.send(embed=embed)

                embed2 = discord.Embed(
                    title="Message Has Been Sent ",
                    description="<a:Red_alert:835058393475448833> Message Has Been Sent to Staff Succesfully<a:Red_alert:835058393475448833>\nStaff Will Contact You as soon as possible\nreplying to this message or sending message will create a new ticket\n\n**If you need to send a image or attachment pls send the link of attachment with the message**",
                    color=0x00ff00,
                    timestamp=datetime.now(self.IST)
                )
                embed2.set_footer(text="Brawl Family Management Team")
                embed2.set_thumbnail(
                    url="https://cdn.discordapp.com/icons/483087746332622851/436d76d81824a558077d0c8811c12b27.png")
                await asyncio.sleep(1)
                await message.channel.send(embed=embed2)
                return
        else:
            pass
        if message.content.lower() == "help commands":
            await message.channel.send(f"Hey! why don't you run the help command `>help`")

        elif message.content.lower() == "hi":
            await message.channel.send(f"Hey {message.author.mention} Wat's Up?")

        elif message.content.lower() == "hmm":
            await message.channel.send("I Wonder why he is Hmming")

    @commands.Cog.listener()
    async def on_command_error(self, message, error):
        ignored = (commands.CommandNotFound, commands.UserInputError)
        if isinstance(error, ignored):
            return

        if isinstance(error, commands.CheckFailure):
            await message.channel.send(f"Hey! {message.author.mention} you lack on permisions")
            return

        if isinstance(error, commands.CommandOnCooldown):
            msg = "**Command is still in Cooldown**, pls try again in {:.2f}s".format(error.retry_after)
            await message.channel.send(msg)
            return

    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        if before.name != after.name:
            embed = discord.Embed(title=f"Username change",
                                  colour=after.colour,
                                  timestamp=datetime.now(self.IST))
            embed.add_field(name="Member Id :", value=f"{before.id}")
            fields = [("Before", before.name, False),
                      ("After", after.name, False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            log_channel = self.client.get_channel(863000479889096724)
            await log_channel.send(embed=embed)

        if before.discriminator != after.discriminator:
            embed = discord.Embed(title=f"Discriminator change",
                                  colour=after.colour,
                                  timestamp=datetime.now(self.IST))
            embed.add_field(name="Member Id :", value=f"{before.id}")
            fields = [("Before", before.discriminator, False),
                      ("After", after.discriminator, False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            log_channel = self.client.get_channel(863000479889096724)
            await log_channel.send(embed=embed)

        if before.avatar.url != after.avatar.url:
            embed = discord.Embed(title=f"Avatar change",
                                  description="New image is below, old to the thumbnail.",
                                  colour=after.colour,
                                  timestamp=datetime.now(self.IST))
            embed.add_field(name="Member Id :", value=f"{before.id}")
            embed.set_thumbnail(url=before.avatar.url)
            embed.set_image(url=after.avatar.url)
            log_channel = self.client.get_channel(863000479889096724)
            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.display_name != after.display_name:
            embed = discord.Embed(title=f"Nickname change",
                                  colour=after.colour,
                                  timestamp=datetime.now(self.IST))
            embed.add_field(name="Member Id :", value=f"{before.id}")
            fields = [("Before", before.display_name, False),
                      ("After", after.display_name, False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            log_channel = self.client.get_channel(863000479889096724)
            await log_channel.send(embed=embed)

        elif before.roles != after.roles:
            embed = discord.Embed(title=f"Role updates",
                                  colour=after.colour,
                                  timestamp=datetime.now(self.IST))
            embed.add_field(name="Member Id :", value=f"{before.id}")
            fields = [("Before", ", ".join([r.mention for r in before.roles]), False),
                      ("After", ", ".join([r.mention for r in after.roles]), False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            log_channel = self.client.get_channel(863000479889096724)
            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.content != after.content:
            embed = discord.Embed(title="Message edit",
                                  description=f"Edit by {after.author.name} , id = {after.author.id}",
                                  colour=after.author.colour,
                                  timestamp=datetime.now(self.IST))

            fields = [("Before", before.content, False),
                      ("After", after.content, False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            log_channel = self.client.get_channel(863000479889096724)
            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if not message.author.bot:
            embed = discord.Embed(title="Message deletion",
                                  description=f"Action by {message.author.display_name}.",
                                  colour=message.author.colour,
                                  timestamp=datetime.now(self.IST))
            embed.add_field(name="member id : ", value=f"-{message.author.id}")
            embed.add_field(name="channel : ", value=f"-{message.channel.mention}")

            fields = [("Content", message.content, False)]
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            log_channel = self.client.get_channel(863000479889096724)
            await log_channel.send(embed=embed)


def setup(client):
    client.add_cog(Events(client))
