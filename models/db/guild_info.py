from .base import DatabaseModel


class GuildInfo(DatabaseModel):
    guild_id: int
    music_channel_id: int | None = None
    spam_channel_id: int | None = None
    auto_demo: bool = True
