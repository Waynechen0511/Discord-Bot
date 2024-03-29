import discord
from discord.ext import commands
from youtube_dl import YoutubeDL


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
        self.queue = []
        self.is_playing = False
        self.YDL_OPTIONS = {"format": "bestaudio", "noplaylist": "True"}
        self.FFMPEG_OPTIONS = {
            "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
            "options": "-vn",
        }
        self.vc = ""
        self.current = ""
        print("Music Cogs is now online")

    # Joins the voice channel
    @commands.command(pass_context=True)
    async def join(self, ctx):
        await join_func(self, ctx)

    # Leaves the voice channel
    @commands.command(pass_context=True, aliases=["disconnect"])
    async def leave(self, ctx):
        # Disconnects if the bot is currently in a voice channel
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
        else:
            await ctx.send("Bot is not in a voice channel.")

    # searching the item on youtube
    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" % item, download=False)[
                    "entries"
                ][0]
            except Exception:
                return False

        return {"source": info["formats"][0]["url"], "title": info["title"]}

    # Plays the next songs
    def play_next(self, ctx):
        if len(self.queue) > 0:
            self.is_playing = True

            # get the first url
            m_url = self.queue[0][0]["source"]

            self.current = self.queue[0][0]["title"]

            # remove the first element as you are currently playing it
            self.queue.pop(0)

            self.vc.play(
                discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS),
                after=lambda e: self.play_next(ctx),
            )
        else:
            self.is_playing = False

    # Plays the first song
    async def play_music(self, ctx):
        if len(self.queue) > 0:
            self.is_playing = True

            m_url = self.queue[0][0]["source"]

            # try to connect to voice channel if you are not already connected

            if self.vc == "" or not self.vc.is_connected() or self.vc == None:
                self.vc = await self.queue[0][1].connect()
            else:
                await self.vc.move_to(self.queue[0][1])

            self.current = self.queue[0][0]["title"]
            msg = "Now playing " + self.current

            print(self.queue)

            # remove the first element as you are currently playing it
            self.queue.pop(0)

            embed = discord.Embed(description=msg)
            await ctx.send(embed=embed)

            self.vc.play(
                discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS),
                after=lambda e: self.play_next(ctx),
            )
        else:
            self.is_playing = False

    @commands.command(aliases=["p"], help="Plays a selected song from youtube")
    async def play(self, ctx, *args):
        query = " ".join(args)

        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            # you need to be connected so that the bot knows where to go
            await join_func(self, ctx)
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send(
                    "Could not download the song. Incorrect format try another keyword. This could be due to playlist or a livestream format."
                )
            else:
                await ctx.send("Song added to the queue")
                self.queue.append([song, voice_channel])

                if self.is_playing == False:
                    await self.play_music(ctx)

    @commands.command(aliases=["queue"], help="Displays the current songs in queue")
    async def q(self, ctx):
        retval = ""
        for i in range(0, len(self.queue)):
            retval += str(i + 1) + ". " + self.queue[i][0]["title"] + "\n"

        embed = discord.Embed(title="Music Queue", description=retval)

        if retval != "":
            await ctx.send(embed=embed)
        else:
            await ctx.send("No music in queue")

    @commands.command(aliases=["next"], help="Skips the current song being played")
    async def skip(self, ctx):
        if self.vc != "" and self.vc:
            self.vc.stop()
            # try to play next in the queue if it exists
            await self.play_music(ctx)

    @commands.command(aliases=["song", "current"], help="Views the current song")
    async def currentSong(self, ctx):
        current_song = "The current song playing is: " + self.current + "\n"
        embed = discord.Embed(title="Current Song", description=current_song)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Music(bot))
