from discord.ext import commands
from Utilities.ConfigurationsHelper import get_configuration


def has_permissions():
    async def predicate(ctx):
        guild_roles = ctx.guild.roles
        guild_roles.reverse()
        guild_role_ids = list(map(lambda role: role.id, guild_roles))

        admin_role = get_configuration(ctx.guild.id, "ADMIN_ROLE")
        admin_role_index = guild_role_ids.index(admin_role)

        author_roles = ctx.author.roles
        author_role_ids = list(map(lambda role: role.id, author_roles))
        author_role_indices = list(
            map(lambda role: guild_role_ids.index(role), author_role_ids)
        )

        for index in author_role_indices:
            if index <= admin_role_index:
                return True

        channel_id = get_configuration(ctx.guild.id, "BOT_CHANNEL")
        channel = ctx.guild.get_channel(channel_id)
        invalid_permission = get_configuration(ctx.guild.id, "INVALID_PERMISSION")
        await channel.send(invalid_permission)

        return False

    return commands.check(predicate)
