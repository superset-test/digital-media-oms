"""Line Item domain model."""

from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from uuid import UUID


@dataclass
class LineItem:
    """Line Item domain model representing individual ad placements within orders."""

    id: UUID | None
    tenant_id: UUID
    order_id: UUID
    ad_unit_id: UUID
    rate_card_id: UUID | None
    line_number: int
    name: str
    description: str | None
    quantity: int
    unit_price: Decimal
    discount_percentage: Decimal
    subtotal: Decimal
    start_date: date
    end_date: date
    status: str
    delivered_quantity: int
    notes: str | None
    created_at: datetime | None
    updated_at: datetime | None

    @staticmethod
    def from_db_row(row) -> "LineItem":
        """Create LineItem from database row with position-based unpacking."""
        return LineItem(
            id=row[0],
            tenant_id=row[1],
            order_id=row[2],
            ad_unit_id=row[3],
            rate_card_id=row[4],
            line_number=row[5],
            name=row[6],
            description=row[7],
            quantity=row[8],
            unit_price=Decimal(str(row[9])),
            discount_percentage=Decimal(str(row[10])),
            subtotal=Decimal(str(row[11])),
            start_date=row[12],
            end_date=row[13],
            status=row[14],
            delivered_quantity=row[15],
            notes=row[16],
            created_at=row[17],
            updated_at=row[18],
        )

    def clone_with_id(self, new_id: UUID) -> "LineItem":
        """Create a copy of this line item with a new ID."""
        return LineItem(
            id=new_id,
            tenant_id=self.tenant_id,
            order_id=self.order_id,
            ad_unit_id=self.ad_unit_id,
            rate_card_id=self.rate_card_id,
            line_number=self.line_number,
            name=self.name,
            description=self.description,
            quantity=self.quantity,
            unit_price=self.unit_price,
            discount_percentage=self.discount_percentage,
            subtotal=self.subtotal,
            start_date=self.start_date,
            end_date=self.end_date,
            status=self.status,
            delivered_quantity=self.delivered_quantity,
            notes=self.notes,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def calculate_subtotal(self) -> Decimal:
        """Calculate the subtotal for this line item."""
        return self.quantity * self.unit_price * (1 - self.discount_percentage / 100)

    def delivery_percentage(self) -> Decimal:
        """Calculate the delivery completion percentage."""
        if self.quantity > 0:
            return (Decimal(self.delivered_quantity) / Decimal(self.quantity)) * 100
        return Decimal(0)
