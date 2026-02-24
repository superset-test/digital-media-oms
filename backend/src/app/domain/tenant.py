"""Tenant domain model."""

from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import UUID


@dataclass
class Tenant:
    """Tenant domain model representing a multi-tenant organization."""

    id: UUID | None
    name: str
    slug: str
    is_active: bool
    settings: dict[str, Any]
    created_at: datetime | None
    updated_at: datetime | None

    @staticmethod
    def from_db_row(row) -> "Tenant":
        """Create Tenant from database row with name-based column access."""
        return Tenant(
            id=row["id"],
            name=row["name"],
            slug=row["slug"],
            is_active=row["is_active"],
            settings=row["settings"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    def clone_with_id(self, new_id: UUID) -> "Tenant":
        """Create a copy of this tenant with a new ID."""
        return Tenant(
            id=new_id,
            name=self.name,
            slug=self.slug,
            is_active=self.is_active,
            settings=self.settings,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
