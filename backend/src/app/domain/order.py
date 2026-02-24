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
        """Create Order from database row with name-based column access."""
        return Order(
            id=row["id"],
            tenant_id=row["tenant_id"],
            advertiser_id=row["advertiser_id"],
            agency_id=row["agency_id"],
            order_number=row["order_number"],
            order_name=row["order_name"],
            status=row["status"],
            start_date=row["start_date"],
            end_date=row["end_date"],
            total_amount=Decimal(str(row["total_amount"])),
            currency=row["currency"],
            payment_terms=row["payment_terms"],
            notes=row["notes"],
            created_by=row["created_by"],
            approved_by=row["approved_by"],
            approved_at=row["approved_at"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
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
