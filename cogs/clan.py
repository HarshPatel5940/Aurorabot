import discord
from discord.ext import commands


class Clan(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.group(name="clan")
    @commands.has_permissions(administrator=True)
    async def clan(self, message):
        """Clan  Commands"""
        pass

    @clan.command(name='add')
    async def add(self, ctx, member: discord.Member, rank):
        """Add A member in clan embed"""
        await self.bot.db.execute(f"""INSERT INTO clan(member_id,rank)
        VALUES ('{member.id}','{rank}');""")
        self.bot.clan[member.id] = rank
        await ctx.reply(f"{member.name}#{member.discriminator} has been addded to Db with {rank}")

    @clan.command(name='remove')
    async def remove(self, ctx, member: discord.Member):
        """remove A member in clan embed"""
        await self.bot.db.execute(f"""DELETE FROM clan WHERE member_id = $1""", member.id)
        del self.bot.clan[member.id]
        await ctx.reply(f"{member.name}#{member.discriminator} Has Been Removed from Db")

    @clan.command(name='setrank', aliases=["sr", "change"])
    async def rank_change(self, ctx, member: discord.Member, rank):
        """Update a member rank"""
        await self.bot.db.execute(f"""UPDATE clan SET rank = $1 WHERE member_id = $2""", rank, member.id)
        self.bot.clan[member.id] = rank
        await ctx.reply(f"{member.name}#{member.discriminator} Rank Has Been Changed to {rank}")

    @clan.command(name='update')
    async def embed_update(self, message):
        esports = []
        manager = []
        moderator = []
        commando = []
        officials = []
        doc = '**__CLAN MEMBER RANKS__\n\n**<@798584468998586388> **CLAN LEADER & SERVER OWNER**\n'
        guild = self.bot.get_guild(799974967504535572)

        for n in self.bot.clan:
            if self.bot.clan[n].lower() == "manager":
                manager.append(n)
            elif self.bot.clan[n].lower() == "moderator":
                moderator.append(n)
            elif self.bot.clan[n].lower() == "esports":
                esports.append(n)
            elif self.bot.clan[n].lower() == "commando":
                commando.append(n)
            elif self.bot.clan[n].lower() == "official":
                officials.append(n)

        doc += '\n<@&799976410331873290> **Server & Clan Managers**\n'
        for n in manager:
            doc += f'> <@{n}>\n'
        doc += '\n<@&799977125112447006> **Server Moderator**\n'
        for n in moderator:
            doc += f'> <@{n}>\n'
        doc += '\n<@&883317758849331232> **Professional Gamers & Clan Esports Player**\n'
        if esports != []:
            for n in esports:
                doc += f'> <@{n}>\n'
        else:
            doc += "> No Member Declared\n"
        doc += '\n<@&802591442584338473> **Epic Gamers & Clan Seniors**\n'
        for n in commando:
            doc += f'> <@{n}>\n'
        doc += '\n<@&800336531403177984> **Clan Members**\n'
        for n in officials:
            doc += f'> <@{n}>\n'
        # clan = discord.Embed(title='__CLAN MEMBERS RANKS__', description=doc, color=discord.Color.blurple())
        # clan.set_thumbnail(url=guild.icon.url)
        # clan.set_author(name=guild.name, icon_url=guild.icon.url)

        channel = self.bot.get_channel(833302700678578197)
        message1 = await channel.fetch_message(886577181193547826)

        await message1.edit(doc)
        await message.channel.send(":white_check_mark: Clan Member database has Been **UPDATED**")

    @clan.command(name='yt')
    async def yt(self, ctx):
        """Send Clan youtubers embed"""
        doc = """

<@798584468998586388> - [Youtube Link](https://www.youtube.com/channel/UC51O-eJ0YRLo6apeYdSDYtQ)

<@527177457317445632> - [Youtube Link](https://www.youtube.com/channel/UCOH_G9CiRTDPneNpdMKwYDg)

<@735784238384807999> - [Youtube Link](https://www.youtube.com/channel/UCrjHMGF6GoAAsNqxMTEi05g)

<@484319440108781568> - [Youtube Link](https://www.youtube.com/channel/UC04Zp15M5K21g45J45nV3SA)"""
        clan_embed = discord.Embed(
            title='__CLAN CONTENT CREATORS__', description=doc, color=discord.Color.blurple())
        clan_embed.set_thumbnail(url=ctx.guild.icon.url)
        clan_embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon.url)
        await ctx.send(embed=clan_embed)


def setup(bot):
    bot.add_cog(Clan(bot))
