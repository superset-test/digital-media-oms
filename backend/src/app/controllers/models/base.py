"""Base Pydantic models for API requests and responses."""

from typing import Any

from pydantic import BaseModel, ConfigDict


def to_lower_camel(string: str) -> str:
    """Convert snake_case to lowerCamelCase."""
    words = string.split("_")
    return words[0] + "".join(word.capitalize() for word in words[1:])


class AppBaseModel(BaseModel):
    """Base model with camelCase serialization and exclude_none by default."""

    model_config = ConfigDict(
        alias_generator=to_lower_camel,
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )

    def dict(self, *args, **kwargs) -> dict[str, Any]:
        """Override dict to always exclude None values."""
        kwargs.pop("exclude_none", None)
        return super().model_dump(*args, exclude_none=True, **kwargs)
