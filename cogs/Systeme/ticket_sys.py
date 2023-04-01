import discord
from discord.ext import commands
from discord.commands import slash_command, Option
import config
from utils import logs, urlcheck, embedcheck, ticket

IGNORE_CLOSE = {1081588196913184788, 1049368328067624990}

class ticket_sys(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):

        self.bot.add_view(TicketButton())
        self.bot.add_view(Options())    
        self.bot.add_view(AdminOptions())
        self.bot.add_view(CloseView()) 
        self.bot.add_view(OpenView())

    @slash_command()
    async def setticketmessage(self, ctx):
            
        if config.DB.tickets.find_one({"_id": "settings"})["close_category"] != "0" and config.DB.tickets.find_one({"_id": "settings"})["file_log_channel"] != "0":
            embed12 = discord.Embed(
                title="Titel",
                description="Beschreibung",
                color=config.TRANPARENT
            ) 
            
            await ctx.respond(embed=embed12, view=EmbedMessage(), ephemeral=True)
            config.DB.tickets.update_one({"_id": "embed"}, {"$set": {"Image": "0"}})
            config.DB.tickets.update_one({"_id": "embed"}, {"$set": {"Beschreibung": "0"}})
            config.DB.tickets.update_one({"_id": "embed"}, {"$set": {"Thumbnail": "0"}})
            config.DB.tickets.update_one({"_id": "embed"}, {"$set": {"Titel": "0"}})
            config.DB.tickets.update_one({"_id": "embed"}, {"$set": {"Farbe": "0"}})
        else:
            await ctx.respond("Du musst erst die Kategorie und den Log Channel setzen", ephemeral=True)
def setup(bot):
    bot.add_cog(ticket_sys(bot))

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

            
            if config.DB.tickets.find_one({"_id": "embed"})["Thumbnail"] != "0":
                Thumbnail = config.DB.tickets.find_one({"_id": "embed"})["Thumbnail"]
                if urlcheck.is_url_image(Thumbnail):
                    edit_embed1.set_thumbnail(url=config.DB.tickets.find_one({"_id": "embed"})["Thumbnail"])

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

            
            if config.DB.tickets.find_one({"_id": "embed"})["Thumbnail"] != "0":
                Thumbnail = config.DB.tickets.find_one({"_id": "embed"})["Thumbnail"]
                if urlcheck.is_url_image(Thumbnail):
                    edit_embed1.set_thumbnail(url=config.DB.tickets.find_one({"_id": "embed"})["Thumbnail"])
    
        settings = config.DB.tickets.find_one({"_id": "settings"})
        log_channel = settings["log_channel"]
        ticket_category = settings["ticket_category"]


        if log_channel and ticket_category == "0":
            return await interaction.response("Du musst zuerst die Ticket Kategorie und den Log channel setzen", ephemeral=True)
        else:    

            await interaction.channel.send(embed=edit_embed1, view=TicketButton())
            await interaction.response.send_message("Die Ticket Nachticht wurde gesendet", ephemeral=True)
            await logs.create(title='Tickets | Set Ticket Message', message=f'{interaction.user.mention} set the ticket message in {interaction.channel.mention}',
                                    color=config.GREEN, guild=interaction.guild, db=config.DB.tickets)

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

        config.DB.tickets.update_one({"_id": "embed"}, {"$set": {"Titel": self.children[0].value}})
        config.DB.tickets.update_one({"_id": "embed"}, {"$set": {"Beschreibung": self.children[1].value}})

        await embedcheck.embedcheck(interaction=interaction, view=EmbedMessage())
        
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
            config.DB.tickets.update_one({"_id": "embed"}, {"$set": {"Image": self.children[0].value}})
        if self.children[1].value != None:    
            config.DB.tickets.update_one({"_id": "embed"}, {"$set": {"Thumbnail": self.children[1].value}})

        await embedcheck.embedcheck(interaction=interaction, view=EmbedMessage()) 

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

        config.DB.tickets.update_one({"_id": "embed"}, {"$set": {"Farbe": self.children[0].value}})

        await embedcheck.embedcheck(interaction=interaction, view=EmbedMessage())
        
class TicketButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Ticket", style=discord.ButtonStyle.green, custom_id="öffnen")
    async def button_callback1(self, button, interaction):
        
        result = config.DB.tickets.find_one({"user": interaction.user.id, "status": "offen"})
        result2 = config.DB.tickets.find_one({"user": interaction.user.id, "status": "geschlossen"})
        if result is None and result2 is None:
            await interaction.response.send_modal(modal=(ReasonModal(title="Ticket Reason")))

        else:
            try:
                channel = interaction.guild.get_channel(result["ticket_channel"])
            except:
                channel = interaction.guild.get_channel(result2["ticket_channel"])
            await interaction.response.send_message(f"Du hast bereits ein Ticket offen! Hier kannst du weiterschreiben {channel.mention}", ephemeral=True)

class ReasonModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs):
        super().__init__(
            discord.ui.InputText(
                label="Reason",
                placeholder="Warum öffnest du ein Ticket?"
            ),
            *args,
            **kwargs
        )
    async def callback(self, interaction):
        
        await ticket.create_ticket(creater=interaction.user, grund=self.children[0].value, db=config.DB.tickets)      
        embed = discord.Embed(
            title=f"Ticket - {interaction.user.name}",
            description=f"Das Team wird in kürze auf dich zukommen. Um Infos aufzufordern gehe in das auswahl menü",
            color=config.RED
        )
        embed.set_footer(text=f"Bitte sei geduldig und Pinge niemanden grundlos. Außnutzung des Tickets kann bestraft werden!")
        ticket_channel = interaction.guild.get_channel(config.DB.tickets.find_one({"user": interaction.user.id, "status": "offen"})["ticket_channel"])       
        await ticket_channel.send(embed=embed, view=Options())

        embed2 = discord.Embed(
            title="Ticket wurde erfolgreich geöffnet",
            description=f"Die Moderatoren werden in kürze auf dich zukommen. Hier kannst du schon mal dein Problem und mitteilen:\n{ticket_channel.mention}",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed2, ephemeral=True)
        
