import discord
from discord.ext import commands, tasks
from discord.commands import slash_command, Option
import config
from utils import urlcheck, embedcheck, logs
from datetime import datetime



class Abmelden(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
 

    @commands.Cog.listener()
    async def on_ready(self):
        self.abmelden.start()

    @tasks.loop(seconds=1)
    async def abmelden(self):
        for i in config.DB.Abmelden.find({"Zeit | Bis": datetime.now().strftime("%m/%d/%Y")}):
            user = self.bot.get_user(i["user"])
            await user.remove_roles(discord.utils.get(self.bot.get_guild(1073330559977267240).roles, id=1089572990246727821))
            config.DB.Abmelden.delete_one({"user": i["user"]})
            time_form = datetime.strptime(i['Zeit | Von'], "%m/%d/%Y")
            time_to = datetime.strptime(i['Zeit | Bis'], "%m/%d/%Y")
        await logs.create(title="Anmeldung", message=f"**User:** {user.mention}\n**Von:** {discord.utils.format_dt(time_form, style='D')}\n**Bis:** {discord.utils.format_dt(time_to, style='D')}", color=config.GREEN, db=config.DB.Abmelden, guild=self.bot.get_guild(1049368328067624990))


    
    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(AbmeldeButton())


    @slash_command()
    async def anmelden(self, ctx, user: Option(discord.Member)):
        await user.remove_roles(discord.utils.get(ctx.guild.roles, id=1089572990246727821))
        i = config.DB.Abmelden.find_one({"user": user.id})
        config.DB.Abmelden.update_one({"user": user.id}, {"$set": {"Zeit | Bis": datetime.now().strftime("%m/%d/%Y")}})
        
        time_form = datetime.strptime(i['Zeit | Von'], "%m/%d/%Y")
        time_to = datetime.strptime(i['Zeit | Bis'], "%m/%d/%Y")
        await logs.create(title="Anmeldung", message=f"**User:** {user.mention}\n**Grund:** `{i['Grund']}`\n**Von:** {discord.utils.format_dt(time_form, style='D')}\n**Bis:** {discord.utils.format_dt(time_to, style='D')}", color=config.GREEN, db=config.DB.Abmelden, guild=ctx.guild)
        await ctx.respond(f"{user.mention} wurde erfolgreich angemeldet.", ephemeral=True)


    @slash_command()
    async def setabmeldemessage(self, ctx):
            
        embed12 = discord.Embed(
            title="Titel",
            description="Beschreibung",
            color=config.TRANPARENT
        ) 

        if config.DB.Abmelden.find_one({"_id": "settings"})["log_channel"] != "0":

            await ctx.respond(embed=embed12, view=EmbedMessage(), ephemeral=True)
            config.DB.Abmelden.update_one({"_id": "embed"}, {"$set": {"Image": "0"}})
            config.DB.Abmelden.update_one({"_id": "embed"}, {"$set": {"Beschreibung": "0"}})
            config.DB.Abmelden.update_one({"_id": "embed"}, {"$set": {"Thumbnail": "0"}})
            config.DB.Abmelden.update_one({"_id": "embed"}, {"$set": {"Titel": "0"}})
            config.DB.Abmelden.update_one({"_id": "embed"}, {"$set": {"Farbe": "0"}})
        else:
            await ctx.respond("Du musst zuerst einen Log Channel festlegen.", ephemeral=True)
 

    @slash_command()
    async def abmeldungen(selfe, ctx, user: Option(discord.Member)):
        result = config.DB.Abmelden.find({"user": user.id})

        embed = discord.Embed(
            color=config.KEKS_ORANGE
        )
        embed.set_author(name=f"Abmeldungen von {user.name}", icon_url=user.display_avatar.url)
        embed.set_thumbnail(url=user.display_avatar.url)

        num = 1
        for res in result:
            time_from = datetime.strptime(res["Zeit | Von"], "%m/%d/%Y")
            time_to = datetime.strptime(res["Zeit | Bis"], "%m/%d/%Y")
            embed.add_field(name=f"Abmeldung {num}", value=f"**Grund:** {res['Grund']}\n**Von:** {discord.utils.format_dt(time_from, style='D')}\n**Bis.** {discord.utils.format_dt(time_to, style='D')}", inline=False)
            num += 1
        await ctx.respond(embed=embed, ephemeral=True)





def setup(bot):
    bot.add_cog(Abmelden(bot))


class EmbedMessage(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="Text ändern", style=discord.ButtonStyle.green, custom_id="Text_ändern")
    async def button_callback1(self, button, interaction):

        await interaction.response.send_modal(modal=(TextÄndern(title="Ändere deinen Text")))


    @discord.ui.button(label="Bild hinzufügen", style=discord.ButtonStyle.green, custom_id="Bild_hinzufügen")
    async def button_callback2(self, button, interaction):

        await interaction.response.send_modal(modal=(BildHinzufügen(title="Füge ein Embed Fled hinzu")))

    @discord.ui.button(label="Farbe ändern", style=discord.ButtonStyle.green, custom_id="Farbe_ändern")
    async def button_callback3(self, button, interaction):
            
            await interaction.response.send_modal(modal=(FarbeÄndern(title="Füge ein Embed Fled hinzu")))

    @discord.ui.button(label="Embed senden", style=discord.ButtonStyle.green, custom_id="Embed_senden")
    async def button_callback4(self, button, interaction):

        await interaction.response.defer()
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

            
            if config.DB.Abmelden.find_one({"_id": "embed"})["Thumbnail"] != "0":
                Thumbnail = config.DB.Abmelden.find_one({"_id": "embed"})["Thumbnail"]
                if urlcheck.is_url_image(Thumbnail):
                    edit_embed1.set_thumbnail(url=config.DB.Abmelden.find_one({"_id": "embed"})["Thumbnail"])

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

            
            if config.DB.Abmelden.find_one({"_id": "embed"})["Thumbnail"] != "0":
                Thumbnail = config.DB.Abmelden.find_one({"_id": "embed"})["Thumbnail"]
                if urlcheck.is_url_image(Thumbnail):
                    edit_embed1.set_thumbnail(url=config.DB.Abmelden.find_one({"_id": "embed"})["Thumbnail"])
    
   

        await interaction.channel.send(embed=edit_embed1, view=AbmeldeButton())




class TextÄndern(discord.ui.Modal):
    def __init__(self, *args, **kwargs):
        super().__init__(
            discord.ui.InputText(
                label="Embed Titel",
                placeholder="Der Titel von deinem Embed"
            ),
            discord.ui.InputText(
                label="Embed Beschreibung",
                placeholder="Die Beschreibung von dem Embed",
                style=discord.InputTextStyle.long
            ),
            *args,
            **kwargs
        )

    async def callback(self, interaction):

        config.DB.Abmelden.update_one({"_id": "embed"}, {"$set": {"Titel": self.children[0].value}})
        config.DB.Abmelden.update_one({"_id": "embed"}, {"$set": {"Beschreibung": self.children[1].value}})

        await embedcheck.embedcheck_Abmelden(interaction=interaction, view=EmbedMessage())
        
class BildHinzufügen(discord.ui.Modal):
    def __init__(self, *args, **kwargs):
        super().__init__(
            discord.ui.InputText(
                label="Embed Bild",
                placeholder="Der Link zum Bild von dem Embed(Keine Discord Links)",
                style=discord.InputTextStyle.long,
                required=False
            ),
            discord.ui.InputText(
                label="Embed Thumbnail",
                placeholder="Der Link zum Thumbnail von dem Embed(Keine Discord Links)",
                style=discord.InputTextStyle.long,
                required=False
            ),
            *args,
            **kwargs
        )
    async def callback(self, interaction):
        if self.children[0].value != None:
            config.DB.Abmelden.update_one({"_id": "embed"}, {"$set": {"Image": self.children[0].value}})
        if self.children[1].value != None:    
            config.DB.Abmelden.update_one({"_id": "embed"}, {"$set": {"Thumbnail": self.children[1].value}})

        await embedcheck.embedcheck_Abmelden(interaction=interaction, view=EmbedMessage()) 


class FarbeÄndern(discord.ui.Modal):
    def __init__(self, *args, **kwargs):
        super().__init__(
            discord.ui.InputText(
                label="Embed Farbe",
                placeholder="Der Hexcode der Farbe von dem Embed(z.B. ff0000) Achtung kein #",
                style=discord.InputTextStyle.long
            ),
            *args,
            **kwargs
        )
    async def callback(self, interaction):

        config.DB.Abmelden.update_one({"_id": "embed"}, {"$set": {"Farbe": self.children[0].value}})

        await embedcheck.embedcheck_Abmelden(interaction=interaction, view=EmbedMessage())


class AbmeldeButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Abmelden", style=discord.ButtonStyle.danger, custom_id="Abmelden")
    async def button_callback1(self, button, interaction):

        result = config.DB.Abmelden.find({"user": interaction.user.id})
        list = []

        for x in result:
            list.append(datetime.strptime(x["Zeit | Bis"], '%m/%d/%Y'))
        list.sort(reverse=True)

        time_1 = datetime.strptime(list[0].strftime('%m/%d/%Y'), '%m/%d/%Y') 

        if len(list) == 0:        
            return await interaction.response.send_modal(modal=(AbmeldeModal(title="Abmelde Grund")))
        
        if datetime.now() < time_1:
            await interaction.response.send_message("Du bist bereits abgemeldet", ephemeral=True)
        else:
            return await interaction.response.send_modal(modal=(AbmeldeModal(title="Abmelde Grund")))



class AbmeldeModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs):
        super().__init__(
            discord.ui.InputText(
                label="Grund",
                placeholder="Ich bin im Urlaub",
                style=discord.InputTextStyle.long,
                required=False
            ),
            discord.ui.InputText(
                label="Zeit | Von",
                placeholder="Monat(01)/Tag(31)/Jahr(2024)",
                style=discord.InputTextStyle.short,
                required=True
            ),
            discord.ui.InputText(
                label="Zeit | Bis",
                placeholder="Monat(01)/Tag(31)/Jahr(2024)",
                style=discord.InputTextStyle.short,
                required=True
            ),
            *args,
            **kwargs
        )

    async def callback(self, interaction):
        


        try:
            time_from = datetime.strptime(self.children[1].value, '%m/%d/%Y')
            time_to = datetime.strptime(self.children[2].value, '%m/%d/%Y')
        except:
            
            embed = discord.Embed(
                title="Error",
                description="Bitte überprüfe deine Eingaben\n\n**Beispiel:**\nZeit | Von: 01/31/2024\nZeit | Bis: 01/31/2025\n\n**Achtung:**\nDu musst das Datum im Format Monat(01)/Tag(31)/Jahr(2024) angeben\n\nOder du hast ein falsches Datum angegeben und das Datum(Bis) muss Nach dem Datum(Von) sein",
                color=config.RED
                )       
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
            

        
        if time_from > time_to:
            embed = discord.Embed(
                title="Error",
                description="Bitte überprüfe deine Eingaben\n\n**Beispiel:**\nZeit | Von: 01/31/2024\nZeit | Bis: 01/31/2025\n\n**Achtung:**\nDu musst das Datum im Format Monat(01)/Tag(31)/Jahr(2024) angeben\n\nOder du hast ein falsches Datum angegeben und das Datum(Bis) muss Nach dem Datum(Von) sein"
                )       
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        config.DB.Abmelden.insert_one({"user": interaction.user.id, "Grund": f"{self.children[0].value}", "Zeit | Von": self.children[1].value, "Zeit | Bis": self.children[2].value})
        AbmeldeRole = discord.utils.get(interaction.guild.roles, id=1089572990246727821)
        await interaction.user.add_roles(AbmeldeRole)
        await interaction.response.send_message("Du hast dich erfolgreich abgemeldet", ephemeral=True)
        await logs.create(title="Abmeldung", message=f"**User:** {interaction.user.mention}\n**Grund:** `{self.children[0].value}`\n**Von:** {discord.utils.format_dt(time_from, style='R')}\n**Bis:** {discord.utils.format_dt(time_to, style='R')}", color=config.GREEN, db=config.DB.Abmelden, guild=interaction.guild)
