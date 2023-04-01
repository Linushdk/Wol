import discord
from discord.ext import commands
import config
from utils import embedcheck, logs, urlcheck
import io
import chat_exporter
from cogs.Systeme import ticket_sys
import datetime

async def create_ticket(creater: discord.Member, grund: str, db):	
    db.update_one({"_id": "settings"}, {"$set": {"ticket_number": db.find_one({"_id": "settings"})["ticket_number"] + 1}})
    server = creater.guild
    cat = server.get_channel(config.DB.tickets.find_one({"_id": "settings"})["ticket_category"])
    ticket_channel = await server.create_text_channel(f"ticket - {db.find_one({'_id': 'settings'})['ticket_number']}",
                                                                category=cat,
                                                                topic=f"Ticket von {creater.mention} - {grund}")


    db.insert_one({"ticket_channel": ticket_channel.id, "user": creater.id, "grund": grund, "status": "offen"})  
    await ticket_channel.set_permissions(creater, view_channel=True, read_messages=True, send_messages=True, create_instant_invite=False)
    await logs.create(title='Ticket | Create', message=f'{creater.mention} created a ticket({ticket_channel.mention})\nReason:`{grund}`', color=config.GREEN, guild=server, db=config.DB.tickets)


async def transcript(interaction: discord.Interaction):
    await interaction.response.defer() 
    transcript = await chat_exporter.export(interaction.channel)


    transcript_file = discord.File(
        io.BytesIO(transcript.encode()),
        filename=f"transcript-{interaction.channel.name}.html",
    )
    message = await interaction.followup.send(file=transcript_file)
    link = await chat_exporter.link(message)            
    embed4 = discord.Embed(
        title="__Transcript__",
        description="Klick auf den link oder lade dir die Datei runter um dir das Transcript aunzusehen",
        color=config.TRANPARENT,

    )
    embed4.add_field(name=f"Transcript Link", value=f"[Hier klicken für link.]({link})")
    await interaction.channel.send(embed=embed4)


async def close_ticket(interaction: discord.Interaction, db):
    for role in interaction.guild.roles:
        if(not ticket_sys.IGNORE_CLOSE.__contains__(role.id)):
            for member in role.members:       
                overwrite = discord.PermissionOverwrite()
                overwrite.send_messages = False
                overwrite.create_instant_invite = False
                await interaction.channel.set_permissions(member, overwrite=overwrite)

    new_cat = interaction.guild.get_channel(db.find_one({'_id': 'settings'})['close_category'])
    await interaction.channel.edit(category=new_cat)
    await logs.create(title="Ticket | Closed", message=f"{interaction.channel} closed by {interaction.user}", color=config.RED, guild=interaction.guild, db=db)

    db.update_one({"ticket_channel": interaction.channel.id}, {"$set": {"status": "geschlossen"}})

async def reopen_ticket(interaction: discord.Interaction, db):
    for role in interaction.guild.roles:
        if(not ticket_sys.IGNORE_CLOSE.__contains__(role.id)):
            for member in role.members:      
                overwrite = discord.PermissionOverwrite()
                overwrite.send_messages = True
                overwrite.create_instant_invite = False
                await interaction.channel.set_permissions(member, overwrite=overwrite)
    cat = interaction.guild.get_channel(db.find_one({'_id': 'settings'})['ticket_category'])
    await interaction.channel.edit(category=cat)
    await logs.create(title="Ticket | Opened", message=f"{interaction.channel} opened by {interaction.user}", color=config.GREEN, guild=interaction.guild, db=db)
    db.update_one({"ticket_channel": interaction.channel.id}, {"$set": {"status": "offen"}})

