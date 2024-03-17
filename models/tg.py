from typing import Any

import telethon.tl.types as tg_type

from ..base_objs.base import BaseModel


class CopypasteData(BaseModel):
    text: str
    image: str | None
