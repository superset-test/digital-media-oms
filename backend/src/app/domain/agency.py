"""Agency domain model."""

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class Agency:
    """Agency domain model representing advertising agencies."""

    id: UUID | None
    tenant_id: UUID
    name: str
    address: str | None
    city: str | None
    state: str | None
    postal_code: str | None
    country: str | None
    phone: str | None
    email: str | None
    website: str | None
    notes: str | None
    is_active: bool
    created_at: datetime | None
    updated_at: datetime | None

    @staticmethod
    def from_db_row(row) -> "Agency":
        """Create Agency from database row with position-based unpacking."""
        return Agency(
            id=row[0],
            tenant_id=row[1],
            name=row[2],
            address=row[3],
            city=row[4],
            state=row[5],
            postal_code=row[6],
            country=row[7],
            phone=row[8],
            email=row[9],
            website=row[10],
            notes=row[11],
            is_active=row[12],
            created_at=row[13],
            updated_at=row[14],
        )

    def clone_with_id(self, new_id: UUID) -> "Agency":
        """Create a copy of this agency with a new ID."""
        return Agency(
            id=new_id,
            tenant_id=self.tenant_id,
            name=self.name,
            address=self.address,
            city=self.city,
            state=self.state,
            postal_code=self.postal_code,
            country=self.country,
            phone=self.phone,
            email=self.email,
            website=self.website,
            notes=self.notes,
            is_active=self.is_active,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
