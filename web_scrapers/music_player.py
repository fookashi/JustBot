import disnake
from disnake.ext import commands
import yt_dlp as youtube_dl

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}


class MusicPlayer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice = None
        self.is_playing = False
        self.queue = []

    async def join_voice_channel(self, ctx):
        if ctx.author.voice is None or ctx.author.voice.channel is None:
            await ctx.send("Вы должны быть в голосовом канале, чтобы использовать эту команду.")
            return False

        self.voice = await ctx.author.voice.channel.connect()
        return True

    async def leave_voice_channel(self, ctx):
        if self.voice is not None:
            await self.voice.disconnect()
            self.voice = None

    async def play_next(self):
        if len(self.queue) > 0:
            self.is_playing = True
            url = self.queue[0]["url"]
            print(url)
            self.voice.play(disnake.FFmpegPCMAudio(url, **FFMPEG_OPTIONS))
            self.queue.pop(0)
        else:
            self.is_playing = False

    @commands.slash_command()
    async def play(self, ctx, url: str):
        if self.voice is None:
            if not await self.join_voice_channel(ctx):
                return


        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['formats'][0]['url']

        self.queue.append({"url": url2})
        if not self.is_playing:
            await self.play_next()

    @commands.command()
    async def stop(self, ctx):
        if self.voice is not None and self.voice.is_playing():
            self.voice.stop()
            self.is_playing = False
            await ctx.send("Музыка остановлена.")

    @commands.command()
    async def skip(self, ctx):
        if self.voice is not None and self.voice.is_playing():
            self.voice.stop()
            await ctx.send("Текущая песня пропущена.")

    @commands.command()
    async def leave(self, ctx):
        await self.leave_voice_channel(ctx)
        await ctx.send("Покинул голосовой канал.")

    @commands.command()
    async def ensure_voice(self, ctx: commands.Context):
        if ctx.voice_client is None:
            if ctx.author.voice is not None:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("Вы должны находиться в голосовом канале, чтобы воспроизводить музыку.")
                raise commands.CommandError("Автор не находится в голосовом канале.")

    @stop.before_invoke
    async def ensure_playing(self, ctx):
        if ctx.voice_client is None or not ctx.voice_client.is_playing():
            await ctx.send("Сейчас ничего не играет.")
            raise commands.CommandError("Нет активного воспроизведения музыки.")