class Options(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    options2 = [
        discord.SelectOption(label="Reason", description="Rufe den Grund des Tickets auf."),
        discord.SelectOption(label="Add User", description="Füge einen user dem channel hinzu."),
        discord.SelectOption(label="Remove User", description="Entferne einen user aus dem channel."),
        discord.SelectOption(label="Admin Options", description="Rufe als Moderator Admin commands auf."),
        discord.SelectOption(label="Transcript", description="Lass dir den Chatverlauf als Datei senden"),
        discord.SelectOption(label="Close", description="Schließe das Ticket. Somit ist das gespräch beendet")
                ]

    @discord.ui.select(
        min_values=1,
        max_values=1,
        placeholder="Triff eine Auswahl",
        options=options2,
        custom_id="TicketsOptions"
    )
       
    async def select_callback(self, select, interaction):
        
        ticket_doc = config.DB.tickets.find_one({"ticket_channel": interaction.channel.id})
        grund  = ticket_doc["grund"]
     
        if "Reason" in select.values:

            embed = discord.Embed(
                title="Ticket - Grund",
                description=f"Das Ticket wurde wegen folgendem Grund aufgerufen:\n```{grund}```",
                color=config.TRANPARENT
            )

            await interaction.response.send_message(embed=embed, ephemeral=True)

        if "Add User" in select.values:

            embed2 = discord.Embed(
                description="Wähle den User aus, den du zum Ticket hinzufügen möchtest",
                color=config.GREEN
            )

            embed2.set_author(name="User zum Ticket hinzufügen")

            await interaction.response.send_message(embed=embed2, view=AddUser(), ephemeral=True)

        if "Remove User" in select.values:

            embed12 = discord.Embed(
                description="Wähle den User aus, den du aus dem Ticket entfernen möchtest",
                color=config.RED
            )

            embed12.set_author(name="User aus dem Ticket entfernen")
            await interaction.response.send_message(embed=embed12, view=RemoveUser(), ephemeral=True)

        if "Admin Options" in select.values:

            
            if interaction.user.guild_permissions.administrator == False:
                return await interaction.response.send_message("Du hast keine Admin Rechte!", ephemeral=True)            
            
            embed3 = discord.Embed(
                title="Admin Options",
                description="Du kannst nun unten im Menü verschiedene Admin Options ausführen",
                color=config.TRANPARENT
            )

            await interaction.response.send_message(embed=embed3 ,view=AdminOptions(), ephemeral=True)       
        
        if "Transcript" in select.values:
            await ticket.transcript(interaction=interaction)

        if "Close" in select.values:
            embed5 = discord.Embed(
                title="__SCHLIEßEN__",
                description="Willst du wirklich das Ticket schließen?\nModerator wissen dann das du keine Fragen mehr hast und könnnen es dann löschen. Du kannst dir noch im selection menü ein Transcript anfordern.",
                color=config.RED
             )        
            await interaction.response.send_message(embed=embed5, view=CloseView())
            
class AdminOptions(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    
    adminoptions = [
        discord.SelectOption(label="Claim", description="Beanspruche das Ticket"),
        discord.SelectOption(label="Delete", description="Arichiviere das Ticket")
    ]

    @discord.ui.select(
        min_values=1,
        max_values=1,
        placeholder="Triff eine Auswahl",
        options=adminoptions,
        custom_id="AdminOptions"
    )

    async def select_callback(self, select, interaction):
        if "Claim" in select.values:
            
            embed6 = discord.Embed(
                title="**Ticket wurde beansprucht**",
                description=f"{interaction.user} ist jetzt für dich zuständig.",
                color=config.TRANPARENT
            )
            embed6.set_thumbnail(url=interaction.user.display_avatar.url)
            await interaction.response.send_message("Ticket wurde beansprucht", ephemeral=True)
            await interaction.channel.send(embed=embed6)
            await logs.create(title='Ticket | Claim', message=f'{interaction.user.mention} claimed a ticket({interaction.channel.mention})', color=config.GREEN, guild=interaction.guild, db=config.DB.tickets)
        if "Delete" in select.values:
            
            await ticket.delete_ticket(interaction=interaction, db=config.DB.tickets)

class CloseView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)       
    
    @discord.ui.button(label="Schließen", style=discord.ButtonStyle.red, custom_id="close")
    async def button_callback1(self, button, interaction):
        
        embed7 = discord.Embed(
                            title="**Ticket wurde geschlossen**",
                            description=f"Das Ticket wurde von {interaction.user} geschlossen.",
                            color=config.RED
                        )

        embed9 = discord.Embed(
            title="__ÖFFNEN__",
            description="Willst du wirklich das Ticket wieder öffnen?\nWenn du das Ticket wieder öffnest kannst du noch eine Frage stellen.",
            color=config.GREEN
        )
        await interaction.response.edit_message(embed=embed9, view=OpenView())
        await interaction.followup.send(embed=embed7)
        await ticket.close_ticket(interaction=interaction, db=config.DB.tickets)
        
class OpenView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="Öffnen", style=discord.ButtonStyle.green, custom_id="open")
    async def button_callback(self, button, interaction):
        
        embed8 = discord.Embed(
            title="**Ticket wurde wieder geöffnet**",
            description=f"Das Ticket wurde von {interaction.user} wieder geöffnet.",
                color=config.GREEN
                    )
        await ticket.reopen_ticket(interaction=interaction, db=config.DB.tickets)       
        button.disabled = True
        await interaction.response.edit_message(view=self)
        await interaction.followup.send(embed=embed8)

class AddUser(discord.ui.View):
    @discord.ui.user_select(custom_id="add_user", placeholder="Wähle einen User aus", min_values=1, max_values=1)
    async def user_select(self, select, interaction):
        await ticket.add_user(interaction=interaction, user=select.values[0], db=config.DB.tickets)

class RemoveUser(discord.ui.View):
    @discord.ui.user_select(custom_id="remove_user", placeholder="Wähle einen User aus", min_values=1, max_values=1)
    async def user1_select(self, select, interaction):
        await ticket.remove_user(interaction=interaction, user=select.values[0], db=config.DB.tickets)        