import discord
from discord.ext import commands
from discord.commands import slash_command, Option
from utils import embedcheck, logs, urlcheck, moderation
import config

from datetime import datetime, timedelta




class Base(commands.Cog):
    def __init__(self, bot):
        self.bot = bot




 
    @slash_command(description="Timeoute einen Member")
    async def timeout(
            self,ctx,
            member: discord.Member,
            reason: Option(str, "Der Grund"),
            minuten: Option(int, "Wie viele minuten soll der User getimeoutet werden?", max_value=59, required=False),
            stunden: Option(int, "Wie viele stunden soll der User getimeoutet werden?", max_value=23, required=False),
            tage: Option(int, "Wie viele tage soll der User getimeoutet werden?", max_value=6, required=False)
    ):
        tage = tage or 0
        stunden = stunden or 0
        minuten = minuten or 0
        if tage and stunden and minuten == 0:
            return ctx.respond("Du musst mindestens eine Zeit angeben", ephemeral=True)


        duration = timedelta(minutes=float(minuten), hours=float(stunden), days=float(tage))
        await moderation.timeout_until(member=member, timeouter=ctx.author, reason=reason, until=duration,)
        embed = discord.Embed(
            title="Timeout",
            description=f"**{member.mention}** wurde für {duration} getimeoutet",
            color=config.RED
        )
        await ctx.respond(embed=embed, ephemeral=True)

    @slash_command(description="Remove einen Timeout von einen Member")
    async def remove_timeout(
            self, ctx,
            member: discord.Member,
            reason: Option(str, "Der Grund")
    ):
        if(not member.timed_out):
            embed = discord.Embed(
                title="Remove Timeout",
                description=f"**{member.mention}** ist nicht getimeoutet",
                color=config.RED
            )
            await ctx.respond(embed=embed, ephemeral=True)
            return
        await member.remove_timeout(reason=reason)
        embed1 = discord.Embed(
            title="Remove Timeout",
            description=f"**{member.mention}** wurde enttimeoutet",
            color=config.GREEN
        )

        await moderation.remove_timeout(member=member, remover=ctx.author, reason=reason)
        await ctx.respond(embed=embed1, ephemeral=True)

def setup(bot):
    bot.add_cog(Base(bot))