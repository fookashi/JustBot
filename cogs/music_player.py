import asyncio
from collections import defaultdict, deque

import disnake
import yt_dlp
from disnake.ext import commands

from bot import JustBot
from db.repos.guild_info import GuildInfo, GuildInfoRepo

FFMPEG_OPTIONS = {"before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5", "options": "-vn"}
YDL_OPTIONS = {
    "format": "bestaudio/best",
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        },
    ],
}


class MusicPlayer(commands.Cog):
    def __init__(self, bot: JustBot) -> None:
        self.bot = bot
        self.queues = defaultdict(lambda: {"voice": None, "queue": deque(), "is_playing": False})
        self.ytdl = yt_dlp.YoutubeDL(YDL_OPTIONS)

    async def join_voice_channel(self, ctx: commands.Context) -> bool:
        if ctx.author.voice is None:
            await ctx.send("Вы должны быть в голосовом канале, чтобы использовать эту команду.")
            return False
        self.queues[ctx.guild.id]["voice"] = await ctx.author.voice.channel.connect()
        return True

    async def leave_voice_channel(self, ctx: commands.Context) -> None:
        queue = self.queues[ctx.guild.id]
        if queue["voice"] is not None:
            await queue["voice"].disconnect()
            queue["voice"] = None

    async def play_next(self, guild_id: int) -> None:
        info = self.queues[guild_id]
        if len(info["queue"]) >= 1:
            url = info["queue"].popleft()
            info["voice"].play(
                disnake.FFmpegPCMAudio(url, **FFMPEG_OPTIONS),
                after=lambda e=None: self.play_next(guild_id),  # noqa: ARG005
            )
        else:
            asyncio.sleep(90)
            info["is_playing"] = False
            info["voice"] = await info["voice"].disconnect()

    @commands.command()
    async def play(self, ctx: commands.Context, url: str) -> None:
        info = await self.bot.get_guild_info(ctx.guild.id)
        if info.music_channel_id is not None and ctx.channel.id != info.music_channel_id:
            channel = self.bot.get_channel(info.music_channel_id)
            msg_content = ctx.message.content
            await ctx.message.delete()
            text = f"{ctx.author.mention}, ваше сообщение автоматически перенесено на этот канал:\n*{msg_content}*"
            ctx.message = await channel.send(text)
        if self.queues[ctx.guild.id]["voice"] is None and not await self.join_voice_channel(ctx):
            return
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: self.ytdl.extract_info(url, download=False))
        song = data["url"]

        self.queues[ctx.guild.id]["queue"].append(song)
        if not self.queues[ctx.guild.id]["is_playing"]:
            await self.play_next(ctx.guild.id)

    @commands.command()
    async def stop(self, ctx: commands.Context) -> None:
        self.queues[ctx.guild.id]["queue"].clear()
        await self.skip(ctx)

    @commands.command()
    async def skip(self, ctx: commands.Context) -> disnake.Message | None:
        if self.queues[ctx.guild.id]["voice"] is None:
            return await ctx.send("Бот не играет музыку")
        self.queues[ctx.guild.id]["voice"].stop()
        return None

    @commands.command()
    async def set_mc(self, ctx: commands.Context) -> disnake.Message:
        if ctx.message.author.id != ctx.guild.owner_id:
            return await ctx.send("У вас не хватает прав")

        async with GuildInfoRepo() as guild_table:
            await guild_table.update_one(ctx.guild.id, "music_channel_id", ctx.channel.id)

        return await ctx.send("Канал для музыкальных комманд установлен")

    @commands.command()
    async def unset_mc(self, ctx: commands.Context) -> disnake.Message:
        if ctx.message.author.id != ctx.guild.owner_id:
            return await ctx.send("У вас не хватает прав")

        async with GuildInfoRepo() as guild_table:
            await guild_table.update_one(ctx.guild.id, "music_channel_id", None)

        return await ctx.send("Музыкальный канал откреплен")
