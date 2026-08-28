import random
import discord
from discord.ext import commands
from ddgs import DDGS

class ImageSearch(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print("Image Search Cogs is now online")

    @commands.command(aliases=["img"])
    async def image(self, ctx, *, query):



        results = DDGS().images(query, max_results=10, safesearch="on")

        if not results:
            await ctx.send("No images found.")
            return

        result = random.choice(results)

        image_url = result["image"]

        embed = discord.Embed()
        embed.set_image(url=image_url)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(ImageSearch(bot))
