"""JWT token handling."""

import os
from datetime import datetime, timedelta
from uuid import UUID

from jose import JWTError, jwt


def _get_secret_key() -> str:
    """Get JWT secret key from environment variable.

    Raises:
        ValueError: If JWT_SECRET_KEY is not set
    """
    secret_key = os.getenv("JWT_SECRET_KEY")
    if not secret_key:
        raise ValueError(
            "JWT_SECRET_KEY environment variable is required. "
            "Please set it to a secure random string."
        )
    return secret_key


def create_access_token(
    data: dict,
    tenant_id: UUID,
    user_id: UUID,
    is_super_admin: bool = False,
    expires_delta: timedelta | None = None,
) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    to_encode.update(
        {
            "tenant_id": str(tenant_id),
            "user_id": str(user_id),
            "is_super_admin": is_super_admin,
        }
    )

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        minutes = int(os.getenv("JWT_EXPIRATION_MINUTES", "1440"))
        expire = datetime.utcnow() + timedelta(minutes=minutes)

    to_encode.update({"exp": expire})

    secret_key = _get_secret_key()
    algorithm = os.getenv("JWT_ALGORITHM", "HS256")

    return jwt.encode(to_encode, secret_key, algorithm=algorithm)


def decode_access_token(token: str) -> dict:
    """Decode and validate a JWT access token."""
    try:
        secret_key = _get_secret_key()
        algorithm = os.getenv("JWT_ALGORITHM", "HS256")
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        return payload
    except JWTError as e:
        raise ValueError(f"Invalid token: {e}")
