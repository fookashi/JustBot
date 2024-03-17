from abc import ABC, abstractmethod


class IWebScraper(ABC):
    @abstractmethod
    async def _get_data_with_soup(self, *args, **kwargs):
        raise NotImplementedError
