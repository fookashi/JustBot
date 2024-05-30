import asyncio
from collections import defaultdict

import disnake
import yt_dlp
from db.repos.guild_info import GuildInfoRepo
from disnake.ext import commands
from models.guild_music_info import GuildMusicInfo

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
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot
        self.music_infos: dict[int, GuildMusicInfo] = defaultdict(GuildMusicInfo)
        self.ytdl: yt_dlp.YoutubeDL = yt_dlp.YoutubeDL(YDL_OPTIONS)

    async def join_voice_channel(self, ctx: commands.Context) -> bool:
        if ctx.author.voice is None:
            await ctx.send("Вы должны быть в голосовом канале, чтобы использовать эту команду.")
            return False
        self.music_infos[ctx.guild.id].voice = await ctx.author.voice.channel.connect()
        return True

    async def leave_voice_channel(self, ctx: commands.Context) -> None:
        self.music_infos[ctx.guild.id].voice = (
            await self.music_infos[ctx.guild.id].voice.disconnect()
            if self.music_infos[ctx.guild.id].voice
            else self.music_infos[ctx.guild.id].voice
        )

    async def play_next(self, guild_id: int) -> None:
        music_info = self.music_infos[guild_id]
        if len(music_info.playlist) >= 1:
            url = music_info.playlist.pop(0)
            music_info.voice.play(
                disnake.FFmpegPCMAudio(url, **FFMPEG_OPTIONS),
                after=lambda _=None: asyncio.run(self.play_next(guild_id)),
            )
        else:
            music_info.is_playing = False
            music_info.voice = await music_info.voice.disconnect()

    @commands.command()
    async def play(self, ctx: commands.Context, url: str) -> None:
        guild_info = await self.bot.get_guild_info(ctx.guild.id)
        if guild_info.music_channel_id is not None and ctx.channel.id != guild_info.music_channel_id:
            channel = self.bot.get_channel(guild_info.music_channel_id)
            msg_content = ctx.message.content
            await ctx.message.delete()
            text = f"{ctx.author.mention}, ваше сообщение автоматически перенесено на этот канал:\n*{msg_content}*"
            ctx.message = await channel.send(text)
        music_info = self.music_infos[ctx.guild.id]
        if music_info.voice is None and not await self.join_voice_channel(ctx):
            return None
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: self.ytdl.extract_info(url, download=False))
        song = data["url"]
        music_info.playlist.append(song)
        if not music_info.is_playing:
            music_info.is_playing = True
            return await self.play_next(ctx.guild.id)
        return None

    @commands.command()
    async def stop(self, ctx: commands.Context) -> None:
        self.music_infos[ctx.guild.id].playlist.clear()
        return await self.skip(ctx)

    @commands.command()
    async def skip(self, ctx: commands.Context) -> disnake.Message | None:
        if self.music_infos[ctx.guild.id].voice is None:
            return await ctx.send("Бот не играет музыку!")
        self.music_infos[ctx.guild.id].voice.stop()
        if not len(self.music_infos[ctx.guild].playlist):
            await self.leave_voice_channel(ctx)
            return await ctx.send("Плейлист пуст, я пошел.")
        return await ctx.send("Песня убрана из плейлиста.")

    @commands.command()
    async def set_mc(self, ctx: commands.Context) -> disnake.Message:
        if ctx.message.author.id != ctx.guild.owner_id:
            return await ctx.send("У вас не хватает прав")

        async with GuildInfoRepo() as guild_repo:
            await guild_repo.update_one(ctx.guild.id, "guild_id", {"music_channel_id": ctx.channel.id})

        return await ctx.send("Канал для музыкальных комманд установлен")

    @commands.command()
    async def unset_mc(self, ctx: commands.Context) -> disnake.Message:
        if ctx.message.author.id != ctx.guild.owner_id:
            return await ctx.send("У вас не хватает прав")

        async with GuildInfoRepo() as guild_repo:
            await guild_repo.update_one(ctx.guild.id, "guild_id", {"music_channel_id": None})

        return await ctx.send("Музыкальный канал откреплен")
