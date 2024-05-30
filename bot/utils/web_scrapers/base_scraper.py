from io import BytesIO

import aiohttp
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


class ScraperError(Exception): ...


class BadResponseError(ScraperError): ...


class BaseScrapper:
    ua: UserAgent = UserAgent()

    async def _get_data_with_soup(self, url: str) -> BeautifulSoup:
        async with aiohttp.ClientSession() as session, session.get(url) as resp:
            text = await resp.read()

        return BeautifulSoup(text.decode("utf-8"), "html5lib")

    async def _get_bytes_from_url(self, url: str) -> BytesIO | None:
        headers = {
            "User-Agent": self.ua.random,
            "Accept": "*/*",
        }
        async with aiohttp.ClientSession(headers=headers) as session, session.get(url) as resp:
            if resp.status != 200:  # noqa: PLR2004
                msg = f"\nStatus code: {resp.status}\nResponse: {await resp.read()}\nHeaders:{resp.headers}"
                raise BadResponseError(msg)
            return BytesIO(await resp.read())
