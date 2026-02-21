"""Advertiser domain model."""

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class Advertiser:
    """Advertiser domain model representing companies purchasing advertising."""

    id: UUID | None
    tenant_id: UUID
    name: str
    industry: str | None
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
    def from_db_row(row) -> "Advertiser":
        """Create Advertiser from database row with position-based unpacking."""
        return Advertiser(
            id=row[0],
            tenant_id=row[1],
            name=row[2],
            industry=row[3],
            address=row[4],
            city=row[5],
            state=row[6],
            postal_code=row[7],
            country=row[8],
            phone=row[9],
            email=row[10],
            website=row[11],
            notes=row[12],
            is_active=row[13],
            created_at=row[14],
            updated_at=row[15],
        )

    def clone_with_id(self, new_id: UUID) -> "Advertiser":
        """Create a copy of this advertiser with a new ID."""
        return Advertiser(
            id=new_id,
            tenant_id=self.tenant_id,
            name=self.name,
            industry=self.industry,
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
