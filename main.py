import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord.commands import Option
import ezcord
from colorama import Fore
import logging
intents = discord.Intents.all()
intents.members = True
intents.message_content = True
colors = {logging.DEBUG: Fore.GREEN}
ezcord.set_log(log_level=logging.DEBUG, colors=colors)
load_dotenv()
bot = ezcord.Bot(
    intents=intents,
    debug_guilds=[1049368328067624990],
    error_webhook_url=os.getenv("WEBHOOK"),
)

if __name__ == "__main__":
    bot.load_cogs("cogs", subdirectories=True)
    bot.run(os.getenv("TOKEN"))