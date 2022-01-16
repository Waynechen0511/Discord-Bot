from shlex import join
import discord
from discord.ext import commands
import youtube_dl

async def join_func(self, ctx):
    # Connect if the user is already in a voice channel
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("You are not currently in a voice channel, please join one.")

class Music(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        print("Music Cogs is now online")

    '''
    def youtube_search(self, title):
        with youtube_dl.YoutubeDL(self.YDL_OPTIONS) as ydl:
            info = ydl.extract_info(title, download = False)
            url = info["formats"][0]["url"]
            link = discord.FFmpegOpusAudio.from_probe(url, ** self.FFMPEG_OPTIONS)
            return link
    '''

    # Joins the voice channel
    @commands.command(pass_context=True)
    async def join(self, ctx):
        await join_func(self, ctx)

    # Leaves the voice channel
    @commands.command(pass_context=True, aliases=['disconnect'])
    async def leave(self, ctx):
        # Disconnects if the bot is currently in a voice channel
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
        else:
            await ctx.send("Bot is not in a voice channel.")

    # Plays a song in the voice channel
    @commands.command(pass_context=True)
    async def play(self, ctx, url):
        await join_func(self,ctx)
        channel = ctx.voice_client
        with youtube_dl.YoutubeDL(self.YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download = False)
            url2 = info["formats"][0]["url"]
            link = await discord.FFmpegOpusAudio.from_probe(url2, ** self.FFMPEG_OPTIONS)
            channel.play(link)
    '''
    @play.error
    async def play_error(self, ctx, error):
        if isinstance(error, commands.DownloadError):
            await ctx.reply("Download Error")
    '''


def setup(bot):
    bot.add_cog(Music(bot))
