"""Order domain model."""

from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from uuid import UUID


@dataclass
class Order:
    """Order domain model representing advertising campaign orders."""

    id: UUID | None
    tenant_id: UUID
    advertiser_id: UUID
    agency_id: UUID | None
    order_number: str
    order_name: str
    status: str
    start_date: date
    end_date: date
    total_amount: Decimal
    currency: str
    payment_terms: str | None
    notes: str | None
    created_by: UUID
    approved_by: UUID | None
    approved_at: datetime | None
    created_at: datetime | None
    updated_at: datetime | None

    @staticmethod
    def from_db_row(row) -> "Order":
        """Create Order from database row with position-based unpacking."""
        return Order(
            id=row[0],
            tenant_id=row[1],
            advertiser_id=row[2],
            agency_id=row[3],
            order_number=row[4],
            order_name=row[5],
            status=row[6],
            start_date=row[7],
            end_date=row[8],
            total_amount=Decimal(str(row[9])),
            currency=row[10],
            payment_terms=row[11],
            notes=row[12],
            created_by=row[13],
            approved_by=row[14],
            approved_at=row[15],
            created_at=row[16],
            updated_at=row[17],
        )

    def clone_with_id(self, new_id: UUID) -> "Order":
        """Create a copy of this order with a new ID."""
        return Order(
            id=new_id,
            tenant_id=self.tenant_id,
            advertiser_id=self.advertiser_id,
            agency_id=self.agency_id,
            order_number=self.order_number,
            order_name=self.order_name,
            status=self.status,
            start_date=self.start_date,
            end_date=self.end_date,
            total_amount=self.total_amount,
            currency=self.currency,
            payment_terms=self.payment_terms,
            notes=self.notes,
            created_by=self.created_by,
            approved_by=self.approved_by,
            approved_at=self.approved_at,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
