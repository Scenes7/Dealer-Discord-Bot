import discord
from discord.ext import commands

class chat_modifacations(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    #clear chat
    @commands.command()
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount)
    
    


def setup(client):
    client.add_cog(chat_modifacations(client))