from io import BytesIO

import aiohttp
from bs4 import BeautifulSoup


class BaseScrapper:
    async def _get_data_with_soup(self, url: str) -> BeautifulSoup:
        async with aiohttp.ClientSession() as session, session.get(url) as resp:
            text = await resp.read()

        return BeautifulSoup(text.decode("utf-8"), "html5lib")

    async def _get_bytes_from_url(self, url: str) -> BytesIO | None:
        async with aiohttp.ClientSession() as session, session.get(url) as resp:
            if resp.status != 200:  # noqa: PLR2004
                return None
            return BytesIO(await resp.read())
