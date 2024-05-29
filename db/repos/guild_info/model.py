from models.base import BaseModel


class GuildInfo(BaseModel):
    guild_id: int
    music_channel_id: int | None = None
    spam_channel_id: int | None = None
    auto_demo: bool = True
