import random

from aiocache import cached
from aiocache.serializers import PickleSerializer
import telethon
from telethon.tl import types as tg_type

from ..base_objs.base_scraper import BaseScrapper
from utils.tg_scraper import TgScrapper
from models.tg import CopypasteData


class JokesScrapper(BaseScrapper):
    def __init__(self, tg_scraper: TgScrapper):
        self.stupid_jokes_url = "https://www.anekdot.ru/release/anekdot/week/"
        self.tg_scraper = tg_scraper

    @cached(ttl=60 * 60 * 24, serializer=PickleSerializer())
    async def _scrape_stupid_jokes(self) -> list[str]:
        data = await self._get_data_with_soup(self.stupid_jokes_url)
        jokes = data.find_all('div', class_='text')[0:100]
        print(len(jokes))
        return [joke.text for joke in jokes]

    async def do_stupid_joke(self) -> str:
        jokes = await self._scrape_stupid_jokes()
        return random.choice(jokes)

    @cached(ttl=60 * 60 * 24, serializer=PickleSerializer())
    async def _scrape_category_b_jokes(self) -> list[str]:
        jokes = await self.tg_scraper._get_data_from_tg_chanel(1743905774, limit=200)
        return [j.text async for j in jokes if j.__getattribute__('photo') is None]

    async def do_category_b_joke(self) -> str:
        data = await self._scrape_category_b_jokes()
        return random.choice(data)

    @cached(ttl=60 * 60 * 24, serializer=PickleSerializer())
    async def _scrape_copypastes(self) -> list[tg_type.Message]:
        data = await self.tg_scraper._get_data_from_tg_chanel(1640385961, limit=200)
        return [cp.id async for cp in data if cp.text is not None and cp.text.find("http") == -1]

    async def do_copypaste(self) -> CopypasteData | None:
        msgs = await self._scrape_copypastes()
        msg_id = random.choice(msgs)
        msg = await self.tg_scraper.get_message_by_peer_and_id(peer_id=1640385961, msg_id=msg_id)
        if msg is None:
            print("Не найдено сообщение из заготовленного списка, обновляю список")
            await self._scrape_copypastes()
            return await self.do_copypaste()
        text = msg.text
        image = None
        if msg.media and isinstance(msg.media, tg_type.MessageMediaPhoto):
            image = await self.tg_scraper.client.download_media(msg.media.photo, 'tg_copypaste.jpg')
        return CopypasteData(text=text, image=image)
