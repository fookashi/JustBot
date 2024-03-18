from io import BytesIO

from .base import BaseModel


class FrogData(BaseModel):
    text: str
    image: BytesIO | None
