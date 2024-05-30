from db.repos.guild_info import GuildInfoRepo
from db.repos.guild_info.model import GuildInfo
from disnake.ext import commands
from utils.telegram_handler import TelegramClientHandler


class JustBot(commands.Bot):
    def __init__(self, *args: int, **kwargs: int) -> None:
        self.tg_handler = TelegramClientHandler()
        self.guild_infos = {}
        super().__init__(*args, **kwargs)

    async def get_guild_info(self, guild_id: int) -> GuildInfo:
        guild_info: GuildInfo | None = None
        if self.guild_infos.get(guild_id) is not None:
            return self.guild_infos[guild_id]
        async with GuildInfoRepo() as guild_repo:
            guild_info = await guild_repo.get_one(value=guild_id, key="guild_id")
            if guild_info is None:
                guild_info = await guild_repo.add_one({"guild_id": guild_id})
        self.guild_infos[guild_id] = guild_info
        return guild_info

    async def get_all_guilds_info(self) -> list[GuildInfo]:
        return list(self.guild_infos.values)
