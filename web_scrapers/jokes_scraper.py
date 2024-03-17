import random

from aiocache import cached
from aiocache.serializers import PickleSerializer

from .base_scraper import BaseScrapper
from .tg_scraper import TgScrapper

class JokesScrapper(BaseScrapper):
    def __init__(self):
        self.stupid_jokes_url = "https://www.anekdot.ru/release/anekdot/week/"
        self.category_b_url = "https://baneks.ru/"
        self.tg_scraper = TgScrapper()

    @cached(ttl=60 * 60 * 24, serializer=PickleSerializer())
    async def _scrape_stupid_jokes(self):
        data = await self._get_data_with_soup(self.stupid_jokes_url)
        jokes = data.find_all('div', class_='text')[0:50]
        return [joke.text for joke in jokes]

    async def do_stupid_joke(self):
        jokes = await self._scrape_stupid_jokes()
        return random.choice(jokes)

    @cached(ttl=60 * 60 * 24, serializer=PickleSerializer())
    async def _scrape_category_b_jokes(self):
        jokes = await self.tg_scraper._get_data_from_tg_chanel(1743905774, limit=50)
        return [j.text async for j in jokes if j.__getattribute__('photo') is None]

    async def do_category_b_joke(self):
        data = await self._scrape_category_b_jokes()
        return random.choice(data)
