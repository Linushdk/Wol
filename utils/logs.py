
from datetime import datetime

import discord
import config
import chat_exporter

import pymongo




async def create(title: str, message: str, color: discord.Color, guild: discord.Guild, db):
    await Log(discord.Embed(title=title, description=message, color=color, timestamp=datetime.utcnow())).send(guild=guild, db=db)


class Log:
    def __init__(self, embed: discord.Embed):
        self.embed = embed
        self.embed.timestamp = datetime.utcnow()


    async def send(self, guild: discord.Guild, db):
        

        
        settings = db.find_one({"_id": "settings"})
        if "log_channel" in settings:
            channel = guild.get_channel(settings["log_channel"])
            await channel.send(embed=self.embed)
