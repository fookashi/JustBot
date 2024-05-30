import asyncio
from functools import lru_cache

from motor.motor_asyncio import AsyncIOMotorClient
from pydantic_settings import BaseSettings

# from settings import get_settings


class Settings(BaseSettings):
    BOT_TOKEN: str
    TG_API_ID: str
    TG_API_HASH: str
    MONGO_HOST: str
    MONGO_DB: str
    MONGO_PORT: int
    MONGO_USER: str
    MONGO_PASSWORD: str

    class Config:
        env_file = ".env"


@lru_cache(None)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
uri = f"mongodb://{settings.MONGO_USER}:{settings.MONGO_PASSWORD}@\
mongodb:{settings.MONGO_PORT}"
client = AsyncIOMotorClient(uri)


async def check_connection():
    db = client.get_database("test")
    coll = db.get_collection("test")
    await coll.insert_one({"ok": True})
    print(await coll.find_one({}))


if __name__ == "__main__":
    asyncio.run(check_connection())
