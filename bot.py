from disnake.ext import commands

from db.repos.guild_info import GuildInfoRepo
from db.repos.guild_info.model import GuildInfo
from utils.telegram_handler import TelegramClientHandler


class JustBot(commands.Bot):
    def __init__(self, *args: int, **kwargs: int) -> None:
        self.tg_handler = TelegramClientHandler()
        super().__init__(*args, **kwargs)

    async def get_guild_info(self, guild_id: int) -> GuildInfo:
        info: GuildInfo | None = None
        guild_repo: GuildInfoRepo
        async with GuildInfoRepo as guild_repo:
            # TODO: Collection guild info should have guild_id(int) as main index, maybe i should remove objectid idk
            info = await guild_repo.get_one(value=guild_id)
            if info is None:
                info = await guild_repo.add_one({"guild_id": guild_id})
        return info
