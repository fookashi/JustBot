from db.repos.base import BaseRepo
from db.repos.guild_info.model import GuildInfo
from motor.motor_asyncio import AsyncIOMotorCollection


class GuildInfoRepo(BaseRepo):
    @property
    def _collection_name(self) -> str:
        return "guildInfo"

    @property
    def collection(self) -> AsyncIOMotorCollection:
        return self._database.get_collection(self._collection_name)

    @property
    def model(self) -> GuildInfo:
        return GuildInfo
