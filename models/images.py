from typing_extensions import Annotated
from io import BytesIO

from .base import BaseModel


class ValidatedContentType(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if v not in ('image/png', 'image/jpeg', 'image/jpg'):
            raise ValueError('Invalid content type')
        return v


class DemotivatorImage(BaseModel):
    name: str
    image: BytesIO


class ImageToDemotivator(BaseModel):
    name: str
    content_type: Annotated[str, ValidatedContentType]
    image: bytes
