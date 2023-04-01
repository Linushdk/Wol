import discord
from discord.ext import commands
from discord.commands import slash_command, user_command, Option
from datetime import datetime
import config
from discord.utils import basic_autocomplete

async def unban_autocomplete(ctx: discord.AutocompleteContext):
    x = await ctx.interaction.guild.bans().flatten()
    x = [f'{y.user}' for y in x]
    return x

class BanSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @slash_command()
    async def ban(self, ctx, user: discord.Option(discord.Member), reason: discord.Option(str, description="Grund")):
        config.DB.bans.insert_one({"user": user.id, "ban_reason": reason, "ban_date": datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), "banner": ctx.author.id, "unban_date": "None", "unban_reason": "None", "unbanner": "None"})
        await user.ban(reason=reason)
        
        embed = discord.Embed(title="Ban", description=f"{user.mention} wurde gebannt", color=config.RED)

        await ctx.respond(embed=embed, ephemeral=True)



    @slash_command(name="unban", description="")
    @discord.default_permissions(ban_members=True)
    async def _unban(self, ctx: discord.ApplicationContext, member: discord.Option(str, autocomplete=basic_autocomplete(unban_autocomplete)), reason: discord.Option(str, description="Grund")):
        async for ban in ctx.guild.bans():
            
            embed2 = discord.Embed(title="Unban", description=f"{ban.user.mention} wurde entbannt", color=config.GREEN)
            embed3 = discord.Embed(title="Unban", description=f"{ban.user.mention} konnte nicht entbannt werden", color=config.RED)
            if f'{ban.user}' == f'{member}':
                await ctx.guild.unban(ban.user, reason=reason)
                config.DB.bans.update_one({"user": ban.user.id}, {"$set": {"unban_date": datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), "unban_reason": reason, "unbanner": ctx.author.id}})
                return await ctx.respond(embed=embed2, ephemeral=True)

            else:
                continue

        return await ctx.respond(embed=embed3, ephemeral=True)
    
    @slash_command(name="banlist", description="Zeigt die Bannliste")
    @discord.default_permissions(ban_members=True)
    async def _banlist(self, ctx: discord.ApplicationContext):
        bans = config.DB.bans.find()
        embed = discord.Embed(title="Banliste", color=config.KEKS_ORANGE)
        for ban in bans:
            embed.add_field(name=f"{self.bot.get_user(ban['user'])}", value=f"Grund: {ban['ban_reason']} | Banner: {self.bot.get_user(ban['banner'])} | Datum: {ban['ban_date']}", inline=False)
        await ctx.respond(embed=embed, ephemeral=True)
    
    @user_command(name="Ban", description="Bannt einen User")
    @discord.default_permissions(ban_members=True)
    async def _ban(self, ctx: discord.ApplicationContext, member: discord.Option(discord.Member)):	
        config.DB.bans.insert_one({"user": member.id, "ban_reason": "None", "ban_date": datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), "banner": ctx.author.id, "unban_date": "None", "unban_reason": "None", "unbanner": "None"})
        await ctx.send_modal(modal=BanModal(member, title="Ban Reason",))
        await ctx.respond("Bitte den Grund angeben!", ephemeral=True)

def setup(bot):
    bot.add_cog(BanSystem(bot))

class BanModal(discord.ui.Modal):
    def __init__(self, member, *args, **kwargs):
        self.member = member
        super().__init__(
            discord.ui.InputText(
                label="Reason",
                placeholder="Spam"
            ),

            *args,
            **kwargs
        )

    async def callback(self, interaction):
        embed = discord.Embed(title="Ban", description=f"{self.member.mention} wurde gebannt", color=config.RED) 
        config.DB.bans.update_one({"user": self.member.id}, {"$set": {"ban_reason": self.children[0].value}})
        await self.member.ban(reason=self.children[0].value)
        await interaction.response.send_message(embed=embed, ephemeral=True)


