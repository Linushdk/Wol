import discord
from discord.ext import commands
from discord.commands import slash_command, Option, user_command, message_command
import config
import embeds
from datetime import datetime, timedelta
import secrets

class Warn(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @slash_command(description="Warn")
    async def warn(self, ctx, user: discord.Option(discord.Member)):
        await ctx.send_modal(modal=(Reason(user, title=f"Warn {user.name}")))


    @slash_command(description="Warns")
    async def warns(self, ctx, user: discord.Option(discord.Member)):
        warns = config.DB.warns.find({"user": user.id})
        embed = discord.Embed(title=f"Warns von {user.name}", color=config.TRANPARENT)
        warn_num = 1
        for warn in warns:
            time = datetime.strptime(warn['date'], '%m/%d/%Y, %H:%M:%S')
            embed.add_field(name=f"{warn_num}. Warn", value=f"**Warner**: {self.bot.get_user(warn['warner']).name}\n**Grund**: `{warn['reason']}`\n**Datum**: {discord.utils.format_dt(time, style='R')}", inline=False)
            warn_num += 1
        embed.set_author(name=f"{ctx.author.name}", icon_url=ctx.author.avatar.url)
        await ctx.respond(embed=embed)

    @slash_command(description="Delete Warns")
    async def deletewarns(self, ctx, user: discord.Option(discord.Member)):
        embed2 = discord.Embed(
            color=config.KEKS_ORANGE
        )
        embed2.set_thumbnail(url=user.avatar.url)
        embed2.set_author(name=f"{ctx.author.name}", icon_url=ctx.author.avatar.url)

        warns = config.DB.warns.find({"user": user.id})
        warn_num = 1
        for warn in warns:
            time = datetime.strptime(warn['date'], '%m/%d/%Y, %H:%M:%S')
            embed2.add_field(name=f"{warn_num}. Warn", value=f"**Warner**: {self.bot.get_user(warn['warner']).name}\n**Grund**: `{warn['reason']}`\n**Datum**: {discord.utils.format_dt(time, style='R')}", inline=False)
            warn_num += 1
        if warn_num == 1:
            embed2.insert_field_at(name="Keine Warns", value="Dieser User hat eine Warns", inline=False, index=0)
        else: 
            embed2.insert_field_at(name="Warns löschen", value="Wähle die Warns im Select Menü aus um sie zu löschen", inline=False, index=0)
        await ctx.respond(embed=embed2, view=WarnsView(user, warns))

    @user_command(name="Warn", description="Warn")
    async def warn1(self, ctx, user: discord.Option(discord.Member)):
        await ctx.send_modal(modal=(Reason(user, title=f"Warn {user.name}")))

    @user_command(name="Warns", description="Warns")
    async def warns1(self, ctx, user: discord.Option(discord.Member)):
        warns = config.DB.warns.find({"user": user.id})
        embed = discord.Embed(title=f"Warns von {user.name}", color=config.TRANPARENT)
        warn_num = 1
        for warn in warns:
            time = datetime.strptime(warn['date'], '%m/%d/%Y, %H:%M:%S')
            embed.add_field(name=f"{warn_num}. Warn", value=f"**Warner**: {self.bot.get_user(warn['warner']).name}\n**Grund**: `{warn['reason']}`\n**Datum**: {discord.utils.format_dt(time, style='R')}", inline=False)
            warn_num += 1
        embed.set_author(name=f"{ctx.author.name}", icon_url=ctx.author.avatar.url)
        await ctx.respond(embed=embed)

    @user_command(name="Warns Löschen", description="Delete Warns")
    async def deletewarns1(self, ctx, user: discord.Option(discord.Member)):
        embed2 = discord.Embed(
            color=config.KEKS_ORANGE
        )
        embed2.set_thumbnail(url=user.avatar.url)
        embed2.set_author(name=f"{ctx.author.name}", icon_url=ctx.author.avatar.url)

        warns = config.DB.warns.find({"user": user.id})
        warn_num = 1
        for warn in warns:
            time = datetime.strptime(warn['date'], '%m/%d/%Y, %H:%M:%S')
            embed2.add_field(name=f"{warn_num}. Warn", value=f"**Warner**: {self.bot.get_user(warn['warner']).name}\n**Grund**: `{warn['reason']}`\n**Datum**: {discord.utils.format_dt(time, style='R')}", inline=False)
            warn_num += 1
        if warn_num == 1:
            embed2.insert_field_at(name="Keine Warns", value="Dieser User hat eine Warns", inline=False, index=0)
        else: 
            embed2.insert_field_at(name="Warns löschen", value="Wähle die Warns im Select Menü aus um sie zu löschen", inline=False, index=0)
        await ctx.respond(embed=embed2, view=WarnsView(user, warns))

def setup(bot):
    bot.add_cog(Warn(bot))

class WarnsView(discord.ui.View):
    def __init__(self, user, warns):

        super().__init__()
        self.add_item(WarnSelect(user, warns))

class WarnSelect(discord.ui.Select):
    def __init__(self, user, warns):
        self.user = user
        self.warns = warns
        warns = config.DB.warns.find({"user": self.user.id})
        options = []
        warns_num = 1
        for warn in warns:
            options.append(discord.SelectOption(label=f"{warns_num}"))
            warns_num += 1
        if warns_num == 1:
            options.append(discord.SelectOption(label="Dieser User hat Kein Warn"))

        super().__init__(
            placeholder='Welcher Warn',
            max_values=1,
            min_values=1,
            options=options
        )
    async def callback(self, interaction: discord.Interaction):
        if "Dieser User hat Kein Warn" in self.values:
            return await interaction.response.send_message("Dieser User hat Kein Warn", ephemeral=True)
        selection = int(self.values[0])
        warns = config.DB.warns.find({"user": self.user.id})
        warn_num = 0
        for warn in warns:
            warn_num += 1
            if warn_num == selection:
                config.DB.warns.delete_one({"_id": f"{warn['_id']}"})
                embed2 = discord.Embed(
                    color=config.KEKS_ORANGE
                )
                embed2.set_thumbnail(url=self.user.display_avatar.url)
                warns = config.DB.warns.find({"user": self.user.id})
                user = self.user.guild.get_member(warn['user'])
                embed2.set_author(name=f"{user}", icon_url=user.display_avatar.url)
                embed2.set_author(name=f"{interaction.user.name}", icon_url=interaction.user.display_avatar.url)

                warner = self.user.guild.get_member(warn['warner'])
                warn_num = 1
                for warn in warns:
                    time = datetime.strptime(warn['date'], '%m/%d/%Y, %H:%M:%S')
                    embed2.add_field(name=f"{warn_num}. Warn", value=f"**Warner**: {warner.mention}\n**Grund**: `{warn['reason']}`\n**Datum**: {discord.utils.format_dt(time, style='R')}", inline=False)
                    warn_num += 1
                if warn_num == 1:
                    embed2.insert_field_at(name="Keine Warns", value="Dieser User hat eine Warns", inline=False, index=0)
                else: 
                    embed2.insert_field_at(name="Warns löschen", value="Wähle die Warns im Select Menü aus um sie zu löschen", inline=False, index=0)

                await interaction.response.edit_message(embed=embed2, view=WarnsView(self.user, self.warns))

class Reason(discord.ui.Modal):
    def __init__(self, user, *args, **kwargs):
        self.user = user

        super().__init__(
            discord.ui.InputText(
                label="Warngrund",
                placeholder="Dm Werbung",
            ),
            *args,
            **kwargs
        )

    async def callback(self, interaction):
    
        await interaction.response.send_message("Warnung war erfolgreich", ephemeral=True)     
        config.DB.warns.insert_one({"user": self.user.id, "warner": interaction.user.id, "date": f'{datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}', "reason": self.children[0].value, "_id": secrets.token_urlsafe(40)})
        
        warns = config.DB.warns.find({"user": self.user.id})
        warn_num = 0
        for warn in warns:
            warn_num += 1
        if warn_num >= 3 and warn_num < 4:
            duration = timedelta(days=4)
            await self.user.timeout_for(duration, reason="3 Warns")
        if warn_num >= 5:
            await self.user.ban(reason="5 Warns")