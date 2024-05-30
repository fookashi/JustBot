from .base import BaseModel


class CopypasteData(BaseModel):
    text: str
    image: str | None
