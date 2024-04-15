import discord
from discord.ext import commands 
import datetime
import time

class Autoroles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
    
    @commands.hybrid_group()
    @commands.has_permissions(administrator=True)
    async def autorole(self, ctx):
        await ctx.send("Please, use this command properly, like; `.autorole add <role>`")
        
    @autorole.command()        
    async def add(self, ctx, role: discord.Role):
        if role is None:
            return await ctx.send("Please mention a role, `.autorole add <role>`") 
        else:
            try:
                query = "SELECT * FROM autorole WHERE guild_id = $1 AND role_id = $2"
                record = await self.bot.db.fetchrow(query, ctx.guild.id, role.id)
                if record:
                    return await ctx.send(f"{role.mention} is already a default autorole.")
                
                if ctx.guild.me.top_role > role:
                    try:
                        query = "INSERT INTO autorole (guild_id, role_id) VALUES ($1, $2)"
                        await self.bot.db.execute(query, ctx.guild.id, role.id)
                        embed = discord.Embed()
                        embed.color = 0x2e2e2e
                        embed.description = f"{role.mention} is now default autorole."
                        await ctx.send(embed=embed)
                    except Exception as e:
                        print(e)
                else:
                    await ctx.send("Bot's role is lower than the selected role.")
            except Exception as e:
                print(e)
    
    @autorole.command()        
    async def remove(self, ctx, role: discord.Role):
        if role is None:
            return await ctx.send("Please mention a role, `.autorole remove <role>`") 
        else:
            try:
                query = "DELETE FROM autorole WHERE guild_id = $1 AND role_id = $2"
                await self.bot.db.execute(query, ctx.guild.id, role.id)
                embed = discord.Embed()
                embed.color = 0x2e2e2e
                embed.description = f"{role.mention} is no longer a default autorole."
                await ctx.send(embed=embed)
            except Exception as e:
                print(e)
                
    @autorole.command()
    async def log(self, ctx, channel: discord.TextChannel):
        try:
            query1 = "SELECT * FROM autorole WHERE guild_id = $1 and logchannel = $2"
            r = await self.bot.db.fetchrow(query1, ctx.guild.id, channel.id)
            if r:
                return await ctx.send(f"Already!, logging channel is setuped to {channel.mention}({channel.id})")
            else:
                query2 = "UPDATE autorole SET logchannel = $1 WHERE guild_id = $2"
                await self.bot.db.execute(query2, channel.id, ctx.guild.id)
                embed = discord.Embed()
                embed.color = 0x2e2e2e
                embed.description = f"{channel.mention}({channel.id}) is now the logging channel."
                await ctx.send(embed=embed)
        except Exception as e:
            print(e)
                


    async def guild_autorole(self, guild):
        try:
            query = "SELECT role_id FROM autorole WHERE guild_id = $1"
            res = await self.bot.db.fetchrow(query, guild.id)
            if res:
                return res["role_id"]
            else:
                return None
        except Exception as e:
            print(e)
            return None


    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if member.bot:
            return        
        default_autorole = await self.guild_autorole(member.guild)
        if default_autorole:
            try:
                role = member.guild.get_role(default_autorole)
                await member.add_roles(role,reason="autorole.")
                records = await self.bot.db.fetch("SELECT logchannel FROM autorole WHERE guild_id = $1 AND role_id = $2",
                                        member.guild.id,
                                        default_autorole)
                if records:
                    for r in records:
                        rr = r['logchannel']
                        if rr:
                            ch = member.guild.get_channel(rr)
                            if ch:
                                await ch.send(f"{member.mention} has joined the server, and I've assigned {role.mention}")
            except Exception as e:
                print(e)
    



async def setup(bot) -> None:
    await bot.add_cog(Autoroles(bot))
