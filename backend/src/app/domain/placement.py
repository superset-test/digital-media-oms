"""Placement domain model."""

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class Placement:
    """Placement domain model representing advertising inventory categories."""

    id: UUID | None
    tenant_id: UUID
    name: str
    description: str | None
    medium: str
    type: str | None
    is_active: bool
    created_at: datetime | None
    updated_at: datetime | None

    @staticmethod
    def from_db_row(row) -> "Placement":
        """Create Placement from database row with position-based unpacking."""
        return Placement(
            id=row[0],
            tenant_id=row[1],
            name=row[2],
            description=row[3],
            medium=row[4],
            type=row[5],
            is_active=row[6],
            created_at=row[7],
            updated_at=row[8],
        )

    def clone_with_id(self, new_id: UUID) -> "Placement":
        """Create a copy of this placement with a new ID."""
        return Placement(
            id=new_id,
            tenant_id=self.tenant_id,
            name=self.name,
            description=self.description,
            medium=self.medium,
            type=self.type,
            is_active=self.is_active,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
