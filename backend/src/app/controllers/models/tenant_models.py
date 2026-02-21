"""Pydantic models for tenant endpoints."""

from typing import Any

from pydantic import Field

from app.controllers.models.base import AppBaseModel
from app.domain.tenant import Tenant


class TenantCreateRequest(AppBaseModel):
    """Request model for creating a tenant."""

    name: str = Field(description="Tenant name", examples=["Acme Corporation"])
    slug: str = Field(
        description="Unique slug for tenant identification",
        examples=["acme-corp"],
    )
    is_active: bool = Field(default=True, description="Whether tenant is active")
    settings: dict[str, Any] = Field(default_factory=dict, description="Tenant-specific settings")


class TenantUpdateRequest(AppBaseModel):
    """Request model for updating a tenant."""

    name: str | None = Field(None, description="Tenant name")
    slug: str | None = Field(None, description="Unique slug")
    is_active: bool | None = Field(None, description="Whether tenant is active")
    settings: dict[str, Any] | None = Field(None, description="Tenant settings")


class TenantResponse(AppBaseModel):
    """Response model for tenant data."""

    id: str = Field(description="Tenant ID", examples=["123e4567-e89b-12d3-a456-426614174000"])
    name: str = Field(description="Tenant name", examples=["Acme Corporation"])
    slug: str = Field(description="Unique slug", examples=["acme-corp"])
    is_active: bool = Field(description="Whether tenant is active", examples=[True])
    settings: dict[str, Any] = Field(description="Tenant settings", examples=[{}])
    created_at: str | None = Field(description="Creation timestamp")
    updated_at: str | None = Field(description="Last update timestamp")

    @staticmethod
    def from_domain(tenant: Tenant) -> "TenantResponse":
        """Convert domain model to response model."""
        return TenantResponse(
            id=str(tenant.id),
            name=tenant.name,
            slug=tenant.slug,
            is_active=tenant.is_active,
            settings=tenant.settings,
            created_at=tenant.created_at.isoformat() if tenant.created_at else None,
            updated_at=tenant.updated_at.isoformat() if tenant.updated_at else None,
        )


class TenantsListResponse(AppBaseModel):
    """Response model for list of tenants."""

    tenants: list[TenantResponse] = Field(description="List of tenants")
    num_records: int = Field(description="Total number of records", examples=[10])
