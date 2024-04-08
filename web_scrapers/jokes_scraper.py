import random
from datetime import datetime

from aiocache import cached
from aiocache.serializers import PickleSerializer
from telethon.tl.types import MessageMediaPhoto

from .base_scraper import BaseScrapper
from utils.telegram_handler import TelegramClientHandler
from models.tg import CopypasteData
from models.frog import FrogData
from utils import frog


class JokesScrapper(BaseScrapper):
    def __init__(self, tg_handler: TelegramClientHandler):
        self.stupid_jokes_url = "https://www.anekdot.ru/release/anekdot/week/"
        self.frog_text_constructor = frog.FrogTextConstructor()
        self.tg_handler = tg_handler

    @cached(ttl=60 * 60 * 24, serializer=PickleSerializer())
    async def _scrape_stupid_jokes(self):
        data = await self._get_data_with_soup(self.stupid_jokes_url)
        jokes = data.find_all('div', class_='text')[0:100]
        return [joke.text for joke in jokes]

    async def do_stupid_joke(self):
        jokes = await self._scrape_stupid_jokes()
        return random.choice(jokes)

    @cached(ttl=60 * 60 * 24, serializer=PickleSerializer())
    async def _scrape_category_b_jokes(self):
        jokes = await self.tg_handler._get_data_from_tg_chanel(1743905774, limit=100)
        return [j.text async for j in jokes if j.__getattribute__('photo') is None]

    async def do_category_b_joke(self):
        data = await self._scrape_category_b_jokes()
        return random.choice(data)

    @cached(ttl=60 * 60 * 24, serializer=PickleSerializer())
    async def _scrape_copypastes(self) -> list[int]:
        data = await self.tg_handler._get_data_from_tg_chanel(1640385961, limit=300)
        return [cp.id async for cp in data if cp.text is not None and cp.text.find("http") == -1]

    async def do_copypaste(self) -> CopypasteData | None:
        msgs = await self._scrape_copypastes()
        msg_id = random.choice(msgs)
        msg = await self.tg_handler.get_message_by_peer_and_id(peer_id=1640385961, msg_id=msg_id)
        if msg is None:
            print("Не найдено сообщение из заготовленного списка, обновляю список")
            await self._scrape_copypastes()
            return await self.do_copypaste()
        text = msg.text
        image = None
        if msg.media and isinstance(msg.media, MessageMediaPhoto):
            image = await self.tg_handler.client.download_media(msg.media.photo, 'tg_copypaste.jpg')
        return CopypasteData(text=text, image=image)

    async def get_frog(self):
        dt = datetime.now()
        weekday_as_num = dt.weekday()
        frog_link = random.choice(frog.FROG_LINKS[weekday_as_num])
        image = await self._get_bytes_from_url(frog_link)
        text = self.frog_text_constructor.create_text(weekday_as_num)
        if image is None:
            text = text + '\nИ, кстати, сегодня без картинок :('
        return FrogData(text=text, image=image)
