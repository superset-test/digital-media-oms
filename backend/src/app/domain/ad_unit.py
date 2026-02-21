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
        """Create AdUnit from database row with position-based unpacking."""
        return AdUnit(
            id=row[0],
            tenant_id=row[1],
            placement_id=row[2],
            name=row[3],
            description=row[4],
            dimensions=row[5],
            specifications=row[6],
            is_active=row[7],
            created_at=row[8],
            updated_at=row[9],
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
