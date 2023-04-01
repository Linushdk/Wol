import discord
from discord.ext import commands
from discord.commands import slash_command
import aiosqlite
import config
from datetime import datetime
from utils import logs, embedcheck



class Report(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @slash_command(description="Report")
    async def report(self, ctx, user: discord.Option(discord.Member)):
        await ctx.send_modal(modal=(ReasonModalReport(user, title=f"Report {user.name}")))






def setup(bot):
    bot.add_cog(Report(bot))


class ReasonModalReport(discord.ui.Modal):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(
            discord.ui.InputText(
                label="Reason",
                placeholder="Was hat der User gemacht?",
            ),
            *args,
            **kwargs
        )

    async def callback(self, interaction):
        embed =  discord.Embed(
            title="Report",
            description=f"Report erfolgreich gesendet\nDas Team wird sich demnächst um den Report kümmern\n\n**User:** {self.user.mention}\n**Reason:** {self.children[0].value}",
            color=config.KEKS_ORANGE
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        config.DB.reports.insert_one({"reporter": interaction.user.id, "reported": self.user.id, "reason": self.children[0].value, "status": "open", "time": f'{datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}'})
        reports = config.DB.reports.find_one({"reporter": interaction.user.id, "reported": self.user.id, "reason": self.children[0].value, "status": "open", "time": f'{datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}'})        
        time = datetime.strptime(reports['time'], '%m/%d/%Y, %H:%M:%S')
        
        await logs.create(title="Report", message=f"Ein Report wurde erstellt\n\n**Reporter:** {interaction.user.mention}\n**User:** {self.user.mention}\n**Reason:** `{self.children[0].value}`\n**Datum:** {discord.utils.format_dt(time, style='D')}", color=config.KEKS_ORANGE, guild=interaction.guild, db=config.DB.reports)