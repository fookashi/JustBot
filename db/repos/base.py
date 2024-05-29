from types import TracebackType
from typing import Any, Self

from motor.motor_asyncio import AsyncIOMotorClientSession, AsyncIOMotorCollection, AsyncIOMotorDatabase

from db.config import client
from models.base import BaseModel

__all__ = ["BaseRepo"]


class BaseRepo:
    session: AsyncIOMotorClientSession

    @property
    def _database(self) -> AsyncIOMotorDatabase:
        return client.get_default_database()

    @property
    def _collection_name(self) -> str:
        return None

    @property
    def collection(self) -> AsyncIOMotorCollection:
        return self._database.get_collection(self._collection_name())

    @property
    def model(self) -> type[BaseModel]:
        return None

    async def __aenter__(self) -> Self:
        self.session = await client.start_session()
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
        doc = await self.collection.find_one({key: value}, session=self.session)
        return self.model(**doc) if doc else None

    async def update_one(self, value: Any, key: str, updated_values: dict) -> None:  # noqa: ANN401
        key = key or "_id"
        doc = await self.collection.update_one({key: value}, updated_values, session=self.session)
        return self.model(**doc) if doc else None

    async def remove_one(self, value: Any, key: str) -> None:  # noqa: ANN401
        key = key or "_id"
        await self.collection.delete_one({key: value}, session=self.session)

    async def add_one(self, fields: dict) -> BaseModel:
        new_doc = self.model(**fields)
        await self.collection.insert_one(new_doc.model_dump(), session=self.session)
        return new_doc
