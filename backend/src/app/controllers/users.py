"""User management and authentication endpoints."""

from datetime import timedelta
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.dependencies import get_current_user
from app.auth.jwt import create_access_token
from app.controllers.models.user_models import (
    AuthRequest,
    AuthResponse,
    ChangePasswordRequest,
    UserCreateRequest,
    UserResponse,
    UsersListResponse,
    UserUpdateRequest,
)
from app.domain.user import User
from app.services.user_service import UserService

router = APIRouter()


@router.post("/auth/login/{tenant_slug}", response_model=AuthResponse)
async def login_with_tenant(tenant_slug: str, request: AuthRequest):
    """Authenticate user within a specific tenant and return JWT token."""
    from app.services.tenant_service import TenantService

    tenant_service = TenantService()
    tenant = await tenant_service.get_tenant_by_slug(tenant_slug)

    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found",
        )

    user_service = UserService()
    user = await user_service.authenticate_user(tenant.id, request.email, request.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token = create_access_token(
        data={"sub": user.email},
        tenant_id=tenant.id,
        user_id=user.id,
    )

    return AuthResponse(
        user=UserResponse.from_domain(user),
        access_token=access_token,
        token_type="bearer",
    )


@router.post("/auth/change-password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    request: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
):
    """Change current user's password."""
    service = UserService()
    success = await service.change_password(
        current_user.id, request.old_password, request.new_password
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid current password",
        )


@router.post(
    "/tenants/{tenant_id}/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def create_user(
    tenant_id: str,
    request: UserCreateRequest,
    current_user: User = Depends(get_current_user),
):
    """Create a new user in a tenant."""
    tenant_uuid = UUID(tenant_id)

    # Verify user can create users in this tenant
    if current_user.tenant_id != tenant_uuid:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot create users in different tenant",
        )

    service = UserService()
    user = await service.create_user(
        tenant_id=tenant_uuid,
        email=request.email,
        password=request.password,
        full_name=request.full_name,
        role=request.role,
    )

    return UserResponse.from_domain(user)


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    current_user: User = Depends(get_current_user),
):
    """Get a user by ID."""
    service = UserService()
    user = await service.get_user_by_id(UUID(user_id))

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    # Verify user can access this user
    if user.tenant_id != current_user.tenant_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot access users from different tenant",
        )

    return UserResponse.from_domain(user)


@router.get("/tenants/{tenant_id}/users", response_model=UsersListResponse)
async def list_tenant_users(
    tenant_id: str,
    active_only: bool = False,
    current_user: User = Depends(get_current_user),
):
    """List users in a tenant."""
    tenant_uuid = UUID(tenant_id)

    if current_user.tenant_id != tenant_uuid:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot list users from different tenant",
        )

    service = UserService()
    users = await service.list_tenant_users(tenant_uuid, active_only)

    return UsersListResponse(
        users=[UserResponse.from_domain(u) for u in users],
        num_records=len(users),
    )


@router.patch("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    request: UserUpdateRequest,
    current_user: User = Depends(get_current_user),
):
    """Update a user."""
    service = UserService()
    user = await service.get_user_by_id(UUID(user_id))

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if user.tenant_id != current_user.tenant_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot update users from different tenant",
        )

    update_data = request.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update",
        )

    updated_user = await service.update_user(UUID(user_id), **update_data)
    return UserResponse.from_domain(updated_user)


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str,
    current_user: User = Depends(get_current_user),
):
    """Delete a user."""
    service = UserService()
    user = await service.get_user_by_id(UUID(user_id))

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if user.tenant_id != current_user.tenant_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot delete users from different tenant",
        )

    await service.delete_user(UUID(user_id))
