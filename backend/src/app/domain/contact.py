"""Contact domain model."""

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class Contact:
    """Contact domain model for agency or advertiser contacts."""

    id: UUID | None
    tenant_id: UUID
    agency_id: UUID | None
    advertiser_id: UUID | None
    first_name: str
    last_name: str
    title: str | None
    email: str
    phone: str | None
    mobile: str | None
    notes: str | None
    is_primary: bool
    is_active: bool
    created_at: datetime | None
    updated_at: datetime | None

    @staticmethod
    def from_db_row(row) -> "Contact":
        """Create Contact from database row with name-based column access."""
        return Contact(
            id=row["id"],
            tenant_id=row["tenant_id"],
            agency_id=row["agency_id"],
            advertiser_id=row["advertiser_id"],
            first_name=row["first_name"],
            last_name=row["last_name"],
            title=row["title"],
            email=row["email"],
            phone=row["phone"],
            mobile=row["mobile"],
            notes=row["notes"],
            is_primary=row["is_primary"],
            is_active=row["is_active"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    def clone_with_id(self, new_id: UUID) -> "Contact":
        """Create a copy of this contact with a new ID."""
        return Contact(
            id=new_id,
            tenant_id=self.tenant_id,
            agency_id=self.agency_id,
            advertiser_id=self.advertiser_id,
            first_name=self.first_name,
            last_name=self.last_name,
            title=self.title,
            email=self.email,
            phone=self.phone,
            mobile=self.mobile,
            notes=self.notes,
            is_primary=self.is_primary,
            is_active=self.is_active,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def full_name(self) -> str:
        """Get the full name of the contact."""
        return f"{self.first_name} {self.last_name}"
