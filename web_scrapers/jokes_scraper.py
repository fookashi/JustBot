import random
from datetime import UTC, datetime

from aiocache import cached
from aiocache.serializers import PickleSerializer
from telethon.tl.types import MessageMediaPhoto

from models.frog import FrogData
from models.tg import CopypasteData
from utils import frog
from utils.telegram_handler import TelegramClientHandler

from .base_scraper import BaseScrapper


class JokesScrapper(BaseScrapper):
    def __init__(self, tg_handler: TelegramClientHandler) -> None:
        self.stupid_jokes_url = "https://www.anekdot.ru/release/anekdot/week/"
        self.frog_text_constructor = frog.FrogTextConstructor()
        self.tg_handler = tg_handler

    @cached(ttl=60 * 60 * 24, serializer=PickleSerializer())
    async def _scrape_stupid_jokes(self) -> list[str]:
        data = await self._get_data_with_soup(self.stupid_jokes_url)
        jokes = data.find_all("div", class_="text")[0:100]
        return [joke.text for joke in jokes]

    async def do_stupid_joke(self) -> str:
        jokes = await self._scrape_stupid_jokes()
        return random.choice(jokes)  # noqa: S311

    @cached(ttl=60 * 60 * 24, serializer=PickleSerializer())
    async def _scrape_category_b_jokes(self) -> list[str]:
        jokes = await self.tg_handler.get_data_from_tg_chanel(channel_id=1743905774, limit=100)
        return [j.text async for j in jokes if j.__getattribute__("photo") is None]

    async def do_category_b_joke(self) -> str:
        data = await self._scrape_category_b_jokes()
        return random.choice(data)  # noqa: S311

    @cached(ttl=60 * 60 * 24, serializer=PickleSerializer())
    async def _scrape_copypastes(self) -> list[int]:
        data = await self.tg_handler.get_data_from_tg_chanel(channel_id=1640385961, limit=300)
        return [cp.id async for cp in data if cp.text is not None and cp.text.find("http") == -1]

    async def do_copypaste(self) -> CopypasteData | None:
        msgs = await self._scrape_copypastes()
        msg_id = random.choice(msgs)  # noqa: S311
        msg = await self.tg_handler.get_message_by_peer_and_id(channel_id=1640385961, msg_id=msg_id)
        if msg is None:
            await self._scrape_copypastes()
            return await self.do_copypaste()
        text = msg.text
        image = None
        if msg.media and isinstance(msg.media, MessageMediaPhoto):
            image = await self.tg_handler.client.download_media(msg.media.photo, "tg_copypaste.jpg")
        return CopypasteData(text=text, image=image)

    async def get_frog(self) -> FrogData:
        dt = datetime.datetime.now(tz=UTC)
        weekday_as_num = dt.weekday()
        frog_link = random.choice(frog.FROG_LINKS[weekday_as_num])  # noqa: S311
        image = await self._get_bytes_from_url(frog_link)
        text = self.frog_text_constructor.create_text(weekday_as_num)
        if image is None:
            text = text + "\nИ, кстати, сегодня без картинок :("
        return FrogData(text=text, image=image)
