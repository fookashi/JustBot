from typing import Iterator

import telethon
from settings import get_settings
from telethon.tl.types import PeerChannel
from utils.singleton import Singleton


class TelegramClientHandler(metaclass=Singleton):
    def __init__(self) -> None:
        settings = get_settings()
        api_id = settings.TG_API_ID
        tg_api_hash = settings.TG_API_HASH
        self.client = telethon.TelegramClient("justbot", api_id, tg_api_hash)
        #self.client.start()

    async def get_data_from_tg_chanel(self, channel_id: int, limit: int = 100) -> Iterator[telethon.types.Message]:
        entity = PeerChannel(channel_id)
        return self.client.iter_messages(entity, limit=limit)

    async def check_channels_data(self, title: str) -> list | None:
        data = await self.client.get_dialogs()
        try:
            needed = next(filter(lambda x: x.title == title, data))
        except StopIteration:
            return None
        return needed

    async def get_message_by_peer_and_id(self, channel_id: int, msg_id: int) -> telethon.types.Message:
        entity = PeerChannel(channel_id)
        data = await self.client.get_messages(entity, max_id=msg_id + 1, min_id=msg_id - 1)
        if len(data) != 1:
            return None
        return data[0]

if __name__ == "__main__":
    TelegramClientHandler()
