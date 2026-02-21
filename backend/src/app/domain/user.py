"""User domain model."""

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class User:
    """User domain model with tenant association."""

    id: UUID | None
    tenant_id: UUID
    email: str
    hashed_password: str
    full_name: str | None
    role: str
    is_active: bool
    created_at: datetime | None
    updated_at: datetime | None

    @staticmethod
    def from_db_row(row) -> "User":
        """Create User from database row with position-based unpacking."""
        return User(
            id=row[0],
            tenant_id=row[1],
            email=row[2],
            hashed_password=row[3],
            full_name=row[4],
            role=row[5],
            is_active=row[6],
            created_at=row[7],
            updated_at=row[8],
        )

    def clone_with_id(self, new_id: UUID) -> "User":
        """Create a copy of this user with a new ID."""
        return User(
            id=new_id,
            tenant_id=self.tenant_id,
            email=self.email,
            hashed_password=self.hashed_password,
            full_name=self.full_name,
            role=self.role,
            is_active=self.is_active,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
