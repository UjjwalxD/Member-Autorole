import discord 
from discord.ext import commands 
from discord import Intents
import os,asyncpg, jishaku
from config import t  

os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
os.environ["JISHAKU_HIDE"] = "True"
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_FORCE_PAGINATOR"] = "True"

class Ujjwal(commands.AutoShardedBot):
    def __init__(self, *args , **kwargs) -> None:
        super().__init__(sync_commands=True, shard_count=1, case_insensitive=True,command_prefix=".", intents=Intents.all())
        self.owner_ids = [1033579545254711336]
        
        
    async def on_ready(self):
        print("logged in as bot")
        
        
    async def setup_hook(self) -> None:
        await self.load_extension('jishaku')
        await self.tree.sync()
        await self.load_extension('cogs.commands')
        try:
            self.db = await asyncpg.create_pool("postgres://postgres.nputcglxpzypigkcgurj:yKqQcG8bkL6pvC7l@aws-0-ap-south-1.pooler.supabase.com/postgres", min_size=4, max_size=5)
            print("logged in postgres db")
        except Exception as e:
            print(e)
        try:
            async with self.db.acquire() as conn:
                with open("sql/schemas.sql", 'r') as sql_file:
                    sql_query = sql_file.read()
                    await conn.execute(sql_query)

     
        except Exception as e:
            print(e)
        
        


bot = Ujjwal()
bot.run(t)