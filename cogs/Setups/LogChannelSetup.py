import discord
from discord.ext import commands
from discord.commands import slash_command, SlashCommandGroup, Option
from utils import embedcheck, logs, urlcheck
import config



class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.Cog.listener()
    async def on_ready(self):
        if config.DB.reports.find_one({"_id": "settings"}) is None:
            config.DB.reports.insert_one({"_id": "settings", "log_channel": 0})
        else:
            pass
        if config.DB.warns.find_one({"_id": "settings"}) is None:
            config.DB.warns.insert_one({"_id": "settings", "log_channel": 0})
        else:
            pass
        if config.DB.bans.find_one({"_id": "settings"}) is None:
            config.DB.bans.insert_one({"_id": "settings", "log_channel": 0})
        else:
            pass
        if config.DB.tickets.find_one({"_id": "settings"}) is None:
            config.DB.tickets.insert_one({"_id": "settings", "log_channel": 0, "ticket_category": 0, "close_category": 0, "file_log_channel": 0, "ticket_number": 0})
        else:
            pass
        if config.DB.tickets.find_one({"_id": "embed"}) is None:
            config.DB.tickets.insert_one({"_id": "embed", "Beschreibung": "0", "Image": "0", "Thumbnail": "0", "Titel": "0", "Farbe": "0", "message": "0"})
        else:
            pass
        if config.DB.Abmelden.find_one({"_id": "settings"}) is None:
            config.DB.Abmelden.insert_one({"_id": "settings", "log_channel": 0})
        else:
            pass
        if config.DB.Abmelden.find_one({"_id": "embed"}) is None:
            config.DB.Abmelden.insert_one({"_id": "embed", "Beschreibung": "0", "Image": "0", "Thumbnail": "0", "Titel": "0", "Farbe": "0", "message": "0"})
        else:
            pass
        if config.DB.timeouts.find_one({"_id": "settings"}) is None:
            config.DB.timeouts.insert_one({"_id": "settings", "log_channel": 0})
        else:
            pass


            
        
    logchannelsetup = SlashCommandGroup("logchannelsetup", description="Setze die Log Channel und die Ticket Kategorien")
    
    
    @logchannelsetup.command(description="Setze den Log Channel für die Reports")
    async def report(self, ctx, channel: Option(discord.TextChannel)):
        config.DB.reports.update_one({"_id": "settings"}, {"$set": {"log_channel": channel.id}})
        await ctx.respond(f"Der LogChannel wurde auf {channel.mention} gesetzt", ephemeral=True)
    
    @logchannelsetup.command(description="Setze den Log Channel für die Warns")
    async def warn(self, ctx, channel: Option(discord.TextChannel)):
        config.DB.warns.update_one({"_id": "settings"}, {"$set": {"log_channel": channel.id}})
        await ctx.respond(f"Der LogChannel wurde auf {channel.mention} gesetzt", ephemeral=True)

    @logchannelsetup.command(description="Setze den Log Channel für die Bans")
    async def ban(self, ctx, channel: Option(discord.TextChannel)):
        config.DB.bans.update_one({"_id": "settings"}, {"$set": {"log_channel": channel.id}})
        await ctx.respond(f"Der LogChannel wurde auf {channel.mention} gesetzt", ephemeral=True)


    @logchannelsetup.command(description="Setze den Log Channel für die Abmeldungen")
    async def abmelden(self, ctx, channel: Option(discord.TextChannel)):
        config.DB.Abmelden.update_one({"_id": "settings"}, {"$set": {"log_channel": channel.id}})
        await ctx.respond(f"Der LogChannel wurde auf {channel.mention} gesetzt", ephemeral=True)

    @logchannelsetup.command(description="Setze den Log Channel für die Timeouts")
    async def timeout(self, ctx, channel: Option(discord.TextChannel)):
        config.DB.timeouts.update_one({"_id": "settings"}, {"$set": {"log_channel": channel.id}})
        await ctx.respond(f"Der LogChannel wurde auf {channel.mention} gesetzt", ephemeral=True)





def setup(bot):
    bot.add_cog(Setup(bot))