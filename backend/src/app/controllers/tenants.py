"""Tenant management endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.dependencies import ensure_current_user_super_admin
from app.controllers.models.tenant_models import (
    TenantAdminCreateRequest,
    TenantCreateRequest,
    TenantResponse,
    TenantsListResponse,
    TenantUpdateRequest,
)
from app.controllers.models.user_models import UserResponse
from app.domain.user import User
from app.services.tenant_service import TenantService

router = APIRouter()


@router.post("/tenants", response_model=TenantResponse, status_code=status.HTTP_201_CREATED)
async def create_tenant(
    request: TenantCreateRequest,
    current_user: User = Depends(ensure_current_user_super_admin),
):
    """Create a new tenant."""
    service = TenantService()
    tenant = await service.create_tenant(
        name=request.name,
        slug=request.slug,
        is_active=request.is_active,
        settings=request.settings,
    )
    return TenantResponse.from_domain(tenant)


@router.get("/tenants/{tenant_id}", response_model=TenantResponse)
async def get_tenant(
    tenant_id: str,
    current_user: User = Depends(ensure_current_user_super_admin),
):
    """Get a tenant by ID."""
    service = TenantService()
    tenant = await service.get_tenant_by_id(UUID(tenant_id))

    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found",
        )

    return TenantResponse.from_domain(tenant)


@router.get("/tenants", response_model=TenantsListResponse)
async def list_tenants(
    active_only: bool = False,
    current_user: User = Depends(ensure_current_user_super_admin),
):
    """List all tenants."""
    service = TenantService()
    tenants = await service.list_tenants(active_only=active_only)

    return TenantsListResponse(
        tenants=[TenantResponse.from_domain(t) for t in tenants],
        num_records=len(tenants),
    )


@router.patch("/tenants/{tenant_id}", response_model=TenantResponse)
async def update_tenant(
    tenant_id: str,
    request: TenantUpdateRequest,
    current_user: User = Depends(ensure_current_user_super_admin),
):
    """Update a tenant."""
    service = TenantService()

    update_data = request.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update",
        )

    tenant = await service.update_tenant(UUID(tenant_id), **update_data)
    return TenantResponse.from_domain(tenant)


@router.delete("/tenants/{tenant_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tenant(
    tenant_id: str,
    current_user: User = Depends(ensure_current_user_super_admin),
):
    """Delete a tenant."""
    service = TenantService()
    deleted = await service.delete_tenant(UUID(tenant_id))

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found",
        )


@router.post(
    "/tenants/{tenant_id}/admin", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def create_tenant_admin(
    tenant_id: str,
    request: TenantAdminCreateRequest,
    current_user: User = Depends(ensure_current_user_super_admin),
):
    """Create an admin user for a tenant (super-admin only)."""
    service = TenantService()
    tenant_uuid = UUID(tenant_id)

    # Verify tenant exists
    tenant = await service.get_tenant_by_id(tenant_uuid)
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found",
        )

    # Create admin user
    user = await service.create_tenant_admin(
        tenant_id=tenant_uuid,
        email=request.email,
        password=request.password,
        full_name=request.full_name,
        created_by_super_admin_id=current_user.id,
    )

    return UserResponse.from_domain(user)
