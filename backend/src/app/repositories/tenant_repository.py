"""Tenant repository for database operations."""

import traceback
from typing import Any
from uuid import UUID

import asyncpg

from app.domain.tenant import Tenant
from app.utils import SingletonMeta, build_update_query

_COLUMNS = "id, name, slug, is_active, settings, created_at, updated_at"


class TenantRepository(metaclass=SingletonMeta):
    """Repository for tenant database operations."""

    async def create(
        self,
        connection: asyncpg.Connection,
        name: str,
        slug: str,
        is_active: bool = True,
        settings: dict[str, Any] | None = None,
    ) -> Tenant:
        """Create a new tenant."""
        try:
            if settings is None:
                settings = {}

            row = await connection.fetchrow(
                f"""
                INSERT INTO tenants (name, slug, is_active, settings)
                VALUES ($1, $2, $3, $4)
                RETURNING {_COLUMNS}
                """,
                name,
                slug,
                is_active,
                settings,
            )
            return Tenant.from_db_row(row)
        except Exception as e:
            traceback.print_exc()
            raise

    async def get_by_id(self, connection: asyncpg.Connection, tenant_id: UUID) -> Tenant | None:
        """Get tenant by ID."""
        try:
            row = await connection.fetchrow(
                f"SELECT {_COLUMNS} FROM tenants WHERE id = $1", tenant_id
            )
            return Tenant.from_db_row(row) if row else None
        except Exception as e:
            traceback.print_exc()
            raise

    async def get_by_slug(self, connection: asyncpg.Connection, slug: str) -> Tenant | None:
        """Get tenant by slug."""
        try:
            row = await connection.fetchrow(f"SELECT {_COLUMNS} FROM tenants WHERE slug = $1", slug)
            return Tenant.from_db_row(row) if row else None
        except Exception as e:
            traceback.print_exc()
            raise

    async def list_all(
        self, connection: asyncpg.Connection, active_only: bool = False
    ) -> list[Tenant]:
        """List all tenants."""
        try:
            rows = await connection.fetch(
                f"""
                SELECT {_COLUMNS} FROM tenants
                WHERE ($1 = false OR is_active = true)
                ORDER BY name
                """,
                active_only,
            )
            return [Tenant.from_db_row(row) for row in rows]
        except Exception as e:
            traceback.print_exc()
            raise

    async def update(self, connection: asyncpg.Connection, tenant_id: UUID, **kwargs) -> Tenant:
        """Update a tenant."""
        try:
            query, values = build_update_query("tenants", _COLUMNS, tenant_id, **kwargs)
            row = await connection.fetchrow(query, *values)
            return Tenant.from_db_row(row)
        except Exception as e:
            traceback.print_exc()
            raise

    async def delete(self, connection: asyncpg.Connection, tenant_id: UUID) -> bool:
        """Delete a tenant."""
        try:
            result = await connection.execute("DELETE FROM tenants WHERE id = $1", tenant_id)
            return result.split()[-1] != "0"
        except Exception as e:
            traceback.print_exc()
            raise
