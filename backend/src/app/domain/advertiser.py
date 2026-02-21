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
        """Create Advertiser from database row with name-based column access."""
        return Advertiser(
            id=row["id"],
            tenant_id=row["tenant_id"],
            name=row["name"],
            industry=row["industry"],
            address=row["address"],
            city=row["city"],
            state=row["state"],
            postal_code=row["postal_code"],
            country=row["country"],
            phone=row["phone"],
            email=row["email"],
            website=row["website"],
            notes=row["notes"],
            is_active=row["is_active"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
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
