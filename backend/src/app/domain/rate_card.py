"""Rate Card domain model."""

from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from uuid import UUID


@dataclass
class RateCard:
    """Rate Card domain model representing pricing for ad units."""

    id: UUID | None
    tenant_id: UUID
    ad_unit_id: UUID
    name: str
    effective_date: date
    expiration_date: date | None
    base_rate: Decimal
    currency: str
    rate_type: str
    minimum_quantity: int
    discount_percentage: Decimal
    notes: str | None
    is_active: bool
    created_at: datetime | None
    updated_at: datetime | None

    @staticmethod
    def from_db_row(row) -> "RateCard":
        """Create RateCard from database row with position-based unpacking."""
        return RateCard(
            id=row[0],
            tenant_id=row[1],
            ad_unit_id=row[2],
            name=row[3],
            effective_date=row[4],
            expiration_date=row[5],
            base_rate=Decimal(str(row[6])),
            currency=row[7],
            rate_type=row[8],
            minimum_quantity=row[9],
            discount_percentage=Decimal(str(row[10])),
            notes=row[11],
            is_active=row[12],
            created_at=row[13],
            updated_at=row[14],
        )

    def clone_with_id(self, new_id: UUID) -> "RateCard":
        """Create a copy of this rate card with a new ID."""
        return RateCard(
            id=new_id,
            tenant_id=self.tenant_id,
            ad_unit_id=self.ad_unit_id,
            name=self.name,
            effective_date=self.effective_date,
            expiration_date=self.expiration_date,
            base_rate=self.base_rate,
            currency=self.currency,
            rate_type=self.rate_type,
            minimum_quantity=self.minimum_quantity,
            discount_percentage=self.discount_percentage,
            notes=self.notes,
            is_active=self.is_active,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def calculate_effective_rate(self) -> Decimal:
        """Calculate the effective rate after applying discount."""
        return self.base_rate * (1 - self.discount_percentage / 100)
