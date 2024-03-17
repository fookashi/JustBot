from functools import lru_cache

from pydantic_settings import BaseSettings
from pydantic import SecretStr


class Settings(BaseSettings):
    bot_token: SecretStr
    tg_api_id: SecretStr
    tg_api_hash: SecretStr

    class Config:
        env_file = ".env"

    def get_secrets(self):
        return {key: value.get_secret_value() for key, value in self.model_dump().items()}


def get_settings():
    return Settings()
