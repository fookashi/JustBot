from io import BytesIO

import aiohttp
from bs4 import BeautifulSoup

from interfaces import IWebScraper


class BaseScrapper(IWebScraper):

    async def _get_data_with_soup(self, url: str) -> BeautifulSoup:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                text = await resp.read()

        return BeautifulSoup(text.decode('utf-8'), 'html5lib')

    async def _get_bytes_from_url(self, url: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    return None
                image = BytesIO(await resp.read())
        return image
