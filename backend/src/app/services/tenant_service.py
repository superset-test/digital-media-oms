"""Tenant service for business logic."""

from typing import Any
from uuid import UUID

from app.db.postgres import PostgresProvider
from app.domain.tenant import Tenant
from app.repositories.tenant_repository import TenantRepository
from app.utils import SingletonMeta


class TenantService(metaclass=SingletonMeta):
    """Service for tenant business logic."""

    def __init__(self):
        self.repository = TenantRepository()
        self.postgres = PostgresProvider()

    async def create_tenant(
        self,
        name: str,
        slug: str,
        is_active: bool = True,
        settings: dict[str, Any] | None = None,
    ) -> Tenant:
        """Create a new tenant."""
        connection = await self.postgres.get_default_connection()
        try:
            async with connection.transaction():
                return await self.repository.create(connection, name, slug, is_active, settings)
        finally:
            await self.postgres.release_connection(connection)

    async def get_tenant_by_id(self, tenant_id: UUID) -> Tenant | None:
        """Get tenant by ID."""
        connection = await self.postgres.get_default_connection()
        try:
            return await self.repository.get_by_id(connection, tenant_id)
        finally:
            await self.postgres.release_connection(connection)

    async def get_tenant_by_slug(self, slug: str) -> Tenant | None:
        """Get tenant by slug."""
        connection = await self.postgres.get_default_connection()
        try:
            return await self.repository.get_by_slug(connection, slug)
        finally:
            await self.postgres.release_connection(connection)

    async def list_tenants(self, active_only: bool = False) -> list[Tenant]:
        """List all tenants."""
        connection = await self.postgres.get_default_connection()
        try:
            return await self.repository.list_all(connection, active_only)
        finally:
            await self.postgres.release_connection(connection)

    async def update_tenant(self, tenant_id: UUID, **kwargs) -> Tenant:
        """Update a tenant."""
        connection = await self.postgres.get_default_connection()
        try:
            async with connection.transaction():
                return await self.repository.update(connection, tenant_id, **kwargs)
        finally:
            await self.postgres.release_connection(connection)

    async def deactivate_tenant(self, tenant_id: UUID) -> Tenant:
        """Deactivate a tenant."""
        return await self.update_tenant(tenant_id, is_active=False)

    async def delete_tenant(self, tenant_id: UUID) -> bool:
        """Delete a tenant."""
        connection = await self.postgres.get_default_connection()
        try:
            async with connection.transaction():
                return await self.repository.delete(connection, tenant_id)
        finally:
            await self.postgres.release_connection(connection)
