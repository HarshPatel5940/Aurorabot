import asyncio
import json
import time
import traceback

import asyncpg
import discord
from discord.ext import commands

import secret
from cogs.help import HelpCommand

initial_cogs = [
    "help",
    "moderation",
    "other",
    "settings",
    "stats",
    "events",
    "invites",
    "automod",
    "clan"  # This Cog is Specially made for FRNz Server,
    # while cloning i recoment deleting cpgs/clan.py and delete line 22, 66, 87, 88, 89
]


def prefix(self, message):
    if not message.guild:
        return commands.when_mentioned_or('>')(self, message)
    else:
        prefix1 = self.prefix[message.guild.id]
        return commands.when_mentioned_or(prefix1, '>')(self, message)


async def setup_db():
    def _encode_jsonb(value):
        return json.dumps(value)

    def _decode_jsonb(value):
        return json.loads(value)

    async def init(con):
        await con.set_type_codec(
            "jsonb",
            schema="pg_catalog",
            encoder=_encode_jsonb,
            decoder=_decode_jsonb,
            format="text",
        )

    return await asyncpg.create_pool(secret.db_url, init=init, max_size=4, min_size=1)


class AuroraBot(commands.Bot):
    def __init__(self, db) -> None:
        super().__init__(command_prefix=prefix,
                         intents=discord.Intents.all(),
                         activity=discord.Activity(
                             type=discord.ActivityType.listening, name='FRNz PunisherYT'),
                         case_insensitive=True,
                         strip_after_prefix=True,
                         owner_ids=[798584468998586388, 448740493468106753],
                         help_command=HelpCommand())
        self.start_time = time.time()
        self.db = db
        self.version = 11
        self.clan = {}
        self.prefix = {}
        self.mod_logs = {}
        self.ready = False

    async def on_ready(self):
        if self.ready:
            return
        print(f"Logged In as {self.user.name} -- {self.user.id}")
        self.ready = True

    @classmethod
    async def setup(cls):
        db = await setup_db()
        self = cls(db)

        query = """SELECT * FROM guild"""
        fetch = await self.db.fetch(query)
        self.prefix = {n['server_id']: n['prefix'] for n in fetch}
        self.mod_logs = {n['server_id']: n['mod_logs'] for n in fetch}

        query = """SELECT * FROM clan"""
        fetch = await self.db.fetch(query)
        self.clan = {n['member_id']: n['rank'] for n in fetch}

        for e in initial_cogs:
            try:
                self.load_extension(f"cogs.{e}")
            except Exception:
                traceback.print_exc()

        try:
            await self.start(secret.token)
        except KeyboardInterrupt:
            await self.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(AuroraBot.setup())
