import discord 
from discord.ext import commands
from discord.commands import Option, SlashCommand, SlashCommandGroup
import ezcord
import config
import mongoDB
from utils import ticket, embedcheck, logs


class TicketSetup(discord.Cog):
    def __init__(self, bot):
        self.bot = bot

    setup = SlashCommandGroup("setup", description="Richte das Ticket System ein")

    @setup.command(description="Schritt 1: Setze den Log Channel für die Tickets")
    async def ticket(self, ctx):
        embed = discord.Embed(title="Ticket System Setup", description="Im ersten schritt musst du folgende Channel und Kategorien festlegen.", color=0x00ff00)
        res = config.DB.tickets.find_one({"_id": "settings"})        
        if res["log_channel"] == 0:
            embed.add_field(name="Log Channel", value=f"Der Log Channel ist: Noch nicht festgelegt", inline=False)
        else:
            embed.add_field(name="Log Channel", value=f"Der Log Channel ist: <#{res['log_channel']}>", inline=False)
        if res["file_log_channel"] == 0:
            embed.add_field(name="File Log Channel", value=f"Der File Log Channel ist: Noch nicht festgelegt", inline=False)
        else:
            embed.add_field(name="File Log Channel", value=f"Der File Log Channel ist: <#{res['file_log_channel']}>", inline=False)
        if res["ticket_category"] == 0:
            embed.add_field(name="Ticket Kategorie", value=f"Die Ticket Kategorie ist: Noch nicht festgelegt", inline=False)
        else:
            embed.add_field(name="Ticket Kategorie", value=f"Die Ticket Kategorie ist: <#{res['ticket_category']}>", inline=False)#
        if res["close_category"] == 0:
            embed.add_field(name="Close Kategorie", value=f"Die Close Kategorie ist: Noch nicht festgelegt", inline=False)
        else:
            embed.add_field(name="Close Kategorie", value=f"Die Close Kategorie ist: <#{res['close_category']}>", inline=False)

        await ctx.respond(embed=embed, view=LogChannelSetup(), ephemeral=True)

def setup(bot):
    bot.add_cog(TicketSetup(bot))

class LogChannelSetup(discord.ui.View):
    @discord.ui.channel_select(placeholder="Wähle den Log Channel aus", custom_id="log_channel", min_values=1, max_values=1)
    async def log_channel(self, select, interaction):
        channel = interaction.guild.get_channel(select.values[0].id)
        if channel.type == discord.ChannelType.text:    
            tickets = mongoDB.mongoDB1(config.DB.tickets)
            tickets.insertOrUpdate({"_id": "settings"}, {"log_channel": select.values[0].id})
            await ticket.log_channel_check(interaction=interaction, db=config.DB.tickets, view=LogChannelSetup())
        else:
            await interaction.response.send_message("Du musst einen Text Channel auswählen!", ephemeral=True)
    @discord.ui.channel_select(placeholder="Wähle den File Log Channel aus", custom_id="file_log_channel", min_values=1, max_values=1)
    async def file_log_channel(self, select, interaction):
        channel = interaction.guild.get_channel(select.values[0].id)
        if channel.type == discord.ChannelType.text:    
            tickets = mongoDB.mongoDB1(config.DB.tickets)
            tickets.insertOrUpdate({"_id": "settings"}, {"file_log_channel": select.values[0].id})
            await ticket.log_channel_check(interaction=interaction, db=config.DB.tickets, view=LogChannelSetup())
        else:
            await interaction.response.send_message("Du musst einen Text Channel auswählen!", ephemeral=True)

    @discord.ui.channel_select(placeholder="Wähle die Ticket Kategorie aus", custom_id="ticket_category", min_values=1, max_values=1)
    async def ticket_category(self, select, interaction):
        category = interaction.guild.get_channel(select.values[0].id)
        if category.type == discord.ChannelType.category:    
            tickets = mongoDB.mongoDB1(config.DB.tickets)
            tickets.insertOrUpdate({"_id": "settings"}, {"ticket_category": select.values[0].id})
            await ticket.log_channel_check(interaction=interaction, db=config.DB.tickets, view=LogChannelSetup())
        else:
            await interaction.response.send_message("Du musst eine Kategorie auswählen!", ephemeral=True)
    
    @discord.ui.channel_select(placeholder="Wähle die Close Kategorie aus", custom_id="close_category", min_values=1, max_values=1)
    async def close_category(self, select, interaction):
        category = interaction.guild.get_channel(select.values[0].id)
        if category.type == discord.ChannelType.category:    
            tickets = mongoDB.mongoDB1(config.DB.tickets)
            tickets.insertOrUpdate({"_id": "settings"}, {"close_category": select.values[0].id})
            await ticket.log_channel_check(interaction=interaction, db=config.DB.tickets, view=LogChannelSetup())
        else:
            await interaction.response.send_message("Du musst eine Kategorie auswählen!", ephemeral=True)
    
    @discord.ui.button(label="Nächster Schritt", style=discord.ButtonStyle.green)
    async def next_step(self, button, interaction):
        embed = discord.Embed(
            title="Ticket System Setup | Schritt 2",
            description="Im zwieten Schritt musst du die Ticket Mod Rollen festlegen.",
        )
        res = config.DB.tickets.find_one({"_id": "settings"})
        num  = 1
        if res["IGNORE_CLOSE"] == []:
             embed.add_field(name="Ticket Mod Rollen", value=f"Es sind noch keine Ticket Mod Rollen festgelegt", inline=False)
        else:    
            for role in res["IGNORE_CLOSE"]:
                role2 = interaction.guild.get_role(role)
                embed.add_field(name=f"Rolle {num}", value=f"{role2.mention}", inline=False)
                num += 1
        
        await interaction.response.edit_message(embed=embed, view=TicketModRoles())

class TicketModRoles(discord.ui.View):
    @discord.ui.role_select(placeholder="Wähle die Ticket Mod Rollen aus", custom_id="ticket_mod_roles", min_values=1, max_values=10)
    async def ticket_mod_roles(self, select, interaction):
        roles = select.values
        res = config.DB.tickets.find_one({"_id": "settings"})
        for role in roles:
            if role in res["IGNORE_CLOSE"]:
                role2 = interaction.guild.get_role(role)
                return await interaction.response.send_message(f"{role2.mention} Rolle ist schon in der Liste!", ephemeral=True)
            else: 
                config.DB.tickets.update_one({"_id": "settings"}, {"$push": {"IGNORE_CLOSE": role}})
                await ticket.log_channel_check(interaction=interaction, db=config.DB.tickets, view=TicketModRoles())
