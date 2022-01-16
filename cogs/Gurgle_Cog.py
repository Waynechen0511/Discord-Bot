import discord
from discord.ext import commands
from urllib.parse import quote

class Gurgle(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print("Gurgle Cogs is now online")

    @commands.command(aliases=['image'])
    async def img(self, ctx, *, content:commands.clean_content):
        link = await self.bot.requests.get_json(f'https://gurgle.nathaniel-fernandes.workers.dev/single?q={quote(content)}')
        embed = discord.Embed(description = content).set_image(url=link)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        

def setup(bot):
    bot.add_cog(Gurgle(bot))
