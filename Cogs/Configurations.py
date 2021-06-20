from discord import Embed, Color
from discord.ext import commands
from Utilities.ConfigurationsHelper import (
    valid_configurations,
    cast_configuration_value,
    set_configuration,
    get_configuration,
    prettify_configuration,
)
from Utilities.HasPermissions import has_permissions


class ConfigurationsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["setconfig"], help="Sets a configuration value")
    @has_permissions()
    async def setconfiguration(self, ctx, configuration: str, *, value):
        if not configuration in valid_configurations:
            return await ctx.send(
                "Configuration is invalid (case sensitive), please try again"
            )

        value = await cast_configuration_value(ctx, configuration, value)
        if not value:
            return await ctx.send("Value is invalid, please try again")

        response = set_configuration(ctx.author.guild.id, configuration, value)
        if not response:
            await ctx.send("There was a problem")

        await ctx.send("Successfully updated configuration")

    @commands.command(
        aliases=["getconfig"],
        help="Gets a configuration value. If no configuration is specified, gets all configurations",
    )
    async def getconfiguration(self, ctx, configuration: str = None):
        if configuration:
            value = get_configuration(ctx.author.guild.id, configuration)

            if not value:
                await ctx.send(
                    "Configuration is invalid (case sensitive), please try again"
                )

            value = prettify_configuration(ctx, configuration, value)

            responseEmbed = Embed(
                title=configuration,
                description=str(value),
                colour=Color.green(),
            )

            await ctx.send(embed=responseEmbed)
        else:
            configurations = valid_configurations

            responseEmbed = Embed(
                title="Configurations",
                colour=Color.green(),
            )

            for configuration in configurations:
                value = get_configuration(ctx.author.guild.id, configuration)

                value = prettify_configuration(ctx, configuration, value)

                if value:
                    responseEmbed.add_field(
                        name=configuration,
                        value=str(value),
                        inline=True,
                    )
                else:
                    await ctx.send(
                        "Configuration is invalid (case sensitive), please try again"
                    )

            await ctx.send(embed=responseEmbed)
