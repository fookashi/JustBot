from motor.motor_asyncio import AsyncIOMotorClient
from settings import get_settings

settings = get_settings()
uri = f"mongodb://{settings.MONGO_USER}:{settings.MONGO_PASSWORD}@\
mongodb:{settings.MONGO_PORT}"
client = AsyncIOMotorClient(uri)
