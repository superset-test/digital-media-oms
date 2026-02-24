"""Pydantic models for user endpoints."""

from pydantic import Field

from app.controllers.models.base import AppBaseModel
from app.domain.user import User


class UserCreateRequest(AppBaseModel):
    """Request model for creating a user."""

    email: str = Field(description="User email address", examples=["user@example.com"])
    password: str = Field(description="User password", examples=["SecurePass123!"])
    full_name: str | None = Field(None, description="Full name", examples=["John Doe"])
    role: str = Field(
        default="user", description="User role", examples=["user", "admin", "manager"]
    )
    invited_by_user_id: str | None = Field(None, description="ID of user who invited this user")


class UserUpdateRequest(AppBaseModel):
    """Request model for updating a user."""

    email: str | None = Field(None, description="User email address")
    full_name: str | None = Field(None, description="Full name")
    role: str | None = Field(None, description="User role")
    is_active: bool | None = Field(None, description="Whether user is active")


class ChangePasswordRequest(AppBaseModel):
    """Request model for changing password."""

    old_password: str = Field(description="Current password")
    new_password: str = Field(description="New password")


class UserResponse(AppBaseModel):
    """Response model for user data."""

    id: str = Field(description="User ID", examples=["123e4567-e89b-12d3-a456-426614174000"])
    tenant_id: str = Field(description="Tenant ID")
    email: str = Field(description="User email", examples=["user@example.com"])
    full_name: str | None = Field(description="Full name", examples=["John Doe"])
    role: str = Field(description="User role", examples=["user"])
    is_active: bool = Field(description="Whether user is active", examples=[True])
    is_super_admin: bool = Field(description="Whether user is a super-admin", examples=[False])
    invited_by_user_id: str | None = Field(None, description="ID of user who invited this user")
    created_at: str | None = Field(description="Creation timestamp")
    updated_at: str | None = Field(description="Last update timestamp")

    @staticmethod
    def from_domain(user: User) -> "UserResponse":
        """Convert domain model to response model."""
        return UserResponse(
            id=str(user.id),
            tenant_id=str(user.tenant_id),
            email=user.email,
            full_name=user.full_name,
            role=user.role,
            is_active=user.is_active,
            is_super_admin=user.is_super_admin,
            invited_by_user_id=str(user.invited_by_user_id) if user.invited_by_user_id else None,
            created_at=user.created_at.isoformat() if user.created_at else None,
            updated_at=user.updated_at.isoformat() if user.updated_at else None,
        )


class UsersListResponse(AppBaseModel):
    """Response model for list of users."""

    users: list[UserResponse] = Field(description="List of users")
    num_records: int = Field(description="Total number of records", examples=[5])


class AuthRequest(AppBaseModel):
    """Request model for authentication."""

    email: str = Field(description="User email address", examples=["user@example.com"])
    password: str = Field(description="User password", examples=["SecurePass123!"])


class AuthResponse(AppBaseModel):
    """Response model for authentication."""

    user: UserResponse = Field(description="Authenticated user")
    access_token: str = Field(description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")


class UserInviteRequest(AppBaseModel):
    """Request model for inviting a user."""

    email: str = Field(description="User email address", examples=["newuser@example.com"])
    full_name: str = Field(description="Full name", examples=["Jane Doe"])
    role: str = Field(default="user", description="User role", examples=["user", "manager"])


class UserInviteResponse(AppBaseModel):
    """Response model for user invitation."""

    user: UserResponse = Field(description="Created user")
    temporary_password: str = Field(
        description="Temporary password (must be changed on first login)"
    )
