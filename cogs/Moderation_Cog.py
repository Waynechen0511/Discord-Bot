import discord
from discord.ext import commands


class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print("Moderation Cogs is now online")

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong!")

    # Clears messages
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, arg, member: discord.Member = None):
        if member is None:
            deleted = await ctx.channel.purge(limit=int(arg))
            await ctx.send("Deleted {} message(s)".format(len(deleted)))
        else:
            deleted = await ctx.channel.purge(
                limit=int(arg), check=lambda e: e.author == member
            )
            await ctx.send(
                "Deleted {} message(s) from the target member in the previous {} messages.".format(
                    len(deleted), arg
                )
            )

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply("You do not have permissions to manage messages.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply("Please specify an amount of messages to delete")

    # Creates a poll
    @commands.command()
    async def poll(self, ctx, *, question):
        message = await ctx.send(f"📊 **Poll:** {question}")
        await message.add_reaction("👍")
        await message.add_reaction("👎")


def setup(bot):
    bot.add_cog(Moderation(bot))
