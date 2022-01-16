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
    async def clear(self, ctx, arg, member : discord.Member = None):
        if member is None:
            deleted = await ctx.channel.purge(limit = int(arg))
            await ctx.send("Deleted {} message(s)".format(len(deleted)))
        else:
            # Only deletes the messages sent by member in the past arg messages, instead of deleting arg # of messages by member
            deleted = await ctx.channel.purge(limit = int(arg), check = lambda e: e.author == member)
            await ctx.send("Deleted {} message(s) from".format(len(deleted)) + " the target member in the previous " + arg + " messages.")

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply("You do not have permissions to manage messages.")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply("Please specify an amount of messages to delete")

def setup(bot):
    bot.add_cog(Moderation(bot))
