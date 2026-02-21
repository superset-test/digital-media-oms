"""JWT token handling."""

import os
from datetime import datetime, timedelta
from uuid import UUID

from jose import JWTError, jwt


def create_access_token(
    data: dict, tenant_id: UUID, user_id: UUID, expires_delta: timedelta | None = None
) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    to_encode.update(
        {
            "tenant_id": str(tenant_id),
            "user_id": str(user_id),
        }
    )

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        minutes = int(os.getenv("JWT_EXPIRATION_MINUTES", "1440"))
        expire = datetime.utcnow() + timedelta(minutes=minutes)

    to_encode.update({"exp": expire})

    secret_key = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
    algorithm = os.getenv("JWT_ALGORITHM", "HS256")

    return jwt.encode(to_encode, secret_key, algorithm=algorithm)


def decode_access_token(token: str) -> dict:
    """Decode and validate a JWT access token."""
    try:
        secret_key = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
        algorithm = os.getenv("JWT_ALGORITHM", "HS256")
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        return payload
    except JWTError as e:
        raise ValueError(f"Invalid token: {e}")
