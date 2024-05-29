from motor.motor_asyncio import AsyncIOMotorClient

from settings import get_settings

settings = get_settings()
uri = f"mongodb://{settings.MONGO_HOST}/{settings.MONGO_DB}"
client = AsyncIOMotorClient(uri)
