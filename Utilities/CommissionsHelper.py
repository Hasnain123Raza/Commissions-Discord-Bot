import re
from math import floor
from discord import Embed, Color
from discord.ext.commands.errors import CommandInvokeError
from tinydb import Query
from tinydb.operations import set
from time import time
from Utilities.Database import commissionsTable
from Utilities.ConfigurationsHelper import get_configuration


def update_commission(guild_id, user_id, name, property, value):
    query = Query()
    return len(
        commissionsTable.update(
            set(property, value),
            (query.guildId == guild_id)
            & (query.userId == user_id)
            & (query.commission.matches(name, flags=re.IGNORECASE)),
        )
    )


def add_commission(guild_id, user_id, name, days):
    query = Query()
    user_record = commissionsTable.search(
        (query.guildId == guild_id)
        & (query.userId == user_id)
        & (query.commission.matches(name, flags=re.IGNORECASE))
    )
    if len(user_record) > 0:
        return {"success": False, "message": "This commission is already assigned"}

    commissionsTable.insert(
        {
            "guildId": guild_id,
            "userId": user_id,
            "timestamp": time(),
            "commission": name,
            "days": days,
            "finalNoticeReceived": False,
            "intervalNoticeReceived": None,
        }
    )
    return {"success": True, "message": "Commission successfully assigned"}


def remove_commission(guild_id, user_id, name=None):
    query = Query()
    count = 0
    if name == None:
        count = len(
            commissionsTable.remove(
                (query.guildId == guild_id) & (query.userId == user_id)
            )
        )
    else:
        count = len(
            commissionsTable.remove(
                (query.guildId == guild_id)
                & (query.userId == user_id)
                & (query.commission.matches(name, flags=re.IGNORECASE))
            )
        )

    return {"success": True, "payload": count}


async def update_all_commissions(bot):
    for commission in commissionsTable.all():
        ## GET GENERAL VALUES ##
        guild_id = commission.get("guildId")
        channel_id = get_configuration(guild_id, "BOT_CHANNEL")
        admin_role_id = get_configuration(guild_id, "ADMIN_ROLE")
        user_id = commission.get("userId")

        guild = bot.get_guild(guild_id)
        channel = guild.get_channel(channel_id)
        admin_role = guild.get_role(admin_role_id)
        user = guild.get_member(user_id)

        name = commission.get("commission")
        timestamp = commission.get("timestamp")
        days = commission.get("days")
        current_time = time()

        final_notice_days_before = get_configuration(
            guild_id, "FINAL_NOTICE_DAYS_BEFORE"
        )
        notice_days_interval = get_configuration(guild_id, "NOTICE_DAYS_INTERVAL")

        expire_time = timestamp + (days * 86400)
        days_left = round((expire_time - current_time) / 86400)
        final_warning_time = expire_time - (final_notice_days_before * 86400)
        get_interval = (
            lambda time: floor((expire_time - time) / (notice_days_interval * 86400))
            + 1
        )
        current_interval = get_interval(current_time)
        maximum_interval = get_interval(timestamp)

        ## CHECK IF COMMISSION HAS EXPIRED ##
        expired_notice = get_configuration(guild_id, "EXPIRED_NOTICE")

        expired_notice = expired_notice.format(
            admin_role_mention=admin_role.mention,
            user_mention=user.mention,
            commission_name=name,
        )

        if current_time > expire_time:

            embed = Embed(
                title="Cancellation Notice",
                colour=Color.red(),
            )
            embed.set_author(name=user.display_name, icon_url=user.avatar_url)

            await channel.send(expired_notice)
            await channel.send(embed=embed)

            remove_commission(guild_id, user_id, name)
            return

        ## CHECK IF FINAL WARNING NEEDS TO BE ISSUES ##
        final_notice_received = commission.get("finalNoticeReceived")
        days_remaining_forfeit_warning = get_configuration(
            guild_id, "DAYS_REMAINING_FORFEIT_WARNING"
        )

        days_remaining_forfeit_warning = days_remaining_forfeit_warning.format(
            user_mention=user.mention,
            remaining_days=days_left,
            commission_name=name,
        )

        if (current_time > final_warning_time) and not (final_notice_received):

            embed = Embed(
                title="Final Notice",
                colour=Color.orange(),
            )
            embed.set_author(name=user.display_name, icon_url=user.avatar_url)

            await channel.send(days_remaining_forfeit_warning)
            await channel.send(embed=embed)

            update_commission(
                guild_id,
                user_id,
                name,
                "finalNoticeReceived",
                True,
            )
            final_notice_received = True

        if final_notice_received:
            return

        ## CHECK IF INTERVAL WARNING NEEDS TO BE ISSUED ##
        interval_notice_received = commission.get("intervalNoticeReceived")
        days_remaining_warning = get_configuration(guild_id, "DAYS_REMAINING_WARNING")

        days_remaining_warning = days_remaining_warning.format(
            user_mention=user.mention,
            remaining_days=days_left,
            commission_name=name,
        )

        if interval_notice_received == None:
            update_commission(
                guild_id, user_id, name, "intervalNoticeReceived", maximum_interval
            )
            interval_notice_received = maximum_interval

        if interval_notice_received > current_interval:

            embed = Embed(
                title="Regular Notice",
                colour=Color.green(),
            )
            embed.set_author(name=user.display_name, icon_url=user.avatar_url)

            await channel.send(days_remaining_warning)
            await channel.send(embed=embed)
            update_commission(
                guild_id,
                user_id,
                name,
                "intervalNoticeReceived",
                current_interval,
            )
            return
