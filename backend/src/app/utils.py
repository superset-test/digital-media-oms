"""Utility classes and functions."""

from typing import Any


class SingletonMeta(type):
    """Metaclass for implementing singleton pattern."""

    _instances: dict[type, Any] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
