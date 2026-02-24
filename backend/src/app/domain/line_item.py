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
        """Create LineItem from database row with name-based column access."""
        return LineItem(
            id=row["id"],
            tenant_id=row["tenant_id"],
            order_id=row["order_id"],
            ad_unit_id=row["ad_unit_id"],
            rate_card_id=row["rate_card_id"],
            line_number=row["line_number"],
            name=row["name"],
            description=row["description"],
            quantity=row["quantity"],
            unit_price=Decimal(str(row["unit_price"])),
            discount_percentage=Decimal(str(row["discount_percentage"])),
            subtotal=Decimal(str(row["subtotal"])),
            start_date=row["start_date"],
            end_date=row["end_date"],
            status=row["status"],
            delivered_quantity=row["delivered_quantity"],
            notes=row["notes"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
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
