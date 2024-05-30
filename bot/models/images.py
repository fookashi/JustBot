from io import BytesIO

from typing_extensions import Annotated

from .base import BaseModel


class ValidatedContentType(str):  # noqa: SLOT000
    @classmethod
    def __get_validators__(cls):  # noqa: ANN102, ANN206
        yield cls.validate

    @classmethod
    def validate(cls, content_type: str):  # noqa: ANN102, ANN206
        if content_type not in ("image/png", "image/jpeg", "image/jpg"):
            msg = "Invalid content type"
            raise ValueError(msg)
        return content_type


class DemotivatorImage(BaseModel):
    name: str
    image: BytesIO


class ImageToDemotivator(BaseModel):
    name: str
    content_type: Annotated[str, ValidatedContentType]
    image: bytes
