"""Singleton implementation."""

from typing import ClassVar


class Singleton(type):
    _instances: ClassVar[dict] = {}

    def __call__(cls, *args: int, **kwargs: int) -> dict:
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


__all__ = ["Singleton"]
