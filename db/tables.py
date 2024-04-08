from .base import BaseTable
from models.db.guild_info import GuildInfo


class GuildInfoTable(BaseTable):
    @property
    def table(self):
        return 'guild_info'

    @property
    def model(self):
        return GuildInfo

    @property
    def primary_key(self):
        return 'guild_id'
