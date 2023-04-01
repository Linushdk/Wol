import discord
from discord.ext import commands
from discord.commands import slash_command, Option
import config 
from utils import urlcheck

async def embedcheck(interaction: discord.Interaction, view: discord.ui.View):
    
    embed = discord.Embed(
        title="Wird bearbeitet",
        description="Bitte warten",
        color=config.TRANPARENT
    )
    await interaction.response.edit_message(embed=embed)
    
    if config.DB.tickets.find_one({"_id": "embed"})["Farbe"] != "0":
        try:
            hex_datenbank = config.DB.tickets.find_one({"_id": "embed"})["Farbe"]
            hexcode = f"0x{hex_datenbank}"
            color = int(hexcode, 16)
            if config.DB.tickets.find_one({"_id": "embed"})["Titel"] != "0":

                edit_embed1 = discord.Embed(
                    title=config.DB.tickets.find_one({"_id": "embed"})["Titel"],
                    description=config.DB.tickets.find_one({"_id": "embed"})["Beschreibung"],
                    color=color
                )
            else:
                edit_embed1 = discord.Embed(
                    title="Titel",
                    description="Beschreibung",
                    color=color
                )
        except:
            if config.DB.tickets.find_one({"_id": "embed"})["Titel"] != "0":

                edit_embed1 = discord.Embed(
                    title=config.DB.tickets.find_one({"_id": "embed"})["Titel"],
                    description=config.DB.tickets.find_one({"_id": "embed"})["Beschreibung"],
                    color=config.TRANPARENT
                )
            else:
                edit_embed1 = discord.Embed(
                    title="Titel",
                    description="Beschreibung",
                    color=config.TRANPARENT
                )



        if config.DB.tickets.find_one({"_id": "embed"})["Image"] != "0":
            Image = config.DB.tickets.find_one({"_id": "embed"})["Image"]
            if urlcheck.is_url_image(Image):
                edit_embed1.set_image(url=config.DB.tickets.find_one({"_id": "embed"})["Image"])
            else:
                await interaction.followup.send("Die angegebene URL ist kein Link zu einem Png, Gif oder jepg Bild. Oder sie ist eine Discord URL. (Image error)", ephemeral=True)
        
        if config.DB.tickets.find_one({"_id": "embed"})["Thumbnail"] != "0":
            Thumbnail = config.DB.tickets.find_one({"_id": "embed"})["Thumbnail"]
            if urlcheck.is_url_image(Thumbnail):
                edit_embed1.set_thumbnail(url=config.DB.tickets.find_one({"_id": "embed"})["Thumbnail"])
            else:
                await interaction.followup.send("Die angegebene URL ist kein Link zu einem Png, Gif oder jepg Bild. Oder sie ist eine Discord URL. (Thumbnail error)", ephemeral=True)

    else:
        if config.DB.tickets.find_one({"_id": "embed"})["Titel"] != "0":

            edit_embed1 = discord.Embed(
                title=config.DB.tickets.find_one({"_id": "embed"})["Titel"],
                description=config.DB.tickets.find_one({"_id": "embed"})["Beschreibung"],
                color=config.TRANPARENT
            )
        else:
            edit_embed1 = discord.Embed(
                title="Titel",
                description="Beschreibung",
                color=config.TRANPARENT
            )

        if config.DB.tickets.find_one({"_id": "embed"})["Image"] != "0":
            Image = config.DB.tickets.find_one({"_id": "embed"})["Image"]
            if urlcheck.is_url_image(Image):
                edit_embed1.set_image(url=config.DB.tickets.find_one({"_id": "embed"})["Image"])
            else:
                await interaction.followup.send("Die angegebene URL ist kein Link zu einem Png, Gif oder jepg Bild. Oder sie ist eine Discord URL. (Image error)", ephemeral=True)

        
        if config.DB.tickets.find_one({"_id": "embed"})["Thumbnail"] != "0":
            Thumbnail = config.DB.tickets.find_one({"_id": "embed"})["Thumbnail"]
            if urlcheck.is_url_image(Thumbnail):
                edit_embed1.set_thumbnail(url=config.DB.tickets.find_one({"_id": "embed"})["Thumbnail"])
            else:
                await interaction.followup.send("Die angegebene URL ist kein Link zu einem Png, Gif oder jepg Bild. Oder sie ist eine Discord URL. (Thumbnail error)", ephemeral=True)

    message = interaction.message.id            
    
    

    await interaction.followup.edit_message(message_id=message, embed=edit_embed1, view=view)


