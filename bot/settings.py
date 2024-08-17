from functools import lru_cache

from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    BOT_TOKEN: str
    TG_API_ID: str
    TG_API_HASH: str
    MONGO_HOST: str
    MONGO_DB: str
    MONGO_PORT: int
    MONGO_USER: str = Field(default="")
    MONGO_PASSWORD: str = Field(default="")

    class Config:
        env_file = ".env"


@lru_cache(None)
def get_settings() -> Settings:
    return Settings()
