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
        """Create Tenant from database row with position-based unpacking."""
        return Tenant(
            id=row[0],
            name=row[1],
            slug=row[2],
            is_active=row[3],
            settings=row[4],
            created_at=row[5],
            updated_at=row[6],
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
