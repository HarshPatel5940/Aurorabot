import asyncio

import discord
from discord.ext import commands


class Automod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild = self.bot.get_guild(799974967504535572)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.display_name != after.display_name:
            if not after.guild_permissions.manage_roles:
                if f"{after.display_name}".startswith("!" or "! "):
                    await after.edit(nick="zHoister Alert")

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
                try:
                    await message.delete()
                except:
                    pass
                await message.channel.send(
                    f"{message.author.mention} You Are Not Allowed to Send Long Messages!\n\nRepeating this will Cause in a Mute.")

            if "discord.gg/" in message.content.lower() or "disboard.org/server/" in message.content.lower():
                if message.author.guild_permissions.manage_messages:
                    return
                try:
                    await message.delete()
                    await message.channel.send(
                        f"{message.author.mention} No invite Links allowed! <a:ALERT:895323744380256286> Repeating this will Cause in a Mute.")
                    embed = discord.Embed(title=f"AutoMod Warned {message.author.name}",
                                          description=f"reason : Sent Invite link", colour=discord.Color.red())
                    log_channel = self.bot.get_channel(
                        self.bot.mod_logs[message.guild.id])
                    await log_channel.send(embed=embed)
                except:
                    pass

            lst = message.content.split("\n")
            if len(lst) > 9:
                if message.author.guild_permissions.manage_messages:
                    return
                try:
                    await message.delete()
                except:
                    pass
                await message.channel.send(
                    f"{message.author.mention} Don't send messages with multiple lines! <a:ALERT:895323744380256286> Repeating this will Cause in a Mute.")
                embed = discord.Embed(title=f"AutoMod Warned {message.author.name}",
                                      description=f"reason : Sent Multiple lines in a single message",
                                      colour=discord.Color.red())
                log_channel = self.bot.get_channel(
                    self.bot.mod_logs[message.guild.id])
                await log_channel.send(embed=embed)

            if len(message.mentions) > 8:
                if message.author.guild_permissions.manage_messages:
                    return
                await message.delete()
                await message.channel.send(
                    f"{message.author.mention} Don't Mass Mention! You Have Been Muted in Server for 5m")
                role = discord.utils.get(message.guild.roles, name="Muted")
                await message.author.add_roles(role, reason="Automod muted for Mass Mention (5m)")
                embed = discord.Embed(title=f"AutoMod Muted {message.author.name}",
                                      description=f"reason : Spamming", colour=discord.Color.red())
                log_channel = self.bot.get_channel(
                    self.bot.mod_logs[message.guild.id])
                await log_channel.send(embed=embed)
                await asyncio.sleep(300)
                await message.author.remove_roles(role, reason="Automatic unmute for spam")

            bad_words = ["fuck", "bitch", "madharbhakt", "nigger", "nigga", "b#tch", "fuker",
                         "laude", "nude", "sex", "chutiye", "madarchod", "bhienchod", "madarbhakt", "porn"]

            for words in bad_words:
                if words in message.content.lower():
                    if message.author.guild_permissions.manage_messages:
                        return
                    try:
                        await message.delete()
                        await message.channel.send(
                            f"{message.author.mention} No bad words Allowed Here.<a:ALERT:895323744380256286> Repeating this will Cause in a Mute.")
                        embed = discord.Embed(title=f"AutoMod Warned {message.author.name}",
                                              description=f"reason : Used bad word ||{words}||", colour=discord.Color.red())
                        log_channel = self.bot.get_channel(
                            self.bot.mod_logs[message.guild.id])
                        await log_channel.send(embed=embed)
                    except:
                        pass

            if len(list(filter(lambda message: check(message), self.bot.cached_messages))) >= 4:
                if message.author.guild_permissions.manage_roles and message.author.guild_permissions.manage_messages:
                    await message.channel.send(
                        f"{message.author.mention} AY sir, ik you are **staff that does not means you can spam** !!",
                        delete_after=5)
                    return
                role = discord.utils.get(message.guild.roles, name="Muted")
                await message.author.add_roles(role, reason="Automod muted Spamming")
                embed = discord.Embed(title=f"AutoMod Muted {message.author.name}",
                                      description=f"reason : Spamming", colour=discord.Color.red())
                log_channel = self.bot.get_channel(
                    self.bot.mod_logs[message.guild.id])
                await log_channel.send(embed=embed)
                await asyncio.sleep(1)
                await message.channel.send(
                    f"{message.author.mention} Don't spam Messages! You Have Been Muted in Server for 5m")
                await asyncio.sleep(300)
                await message.author.remove_roles(role, reason="Automatic unmute for spam")


def setup(bot):
    bot.add_cog(Automod(bot))
