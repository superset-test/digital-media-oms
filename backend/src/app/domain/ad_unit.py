"""Ad Unit domain model."""

from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import UUID


@dataclass
class AdUnit:
    """Ad Unit domain model representing specific ad positions within placements."""

    id: UUID | None
    tenant_id: UUID
    placement_id: UUID
    name: str
    description: str | None
    dimensions: str | None
    specifications: dict[str, Any]
    is_active: bool
    created_at: datetime | None
    updated_at: datetime | None

    @staticmethod
    def from_db_row(row) -> "AdUnit":
        """Create AdUnit from database row with name-based column access."""
        return AdUnit(
            id=row["id"],
            tenant_id=row["tenant_id"],
            placement_id=row["placement_id"],
            name=row["name"],
            description=row["description"],
            dimensions=row["dimensions"],
            specifications=row["specifications"],
            is_active=row["is_active"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    def clone_with_id(self, new_id: UUID) -> "AdUnit":
        """Create a copy of this ad unit with a new ID."""
        return AdUnit(
            id=new_id,
            tenant_id=self.tenant_id,
            placement_id=self.placement_id,
            name=self.name,
            description=self.description,
            dimensions=self.dimensions,
            specifications=self.specifications,
            is_active=self.is_active,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
