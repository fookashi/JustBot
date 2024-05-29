from db.repos.base import BaseRepo
from db.repos.guild_info.model import GuildInfo


class GuildInfoRepo(BaseRepo):
    @property
    def table(self) -> str:
        return "guild_info"

    @property
    def model(self) -> GuildInfo:
        return GuildInfo
