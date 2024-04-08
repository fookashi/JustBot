from disnake.ext import commands

from utils.telegram_handler import TelegramClientHandler
from db.tables import GuildInfoTable
from models.db.guild_info import GuildInfo

class JustBot(commands.Bot):

    def __init__(self, *args, **kwargs):
        self.tg_handler = TelegramClientHandler()
        self.guild_infos: dict[int: dict] = {}
        super().__init__(*args, **kwargs)
    
    async def get_guild_info(self, guild_id) -> GuildInfo:
        info = None
        try:
            info = self.guild_infos[guild_id]
            return GuildInfo.from_list(**info)
        except KeyError:
            async with GuildInfoTable() as guild_table:
                info = await guild_table.get_by_key(guild_id)
                if info is None:
                    info = await guild_table.add_one(GuildInfo(guild_id=guild_id))
                    self.guild_infos[guild_id] = info
            return info
            
                    