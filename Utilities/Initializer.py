from Utilities.ConfigurationsHelper import set_configuration, get_configuration


def initialize(bot):
    for guild in bot.guilds:
        guild_id = guild.id

        # Default ADMIN_ROLE is either a role named Commissions or
        # the top role in role hierarchy
        if not get_configuration(guild_id, "ADMIN_ROLE"):
            selected_role_id = None

            for role in guild.roles:
                if role.name.lower() == "commissions":
                    selected_role_id = role.id

            if selected_role_id == None:
                selected_role_id = guild.roles[-1].id

            set_configuration(guild_id, "ADMIN_ROLE", selected_role_id)

        # Default BOT_CHANNEL is either a text-channel named bots or
        # a the first channel in the channel list
        if not get_configuration(guild_id, "BOT_CHANNEL"):
            selected_channel_id = None

            for channel in guild.channels:
                if channel.name.lower() == "bots":
                    selected_channel_id = channel.id

            if selected_channel_id == None:
                selected_channel_id = guild.channels[0].id

            set_configuration(guild_id, "BOT_CHANNEL", selected_channel_id)

        # Default NOTICE_DAYS_INTERVAL is: 3
        if not get_configuration(guild_id, "NOTICE_DAYS_INTERVAL"):
            set_configuration(guild_id, "NOTICE_DAYS_INTERVAL", 3)

        # Default NOTICE_DAYS_INTERVAL is: 2
        if not get_configuration(guild_id, "FINAL_NOTICE_DAYS_BEFORE"):
            set_configuration(guild_id, "FINAL_NOTICE_DAYS_BEFORE", 2)

        # Default DAYS_REMAINING_WARNING is:
        if not get_configuration(guild_id, "DAYS_REMAINING_WARNING"):
            set_configuration(
                guild_id,
                "DAYS_REMAINING_WARNING",
                "{user_mention}, you have {remaining_days} days left to complete `{commission_name}` commission.",
            )

        # Default DAYS_REMAINING_FORFEIT_WARNING is:
        if not get_configuration(guild_id, "DAYS_REMAINING_FORFEIT_WARNING"):
            set_configuration(
                guild_id,
                "DAYS_REMAINING_FORFEIT_WARNING",
                "{user_mention}, you have {remaining_days} days left to complete `{commission_name}` commission. You may forfeit the reward if the commission is not complete on time.",
            )

        # Default EXPIRED_NOTICE is:
        if not get_configuration(guild_id, "EXPIRED_NOTICE"):
            set_configuration(
                guild_id,
                "EXPIRED_NOTICE",
                "{admin_role_mention} {user_mention}, your `{commission_name}` commission has expired.",
            )

        # Default INVALID_PERMISSION is You do not have permission to use that command!:
        if not get_configuration(guild_id, "INVALID_PERMISSION"):
            set_configuration(
                guild_id,
                "INVALID_PERMISSION",
                "You do not have permission to use that command!",
            )
