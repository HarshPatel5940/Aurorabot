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

            bad_words = ["fuck", "bitch", "madharbhakt", "nigger", "nigga", "b#tch", "fuker",
                         "Laude", "nude", "sex", "chutiye", "madarchod", "bhienchod", "madarbhakt", "porn"]

            for words in bad_words:
                if words in message.content.lower():
                    if message.author.guild_permissions.manage_messages:
                        await message.channel.send(f"{message.author.mention} Ik you are staff pls mind ur language", delete_after=5)
                        return
                    await message.delete()

                    await message.channel.send(
                        f"{message.author.mention} No bad words Allowed Here.\n\nRepeating this will Cause in a Mute.")

            if "discord.gg/" in message.content.lower():
                if message.author.guild_permissions.manage_messages:
                    return
                await message.delete()

                await message.channel.send(
                    f"{message.author.mention} No invite Links allowed!\n\nRepeating this will Cause in a Mute.")

            if len(list(filter(lambda message: check(message), self.client.cached_messages))) >= 4:
                if message.author.guild_permissions.manage_roles:
                    await message.channel.send(
                        f"{message.author.mention} AY sir, ik you are **staff that does not means you can spam** !!")
                    return
                await message.channel.send(
                    f"{message.author.mention} Don't spam Messages! You Have Been Muted in Server for 5m")
                role = discord.utils.get(message.guild.roles, name="Muted")
                await message.author.add_roles(role, reason="Spamming")
                log_channel = self.client.get_channel(863000643303374920)

                await log_channel.send(f"**{message.author.mention} was muted for 5m for spamming**")
                await asyncio.sleep(300)
                await message.author.remove_roles(role)


def setup(client):
    client.add_cog(Automod(client))
