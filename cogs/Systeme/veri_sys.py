import discord
from discord.ext import commands
from discord.commands import slash_command
import random
from discord.ui import View, button
import config
import embeds


class veri_sys(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @slash_command(description="Regeln")
    async def regeln(self, ctx):
        await ctx.send(file = embeds.file, embed=embeds.offi_Regeln, view=RegelnGelesen())
        await ctx.respond("Regeln erfolgreich gesendet", ephemeral=True)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = await self.bot.get_channel(1049369309534748724)
        await channel.send(f"**Hey** {member.mention} Das **Wolkenlos Team** heißt dich hier herzllich Willkommen!\nDank dir sind wir jetzt **{format(len(member.guild.members))}wolkenlose Mitglieder.**")


def setup(bot):
    bot.add_cog(veri_sys(bot))

class RegelnGelesen(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Akzeptieren", style=discord.ButtonStyle.green, emoji="<:Richtig:1008298064248832061>")
    async def button_callback_Akzeptieren(self, regelnb, interaction):

        random2 = ""

        liste = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
                 "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n",
                 "o", "b", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "1", "2", "3", "4", "5", "6", "7", "8",
                 "9"]

        for x in range(6):
            random1 = random.choice(liste)
            random2 += random1

        embed3 = discord.Embed(
            title="Du bist bereits verifiziert!",
            description="Du bist schon verifizierter Member dieses Servers",
            color=config.TRANPARENT
        )
        role = interaction.guild.get_role(1038850092154753075)
        if role in interaction.user.roles:
            await interaction.response.send_message(embed=embed3, ephemeral=True)
            return

        random3 = random2

        await interaction.response.send_modal(modal=VertifyModal(random3, title=f"Gebe unten den Code ein: {random2}"))


    @discord.ui.button(label="Hilfe", style=discord.ButtonStyle.red, emoji="<:Support:1008103053427212339>")
    async def button_callback_Hilfe(self, hilfe, interaction):

        embedhife = discord.Embed(
            title="Melde dich im Support",
            description="> Melde dich im Support um dort dein Anliegen zu stellen. Um dies zu tun, klicke auf die folgenden verlinkten Chats & Voicekanälen. Bei Gelegenheit kannst du auch einen zuständigen Admin kontaktieren. Bitte tu das jedoch bitte auf dem CaveMC.net-Discordserver.",
            color=config.TRANPARENT
        )

        await interaction.response.send_message(embed=embedhife, ephemeral=True)


class VertifyModal (discord.ui.Modal):
    def __init__(self, random3, *args, **kwargs):


        super().__init__(
            discord.ui.InputText(
                label=f"Beachte groß und klein schreibung",
                placeholder=f"Hier den Code {random3} eingeben",
            ),
            *args,
            **kwargs
        )
        self.random3 = random3
    async def callback(self, interaction:discord.Interaction):

        if self.children[0].value == self.random3:

            embed = discord.Embed(
                title="Du hast dich erfolgreich verifiziert!",
                description="Du hast nun alle nötigen Rechte um mit anderen Mitgliedern zu schreiben und dich hier aus zu toben viel spass!",
                color=config.TRANPARENT
            )

            await interaction.response.send_message(embed=embed)



        else:

            liste2 = ["420", "69"]
            random4 = random.choice(liste2)
            print(random4)

            embed2 = discord.Embed(
                title=f"ERROR {random4}",
                description="> Du hast den Flaschen Code eingegeben. Bitte verifiziere dich erneut und gebe den richtigen Code ein.",
                color=config.RED
            )

            await interaction.response.send_message(embed=embed2)