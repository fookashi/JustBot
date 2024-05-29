from types import TracebackType
from typing import Any, Self

from motor import MotorCollection, MotorDatabase
from motor.motor_asyncio import AsyncIOMotorClientSession

from db.config import client
from models.base import BaseModel

__all__ = ["BaseRepo"]


class BaseRepo:
    session: AsyncIOMotorClientSession

    @property
    def __database_name() -> str:
        return "justBotDatabase"

    @property
    def database(self) -> MotorDatabase:
        return client.get_database(self.__database_name)

    @property
    def __collection_name(self) -> str:
        return None

    @property
    def collection(self) -> MotorCollection:
        return client.get_database(self.__collection_name)

    @property
    def model(self) -> type[BaseModel]:
        return None

    async def __aenter__(self) -> Self:
        self.session = client.start_session()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self.session.end_session()

    async def get_one(self, value: Any, key: str) -> BaseModel:  # noqa: ANN401
        key = key or "_id"
        result = await self.collection.find_one({key: value}, session=self.session)
        return self.model(result) if result else None

    async def update_one(self, value: Any, key: str, updated_values: dict) -> None:  # noqa: ANN401
        key = key or "_id"
        result = await self.collection.update_one({key: value}, updated_values, session=self.session)
        return self.model(result) if result else None

    async def remove_one(self, value: Any, key: str) -> None:  # noqa: ANN401
        key = key or "_id"
        await self.collection.delete_one({key: value}, session=self.session)

    async def add_one(self, fields: dict) -> BaseModel:
        new_doc = self.model(fields, session=self.session)
        await self.collection.insert_one(fields)
        return new_doc
