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
                    await message.channe.send(f"{message.author.mention} Ik you are staff pls mind ur language")
                    return
                await message.delete()
                await message.channel.send(
                    f"{message.author.mention} No bad words Allowed Here.\n\nRepeating this will Cause in a Mute.")  # ,delete_after = 10)

        if "discord.gg/" in message.content.lower():
            if message.author.guild_permissions.manage_messages:
                return
            await message.delete()
            await message.channel.send(
                f"{message.author.mention} No invite Links allowed!\n\nRepeating this will Cause in a Mute.")



def setup(client):
    client.add_cog(Automod(client))