async def delete_ticket(interaction: discord.Interaction, db):
    await interaction.response.defer()
    ticket_doc = db.find_one({"ticket_channel": interaction.channel.id})
    grund  = ticket_doc["grund"]
    user = ticket_doc["user"]

    transcript = await chat_exporter.export(interaction.channel)
    transcript_file = discord.File(
        io.BytesIO(transcript.encode()),
        filename=f"transcript-{interaction.channel.name}.html",
    )
    channel = discord.utils.get(interaction.guild.text_channels, id=db.find_one({'_id': 'settings'})['log_channel'])
    channel2 = discord.utils.get(interaction.guild.text_channels, id=db.find_one({'_id': 'settings'})['file_log_channel'])
    user2 = discord.utils.get(interaction.guild.members, id=user)

    message = await channel2.send(file=transcript_file)
    link = await chat_exporter.link(message)
    embed2 = discord.Embed(
        title=f"Ticket | Deleted",
        color=config.RED,
        timestamp=datetime.datetime.utcnow()
    )
    embed2.add_field(name="Opend by", value=f"{user2.mention}", inline=True)
    embed2.add_field(name="Deleted by", value=f"{interaction.user.mention}", inline=True)
    embed2.add_field(name="Reason", value=f"`{grund}`", inline=True)
    embed2.add_field(name="Transcript", value=f"[Hier klicken für link.]({link})", inline=True)         
    await channel.send(embed=embed2)
    await interaction.channel.delete()
    db.update_one({"ticket_channel": interaction.channel.id}, {"$set": {"status": "gelöscht"}})

async def add_user(interaction: discord.Interaction, db, user: discord.Member):
    await interaction.response.defer()
    await interaction.channel.set_permissions(user, send_messages=True, read_messages=True, create_instant_invite=False)
    await interaction.followup.send(f"{user.mention} wurde hinzugefügt.", ephemeral=True)
    await logs.create(title="Ticket | Add User", message=f"{interaction.user.mention} added {user.mention} to {interaction.channel.mention}", color=config.GREEN, guild=interaction.guild, db=db)

async def remove_user(interaction: discord.Interaction, db, user: discord.Member):
    await interaction.response.defer()
    await interaction.channel.set_permissions(user, send_messages=False, read_messages=False, create_instant_invite=False)
    await interaction.followup.send(f"{user.mention} wurde entfernt.", ephemeral=True)
    await logs.create(title="Ticket | Remove User", message=f"{interaction.user.mention} removed {user.mention} from {interaction.channel.mention}", color=config.RED, guild=interaction.guild, db=db)

async def log_channel_check(interaction: discord.Interaction, db, view: discord.ui.View):
    embed = discord.Embed(title="Ticket System Setup", description="Im ersten schritt musst du folgende Channel und Kategorien festlegen.", color=0x00ff00)
    res = db.find_one({"_id": "settings"})        
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
        embed.add_field(name="Ticket Kategorie", value=f"Die Ticket Kategorie ist: `{res['ticket_category']}`", inline=False)#
    if res["close_category"] == 0:
        embed.add_field(name="Close Kategorie", value=f"Die Close Kategorie ist: Noch nicht festgelegt", inline=False)
    else:
        embed.add_field(name="Close Kategorie", value=f"Die Close Kategorie ist: `{res['close_category']}`", inline=False)

    await interaction.response.edit_message(embed=embed, view=view)

async def check_mod_roles(interaction: discord.Interaction, db, view: discord.ui.View):
    embed = discord.Embed(
        title="Ticket System Setup | Schritt 2",
        description="Im zwieten Schritt musst du die Ticket Mod Rollen festlegen.",
    )
    res = db.find_one({"_id": "settings"})
    num  = 1
    if res["IGNORE_CLOSE"] == []:
            embed.add_field(name="Ticket Mod Rollen", value=f"Es sind noch keine Ticket Mod Rollen festgelegt", inline=False)
    else:    
        for role in res["IGNORE_CLOSE"]:
            role2 = interaction.guild.get_role(role)
            embed.add_field(name=f"Rolle {num}", value=f"{role2.mention}", inline=False)
            num += 1
    
    await interaction.response.edit_message(embed=embed, view=view())