"""FastAPI authentication dependencies."""

from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.auth.jwt import decode_access_token
from app.domain.user import User
from app.services.user_service import UserService

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> User:
    """Get the current authenticated user from JWT token."""
    try:
        payload = decode_access_token(credentials.credentials)
        user_id = UUID(payload.get("user_id"))
        tenant_id = UUID(payload.get("tenant_id"))

        service = UserService()
        user = await service.get_user_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )

        if user.tenant_id != tenant_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token tenant mismatch",
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is inactive",
            )

        return user

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )


async def ensure_current_user_tenant_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    """Ensure current user has admin or manager role."""
    if current_user.role not in ["admin", "manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin or manager role required",
        )
    return current_user


def verify_user_owns_resource(current_user: User, resource_tenant_id: UUID):
    """Verify that the current user's tenant owns the resource."""
    if current_user.tenant_id != resource_tenant_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: resource belongs to different tenant",
        )
