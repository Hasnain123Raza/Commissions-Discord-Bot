import os
import discord

from dotenv import load_dotenv
from discord.ext import commands

from Utilities.Initializer import initialize

## IMPORT COGS ##
from Cogs.Commissions import CommissionsCog
from Cogs.Configurations import ConfigurationsCog

## INITIALIZE BOT ##
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!karen ", intents=intents)


@bot.event
async def on_ready():
    initialize(bot)


## ADD COGS ##
bot.add_cog(CommissionsCog(bot))
bot.add_cog(ConfigurationsCog(bot))


## RUN BOT ##
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

bot.run(TOKEN)
