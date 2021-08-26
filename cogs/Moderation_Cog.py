import discord
from discord.ext import commands

class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Moderation Cogs is now online")

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong!")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, arg):
        await ctx.channel.purge(limit = int(arg) + 1)
        await ctx.send("Messages cleared")

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply("You do not have permissions to manage messages.")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply("Please specify an amount of messages to delete")

def setup(bot):
    bot.add_cog(Moderation(bot))