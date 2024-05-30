from typing import ClassVar

from disnake import VoiceProtocol

from .base import BaseModel


class GuildMusicInfo(BaseModel):
    voice: VoiceProtocol | None = None
    playlist: ClassVar[list[str]] = []
    is_playing: bool = False
