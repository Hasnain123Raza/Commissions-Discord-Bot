from discord.ext.commands import RoleConverter, TextChannelConverter

from tinydb import Query
from tinydb.operations import set
from Utilities.Database import configurationsTable, commissionsTable

valid_configurations = [
    "ADMIN_ROLE",
    "BOT_CHANNEL",
    "NOTICE_DAYS_INTERVAL",
    "FINAL_NOTICE_DAYS_BEFORE",
    "DAYS_REMAINING_WARNING",
    "DAYS_REMAINING_FORFEIT_WARNING",
    "EXPIRED_NOTICE",
    "INVALID_PERMISSION",
]


async def cast_configuration_value(ctx, configuration, value):
    try:
        if configuration == "ADMIN_ROLE":
            role = await RoleConverter().convert(ctx, value)
            if role:
                return role.id
        elif configuration == "BOT_CHANNEL":
            channel = await TextChannelConverter().convert(ctx, value)
            if channel:
                return channel.id
        elif configuration == "NOTICE_DAYS_INTERVAL":
            return int(value)
        elif configuration == "FINAL_NOTICE_DAYS_BEFORE":
            return int(value)
        elif configuration == "DAYS_REMAINING_WARNING":
            return str(value)
        elif configuration == "DAYS_REMAINING_FORFEIT_WARNING":
            return str(value)
        elif configuration == "EXPIRED_NOTICE":
            return str(value)
        elif configuration == "INVALID_PERMISSION":
            return str(value)
    except:
        return None


def set_configuration(guild_id, configuration, value):
    if configuration in valid_configurations:
        if configuration == "NOTICE_DAYS_INTERVAL":
            query = Query()
            commissionsTable.update(
                set("intervalNoticeReceived", None), (query.guildId == guild_id)
            )

        configurationsTable.upsert(
            {"guild_id": guild_id, configuration: value},
            (Query().guild_id == guild_id),
        )
        return True
    return False


def get_configuration(guild_id, configuration):
    if configuration in valid_configurations:
        configurations = configurationsTable.search(
            (Query().guild_id == guild_id) & (Query()[configuration].exists())
        )

        if len(configurations) == 0:
            return False
        else:
            return configurations[0][configuration]

    return False


def prettify_configuration(ctx, configuration, value):
    if configuration == "ADMIN_ROLE":
        role = ctx.guild.get_role(value)
        if role:
            role_name = role.name
            return role_name

    if configuration == "BOT_CHANNEL":
        channel = ctx.guild.get_channel(value)
        if channel:
            channel_name = channel.name
            return channel_name

    return value
