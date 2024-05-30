from db.repos.guild_info import GuildInfoRepo
from db.repos.guild_info.model import GuildInfo
from disnake.ext import commands
from utils.telegram_handler import TelegramClientHandler


class JustBot(commands.Bot):
    def __init__(self, *args: int, **kwargs: int) -> None:
        self.tg_handler = TelegramClientHandler()
        super().__init__(*args, **kwargs)

    async def get_guild_info(self, guild_id: int) -> GuildInfo:
        guild_info: GuildInfo | None = None
        async with GuildInfoRepo() as guild_repo:
            # TODO: Collection guild info should have guild_id(int)  # noqa: FIX002, TD002, TD003
            # maybe as second index, maybe i should remove objectid idk and set guild_id
            guild_info = await guild_repo.get_one(value=guild_id, key="guild_id")
            if guild_info is None:
                guild_info = await guild_repo.add_one({"guild_id": guild_id})
        return guild_info
