"""Agency repository for database operations."""

import traceback
from uuid import UUID

import asyncpg

from app.domain.agency import Agency
from app.utils import SingletonMeta, build_update_query

_COLUMNS = "id, tenant_id, name, address, city, state, postal_code, country, phone, email, website, notes, is_active, created_at, updated_at"


class AgencyRepository(metaclass=SingletonMeta):
    """Repository for agency database operations."""

    async def create(
        self,
        connection: asyncpg.Connection,
        tenant_id: UUID,
        name: str,
        **optional_fields,
    ) -> Agency:
        """Create a new agency."""
        try:
            row = await connection.fetchrow(
                f"""
                INSERT INTO agencies (
                    tenant_id, name, address, city, state, postal_code,
                    country, phone, email, website, notes, is_active
                )
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
                RETURNING {_COLUMNS}
                """,
                tenant_id,
                name,
                optional_fields.get("address"),
                optional_fields.get("city"),
                optional_fields.get("state"),
                optional_fields.get("postal_code"),
                optional_fields.get("country"),
                optional_fields.get("phone"),
                optional_fields.get("email"),
                optional_fields.get("website"),
                optional_fields.get("notes"),
                optional_fields.get("is_active", True),
            )
            return Agency.from_db_row(row)
        except Exception as e:
            traceback.print_exc()
            raise

    async def get_by_id(self, connection: asyncpg.Connection, agency_id: UUID) -> Agency | None:
        """Get agency by ID."""
        try:
            row = await connection.fetchrow(
                f"SELECT {_COLUMNS} FROM agencies WHERE id = $1", agency_id
            )
            return Agency.from_db_row(row) if row else None
        except Exception as e:
            traceback.print_exc()
            raise

    async def list_by_tenant(
        self,
        connection: asyncpg.Connection,
        tenant_id: UUID,
        active_only: bool = False,
    ) -> list[Agency]:
        """List agencies by tenant."""
        try:
            rows = await connection.fetch(
                f"""
                SELECT {_COLUMNS} FROM agencies
                WHERE tenant_id = $1 AND ($2 = false OR is_active = true)
                ORDER BY name
                """,
                tenant_id,
                active_only,
            )
            return [Agency.from_db_row(row) for row in rows]
        except Exception as e:
            traceback.print_exc()
            raise

    async def search_by_name(
        self, connection: asyncpg.Connection, tenant_id: UUID, name_pattern: str
    ) -> list[Agency]:
        """Search agencies by name pattern."""
        try:
            rows = await connection.fetch(
                f"""
                SELECT {_COLUMNS} FROM agencies
                WHERE tenant_id = $1 AND name ILIKE $2
                ORDER BY name
                """,
                tenant_id,
                f"%{name_pattern}%",
            )
            return [Agency.from_db_row(row) for row in rows]
        except Exception as e:
            traceback.print_exc()
            raise

    async def update(self, connection: asyncpg.Connection, agency_id: UUID, **kwargs) -> Agency:
        """Update an agency."""
        try:
            query, values = build_update_query("agencies", _COLUMNS, agency_id, **kwargs)
            row = await connection.fetchrow(query, *values)
            return Agency.from_db_row(row)
        except Exception as e:
            traceback.print_exc()
            raise

    async def delete(self, connection: asyncpg.Connection, agency_id: UUID) -> bool:
        """Delete an agency."""
        try:
            result = await connection.execute("DELETE FROM agencies WHERE id = $1", agency_id)
            return result.split()[-1] != "0"
        except Exception as e:
            traceback.print_exc()
            raise
