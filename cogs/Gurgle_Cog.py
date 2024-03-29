import discord
from discord.ext import commands
from urllib.parse import quote
import aiohttp


class Gurgle(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=bot.loop)
        print("Gurgle Cogs is now online")

    @commands.command(aliases=["image"])
    async def img(self, ctx, *, content: commands.clean_content):
        async with self.session.get(
            f"https://gurgle.nathaniel-fernandes.workers.dev/single?q={quote(content)}"
        ) as response:
            if response.status == 200:
                link = await response.json()  # Assuming the API returns JSON
                embed = discord.Embed(description=content).set_image(url=link)
                embed.set_author(
                    name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url
                )
                await ctx.send(embed=embed)
            else:
                await ctx.send("Failed to fetch image.")


def setup(bot):
    bot.add_cog(Gurgle(bot))
