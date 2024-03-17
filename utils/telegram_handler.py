import telethon
from telethon.tl.types import PeerChannel

from settings import get_settings


class TelegramClientHandler:
    def __init__(self):
        env_vars = get_settings().get_secrets()
        API_ID = env_vars.get('tg_api_id')
        TG_API_HASH = env_vars.get('tg_api_hash')
        self.client = telethon.TelegramClient('justbot', API_ID, TG_API_HASH)
        self.client.start()

    async def _get_data_with_soup(self, url: str):
        raise NotImplementedError

    async def _get_data_from_tg_chanel(self, id: int, limit=100):
        entity = PeerChannel(id)
        data = self.client.iter_messages(entity, limit=limit)
        return data

    async def _check_channels_data(self, title: str):
        data = await self.client.get_dialogs()
        try:
            needed = next(filter(lambda x: x.title == title, data))
        except Exception:
            return None
        return needed

    async def get_message_by_peer_and_id(self, peer_id: int, msg_id: int):
        entity = PeerChannel(peer_id)
        data = await self.client.get_messages(entity, max_id=msg_id+1, min_id=msg_id-1)
        if len(data) != 1:
            return None
        return data[0]
