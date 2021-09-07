import asyncio
import discord
from discord.ext import commands


class Automod(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.guild = self.client.get_guild(799974967504535572)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.Cog.listener()
    async def on_message(self, message):

        def check(m):
            return (m.author == message.author
                    and len(m.content)
                    and (discord.utils.utcnow() - m.created_at).seconds < 4)

        if not message.author.bot:
            if len(message.content) > 1500:
                if message.author.guild_permissions.manage_messages:
                    return
                await message.delete()

                await message.channel.send(
                    f"{message.author.mention} You Are Not Allowed to Send Long Messages!\n\nRepeating this will Cause in a Mute.")

            if "discord.gg/" in message.content.lower():
                if message.author.guild_permissions.manage_messages:
                    return
                await message.delete()
                await message.channel.send(
                    f"{message.author.mention} No invite Links allowed! <a:Red_alert:863017113581256715> Repeating this will Cause in a Mute.")
                embed = discord.Embed(title=f"AutoMod Warned {message.author.name}",
                                      description=f"reason : Sent Invite link", colour=discord.Color.red())
                log_channel = self.client.get_channel(863000643303374920)
                await log_channel.send(embed=embed)

            lst = message.content.split("\n")
            if len(lst) > 9:
                if message.author.guild_permissions.manage_messages:
                    return
                await message.reply(
                    f"{message.author.mention} Don't send messages with multiple lines! <a:Red_alert:863017113581256715> Repeating this will Cause in a Mute.")
                embed = discord.Embed(title=f"AutoMod Warned {message.author.name}",
                                      description=f"reason : Sent Multiple lines in a single message", colour=discord.Color.red())
                log_channel = self.client.get_channel(863000643303374920)
                await log_channel.send(embed=embed)

            bad_words = ["fuck", "bitch", "madharbhakt", "nigger", "nigga", "b#tch", "fuker",
                         "laude", "nude", "sex", "chutiye", "madarchod", "bhienchod", "madarbhakt", "porn"]

            for words in bad_words:
                if words in message.content.lower():
                    if message.author.guild_permissions.manage_messages:
                        await message.channel.send(f"{message.author.mention} Ik you are staff pls mind ur language", delete_after=5)
                        return
                    await message.delete()

                    await message.channel.send(
                        f"{message.author.mention} No bad words Allowed Here.<a:Red_alert:863017113581256715> Repeating this will Cause in a Mute.")
                    embed = discord.Embed(title=f"AutoMod Warned {message.author.name}",
                                          description=f"reason : Used bad word ||{words}||", colour=discord.Color.red())
                    log_channel = self.client.get_channel(863000643303374920)
                    await log_channel.send(embed=embed)


            if len(list(filter(lambda message: check(message), self.client.cached_messages))) >= 4:
                if message.author.guild_permissions.manage_roles and message.author.guild_permissions.manage_messages:
                    await message.channel.send(
                        f"{message.author.mention} AY sir, ik you are **staff that does not means you can spam** !!", delete_after=5)
                    return
                role = discord.utils.get(message.guild.roles, name="Muted")
                await message.author.add_roles(role, reason="Automod muted Spamming")
                embed = discord.Embed(title=f"AutoMod Muted {message.author.name}",
                                      description=f"reason : Spamming", colour=discord.Color.red())
                log_channel = self.client.get_channel(863000643303374920)
                await log_channel.send(embed=embed)
                await asyncio.sleep(1)
                await message.channel.send(
                    f"{message.author.mention} Don't spam Messages! You Have Been Muted in Server for 5m")
                await asyncio.sleep(300)
                await message.author.remove_roles(role, reason="Automatic unmute for spam")


def setup(client):
    client.add_cog(Automod(client))