async def embedcheck_Abmelden(interaction: discord.Interaction, view: discord.ui.View):
    
    embed = discord.Embed(
        title="Wird bearbeitet",
        description="Bitte warten",
        color=config.TRANPARENT
    )
    await interaction.response.edit_message(embed=embed)
    
    if config.DB.Abmelden.find_one({"_id": "embed"})["Farbe"] != "0":
        try:
            hex_datenbank = config.DB.Abmelden.find_one({"_id": "embed"})["Farbe"]
            hexcode = f"0x{hex_datenbank}"
            color = int(hexcode, 16)
            if config.DB.Abmelden.find_one({"_id": "embed"})["Titel"] != "0":

                edit_embed1 = discord.Embed(
                    title=config.DB.Abmelden.find_one({"_id": "embed"})["Titel"],
                    description=config.DB.Abmelden.find_one({"_id": "embed"})["Beschreibung"],
                    color=color
                )
            else:
                edit_embed1 = discord.Embed(
                    title="Titel",
                    description="Beschreibung",
                    color=color
                )
        except:
            if config.DB.Abmelden.find_one({"_id": "embed"})["Titel"] != "0":

                edit_embed1 = discord.Embed(
                    title=config.DB.Abmelden.find_one({"_id": "embed"})["Titel"],
                    description=config.DB.Abmelden.find_one({"_id": "embed"})["Beschreibung"],
                    color=config.TRANPARENT
                )
            else:
                edit_embed1 = discord.Embed(
                    title="Titel",
                    description="Beschreibung",
                    color=config.TRANPARENT
                )



        if config.DB.Abmelden.find_one({"_id": "embed"})["Image"] != "0":
            Image = config.DB.Abmelden.find_one({"_id": "embed"})["Image"]
            if urlcheck.is_url_image(Image):
                edit_embed1.set_image(url=config.DB.Abmelden.find_one({"_id": "embed"})["Image"])
            else:
                await interaction.followup.send("Die angegebene URL ist kein Link zu einem Png, Gif oder jepg Bild. Oder sie ist eine Discord URL. (Image error)", ephemeral=True)
        
        if config.DB.Abmelden.find_one({"_id": "embed"})["Thumbnail"] != "0":
            Thumbnail = config.DB.Abmelden.find_one({"_id": "embed"})["Thumbnail"]
            if urlcheck.is_url_image(Thumbnail):
                edit_embed1.set_thumbnail(url=config.DB.Abmelden.find_one({"_id": "embed"})["Thumbnail"])
            else:
                await interaction.followup.send("Die angegebene URL ist kein Link zu einem Png, Gif oder jepg Bild. Oder sie ist eine Discord URL. (Thumbnail error)", ephemeral=True)

    else:
        if config.DB.Abmelden.find_one({"_id": "embed"})["Titel"] != "0":

            edit_embed1 = discord.Embed(
                title=config.DB.Abmelden.find_one({"_id": "embed"})["Titel"],
                description=config.DB.Abmelden.find_one({"_id": "embed"})["Beschreibung"],
                color=config.TRANPARENT
            )
        else:
            edit_embed1 = discord.Embed(
                title="Titel",
                description="Beschreibung",
                color=config.TRANPARENT
            )

        if config.DB.Abmelden.find_one({"_id": "embed"})["Image"] != "0":
            Image = config.DB.Abmelden.find_one({"_id": "embed"})["Image"]
            if urlcheck.is_url_image(Image):
                edit_embed1.set_image(url=config.DB.Abmelden.find_one({"_id": "embed"})["Image"])
            else:
                await interaction.followup.send("Die angegebene URL ist kein Link zu einem Png, Gif oder jepg Bild. Oder sie ist eine Discord URL. (Image error)", ephemeral=True)

        
        if config.DB.Abmelden.find_one({"_id": "embed"})["Thumbnail"] != "0":
            Thumbnail = config.DB.Abmelden.find_one({"_id": "embed"})["Thumbnail"]
            if urlcheck.is_url_image(Thumbnail):
                edit_embed1.set_thumbnail(url=config.DB.Abmelden.find_one({"_id": "embed"})["Thumbnail"])
            else:
                await interaction.followup.send("Die angegebene URL ist kein Link zu einem Png, Gif oder jepg Bild. Oder sie ist eine Discord URL. (Thumbnail error)", ephemeral=True)

    message = interaction.message.id            
    
    

    await interaction.followup.edit_message(message_id=message, embed=edit_embed1, view=view)




        