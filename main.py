#imports
import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import os
import json


class helpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__()
    async def send_bot_help(self, mapping):
        await self.get_destination().send(embed=discord.Embed(title="Help", color=discord.Colour.green(), description='''
Dealer is a bot that brings an economy and games to your server.
Commands start with a semicolon (";")
Use ";features" to display a list of all commands.
Use ";poker_rules" for an explanation of how to play poker.
Use ";technical_information" for more information about this bot.

        '''))


#Setup
intents = discord.Intents.all()
client = commands.Bot(intents=intents, command_prefix=";")
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('poker'))
    await load_extensions()


@client.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send(embed=discord.Embed(title="Dealer Here.", description='''
Thanks for inviting me to your server! To get started, check out the features I offer by using ";features".

Invite me to other servers by using: https://discord.com/oauth2/authorize?client_id=866733937115922443&permissions=0&scope=bot
            '''))
        break


@client.command()
async def technical_information(ctx):
    await ctx.send(embed=discord.Embed(title="Dealer#5191", description="""
Initial Release: 7/19/2021
Latest Major Update: 8/22/2021
Latest Update: 5/14/2023
Invite Link: https://discord.com/oauth2/authorize?client_id=866733937115922443&permissions=0&scope=bot
Developer: Sean Huang
For a list of all commands, use ;features
"""))


@client.command()
async def features(ctx):
    await ctx.send(embed=discord.Embed(title="Here are all the Commands:", color=discord.Colour.green(), description='''
**Game Commands**
Black Jack                      ;bj (amount)

Texas Hold 'em poker            ;poker (limit), (player2), (player3), ...

5 Card Poker                    ;five_poker (amount), (player)

squares                         ;squares (amount)

**Economy Commands**
Check your balence              ;balence

Check other's balence           ;bal (name)

Steal Chips                     ;steal (name)

Daily Chips                     ;daily

Local Leaderboard               ;leaderboard

Give Chips                      ;give (name) (amount)

Spend Chips                     ;shop (item)


**Information Commands**
Display a help page             ;help

Display this page of commands   ;features

Learn how to play poker         ;poker_rules

Learn how to play squares       ;square_rules
        '''))
    

@client.command()
async def square_rules(ctx):
    await ctx.send(embed=discord.Embed(title="How to Play Squares", color=discord.Colour.red(), description='''
Squares is a singleplayer game where the goal is to turn all red squares into white squares in the optimal number of moves.

You can flip a row or column one at a time by typing the corrosponding number or letter to the columnor row 
into the text channel this game was initiated in.

After you select a row/column, all white squares in the selected row/column will be turned into red squares and
all red squares will be turned into white squares.

You must win in the optimal number of moves. Winning yields a reward equivilent to 1.5x your initial bet.
Failing to clear the game will result in the loss of all tokens bet.

There must be no more than a pause of 30 seconds between each move. Idling for more than 30 seconds will
result in the game being forfeited.
    '''))


async def load_extensions():
    for filename in os.listdir('./bot_cogs'):
        if filename.endswith('.py'):
            await client.load_extension(f'bot_cogs.{filename[:-3]}')


#The file "BotToken.json" stores the token that is used to run the bot
with open('bot_cogs/BotToken.json', "r") as f:
    Token = json.load(f); Token = Token["key"]

async def main():
    async with client:
        await load_extensions()
        await client.start(Token)

asyncio.run(main())
