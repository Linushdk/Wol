import discord
from datetime import datetime, timedelta
from utils import logs
import config



async def timeout_until(timeouter: discord.Member, member: discord.Member, reason: str, until: timedelta):
    await member.timeout_for(until, reason=reason)
    await logs.create(title="Timeout", message=f"**User:** {member.mention} | {member.name}\n**Timeouter:** {timeouter.mention}\n**Grund:** `{reason}`\n**Zeit:** {until}", color=config.RED, guild=member.guild, db=config.DB.timeouts)
    config.DB.timeouts.insert_one({"user": member.id, "reason": reason, "timeouter": timeouter.id, "time": f"{until}", "Datum": f"{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')}"})

async def remove_timeout(member: discord.Member, reason: str, remover: discord.Member):
        result = config.DB.timeouts.find({"user": member.id})
        list = []
        for x in result:
            list.append(datetime.strptime(x["Datum"], '%m/%d/%Y, %H:%M:%S'))
        list.sort(reverse=True)
        value = config.DB.timeouts.find_one({"Datum": list[0].strftime('%m/%d/%Y, %H:%M:%S')})
        config.DB.timeouts.update_one({"_id": value["_id"]}, {"$set": {"remove_Grund": f"{reason}", "remove_Datum": f"{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')}", "remover": f"{member.id}"}})
        grund = value["reason"]
        timeouter = member.guild.get_member(value["timeouter"])
        await member.remove_timeout(reason=reason)
        await logs.create(title="Remove Timeout", message=f"**User:** {member.mention} | {member.name}\n**Timeouter:** {timeouter.mention}\n**Remove Grund:** `{reason}`\n**Timeout Grund:** `{grund}`", color=config.GREEN, guild=member.guild, db=config.DB.timeouts)

async def ban(member: discord.Member, reason: str, banner: discord.Member):
    await member.ban(reason=reason)
    await logs.create(title="Ban", message=f"**User:** {member.mention} | {member.name}\n**Bannender:** {banner}\n**Grund:** `{reason}`", color=config.RED, guild=member.guild, db=config.DB.bans)