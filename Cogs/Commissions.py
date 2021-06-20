from discord import Member, Embed, Color
from discord.ext import tasks, commands
from tinydb import Query
from time import time
from Utilities.Database import commissionsTable
from Utilities.CommissionsHelper import (
    add_commission,
    remove_commission,
    update_all_commissions,
)
from Utilities.HasPermissions import has_permissions


class CommissionsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_commissions.start()

    def cog_unload(self):
        self.update_commissions.cancel()

    @commands.command(help="Gives a commission")
    @has_permissions()
    async def give(self, ctx, user: Member, days: int, *, name):
        if user.bot:
            return await ctx.send("Bots can not have commissions")

        response = add_commission(user.guild.id, user.id, name, days)

        await ctx.send(response.get("message"))

    @commands.command(help="Cancels a commission")
    @has_permissions()
    async def cancel(self, ctx, user: Member, *, name=None):
        if user.bot:
            return await ctx.send("Bots can not have commissions")

        response = remove_commission(user.guild.id, user.id, name)
        count = response.get("payload")

        message = (
            "Successfully cancelled {} commission(s)".format(count)
            if name == None
            else "Successfully cancelled '{}' commission".format(name)
        )
        await ctx.send(message)

    @commands.command(help="Completes a commission")
    @has_permissions()
    async def complete(self, ctx, user: Member, *, name=None):
        if user.bot:
            return await ctx.send("Bots can not have commissions")

        response = remove_commission(user.guild.id, user.id, name)
        count = response.get("payload")

        message = (
            "Successfully completed {} commission(s)".format(count)
            if name == None
            else "Successfully completed '{}' commission".format(name)
        )
        await ctx.send(message)

    @commands.command(help="Views commissions")
    async def view(self, ctx, user: Member):
        if user.bot:
            return await ctx.send("Bots can not have commissions")

        commissions_query = commissionsTable.search(
            (Query().guildId == user.guild.id) & (Query().userId == user.id)
        )
        total_commissions = len(commissions_query)

        embed = Embed(
            title="Commissions",
            description="{.display_name} has {} total active commission(s).".format(
                user, total_commissions
            )
            if total_commissions > 0
            else "{.display_name} has no active commissions.".format(user),
            colour=Color.purple(),
        )
        embed.set_author(name=user.display_name, icon_url=user.avatar_url)

        for user_record in commissions_query:
            timestamp = user_record.get("timestamp")
            days = user_record.get("days")
            current_time = time()
            expire_time = timestamp + (days * 15)
            days_left = round((expire_time - current_time) / 15)
            embed.add_field(
                name=user_record.get("commission"),
                value="{} day(s) left".format(days_left),
                inline=True,
            )

        await ctx.send(embed=embed)

    @tasks.loop(minutes=1 / 15)
    async def update_commissions(self):
        await update_all_commissions(self.bot)

    @update_commissions.before_loop
    async def before_update_commissions(self):
        await self.bot.wait_until_ready()
