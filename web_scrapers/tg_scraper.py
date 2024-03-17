import telethon
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import PeerChannel

from utils.singleton import Singleton
from interfaces import IWebScraper
from settings import get_settings


class TgScrapper(IWebScraper):
    def __init__(self):
        env_vars = get_settings().get_secrets()
        API_ID = env_vars.get('tg_api_id')
        TG_API_HASH = env_vars.get('tg_api_hash')
        self.client = telethon.TelegramClient('justbot', API_ID, TG_API_HASH)
        self.url = "https://t.me/baneksru"

    async def _get_data_with_soup(self, url: str):
        raise NotImplementedError

    async def _get_data_from_tg_chanel(self, id: int, limit=100):
        await self.client.start()
        entity = PeerChannel(id)
        data = self.client.iter_messages(entity, limit=limit)
        return data
