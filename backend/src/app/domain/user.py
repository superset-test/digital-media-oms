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
        """Create User from database row with name-based column access."""
        return User(
            id=row["id"],
            tenant_id=row["tenant_id"],
            email=row["email"],
            hashed_password=row["hashed_password"],
            full_name=row["full_name"],
            role=row["role"],
            is_active=row["is_active"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
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
