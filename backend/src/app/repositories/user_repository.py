"""User repository for database operations."""

import traceback
from uuid import UUID

import asyncpg

from app.domain.user import User
from app.utils import SingletonMeta, build_update_query

_COLUMNS = (
    "id, tenant_id, email, hashed_password, full_name, role, is_active, "
    "is_super_admin, invited_by_user_id, must_change_password, created_at, updated_at"
)


class UserRepository(metaclass=SingletonMeta):
    """Repository for user database operations."""

    async def create(
        self,
        connection: asyncpg.Connection,
        tenant_id: UUID,
        email: str,
        hashed_password: str,
        full_name: str | None,
        role: str = "user",
        is_active: bool = True,
        is_super_admin: bool = False,
        invited_by_user_id: UUID | None = None,
        must_change_password: bool = False,
    ) -> User:
        """Create a new user."""
        try:
            row = await connection.fetchrow(
                f"""
                INSERT INTO users (tenant_id, email, hashed_password, full_name, role, is_active, 
                                   is_super_admin, invited_by_user_id, must_change_password)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
                RETURNING {_COLUMNS}
                """,
                tenant_id,
                email,
                hashed_password,
                full_name,
                role,
                is_active,
                is_super_admin,
                invited_by_user_id,
                must_change_password,
            )
            return User.from_db_row(row)
        except Exception as e:
            traceback.print_exc()
            raise

    async def get_by_id(self, connection: asyncpg.Connection, user_id: UUID) -> User | None:
        """Get user by ID."""
        try:
            row = await connection.fetchrow(f"SELECT {_COLUMNS} FROM users WHERE id = $1", user_id)
            return User.from_db_row(row) if row else None
        except Exception as e:
            traceback.print_exc()
            raise

    async def get_by_email(
        self, connection: asyncpg.Connection, tenant_id: UUID, email: str
    ) -> User | None:
        """Get user by email within tenant."""
        try:
            row = await connection.fetchrow(
                f"SELECT {_COLUMNS} FROM users WHERE tenant_id = $1 AND email = $2",
                tenant_id,
                email,
            )
            return User.from_db_row(row) if row else None
        except Exception as e:
            traceback.print_exc()
            raise

    async def list_by_tenant(
        self, connection: asyncpg.Connection, tenant_id: UUID, active_only: bool = False
    ) -> list[User]:
        """List users by tenant."""
        try:
            rows = await connection.fetch(
                f"""
                SELECT {_COLUMNS} FROM users
                WHERE tenant_id = $1 AND ($2 = false OR is_active = true)
                ORDER BY email
                """,
                tenant_id,
                active_only,
            )
            return [User.from_db_row(row) for row in rows]
        except Exception as e:
            traceback.print_exc()
            raise

    async def update(self, connection: asyncpg.Connection, user_id: UUID, **kwargs) -> User:
        """Update a user."""
        try:
            query, values = build_update_query("users", _COLUMNS, user_id, **kwargs)
            row = await connection.fetchrow(query, *values)
            return User.from_db_row(row)
        except Exception as e:
            traceback.print_exc()
            raise

    async def delete(self, connection: asyncpg.Connection, user_id: UUID) -> bool:
        """Delete a user."""
        try:
            result = await connection.execute("DELETE FROM users WHERE id = $1", user_id)
            return result.split()[-1] != "0"
        except Exception as e:
            traceback.print_exc()
            raise

    async def get_by_email_global(self, connection: asyncpg.Connection, email: str) -> User | None:
        """Get user by email across all tenants (for super-admin login)."""
        try:
            row = await connection.fetchrow(
                f"SELECT {_COLUMNS} FROM users WHERE email = $1",
                email,
            )
            return User.from_db_row(row) if row else None
        except Exception as e:
            traceback.print_exc()
            raise

    async def create_super_admin(
        self,
        connection: asyncpg.Connection,
        email: str,
        hashed_password: str,
        full_name: str,
    ) -> User:
        """Create a super-admin user in the system tenant."""
        try:
            # Get system tenant ID
            system_tenant_row = await connection.fetchrow(
                "SELECT id FROM tenants WHERE slug = $1", "system"
            )
            if not system_tenant_row:
                raise ValueError("System tenant not found. Please run migration 008 first.")

            system_tenant_id = system_tenant_row["id"]

            # Create super-admin user
            row = await connection.fetchrow(
                f"""
                INSERT INTO users (tenant_id, email, hashed_password, full_name, role, 
                                   is_active, is_super_admin, invited_by_user_id, must_change_password)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
                RETURNING {_COLUMNS}
                """,
                system_tenant_id,
                email,
                hashed_password,
                full_name,
                "super_admin",
                True,
                True,
                None,
                False,
            )
            return User.from_db_row(row)
        except Exception as e:
            traceback.print_exc()
            raise

    async def get_super_admins(self, connection: asyncpg.Connection) -> list[User]:
        """Get all super-admin users."""
        try:
            rows = await connection.fetch(
                f"SELECT {_COLUMNS} FROM users WHERE is_super_admin = true ORDER BY email"
            )
            return [User.from_db_row(row) for row in rows]
        except Exception as e:
            traceback.print_exc()
            raise
