"""User service for business logic."""

import secrets
from uuid import UUID

from app.auth.password import PasswordManager
from app.db.postgres import PostgresProvider
from app.domain.user import User
from app.repositories.user_repository import UserRepository
from app.utils import SingletonMeta


class UserService(metaclass=SingletonMeta):
    """Service for user business logic."""

    def __init__(self):
        self.repository = UserRepository()
        self.postgres = PostgresProvider()

    async def create_user(
        self,
        tenant_id: UUID,
        email: str,
        password: str,
        full_name: str | None,
        role: str = "user",
        invited_by_user_id: UUID | None = None,
        must_change_password: bool = False,
    ) -> User:
        """Create a new user with hashed password."""
        connection = await self.postgres.get_default_connection()
        try:
            hashed_password = PasswordManager.get_password_hash(password)
            async with connection.transaction():
                return await self.repository.create(
                    connection,
                    tenant_id,
                    email,
                    hashed_password,
                    full_name,
                    role,
                    is_active=True,
                    is_super_admin=False,
                    invited_by_user_id=invited_by_user_id,
                    must_change_password=must_change_password,
                )
        finally:
            await self.postgres.release_connection(connection)

    async def authenticate_user(self, tenant_id: UUID, email: str, password: str) -> User | None:
        """Authenticate user with email and password."""
        connection = await self.postgres.get_default_connection()
        try:
            user = await self.repository.get_by_email(connection, tenant_id, email)
            if user and PasswordManager.verify_password(password, user.hashed_password):
                return user
            return None
        finally:
            await self.postgres.release_connection(connection)

    async def get_user_by_id(self, user_id: UUID) -> User | None:
        """Get user by ID."""
        connection = await self.postgres.get_default_connection()
        try:
            return await self.repository.get_by_id(connection, user_id)
        finally:
            await self.postgres.release_connection(connection)

    async def list_tenant_users(self, tenant_id: UUID, active_only: bool = False) -> list[User]:
        """List users for a tenant."""
        connection = await self.postgres.get_default_connection()
        try:
            return await self.repository.list_by_tenant(connection, tenant_id, active_only)
        finally:
            await self.postgres.release_connection(connection)

    async def update_user(self, user_id: UUID, **kwargs) -> User:
        """Update a user. If password is provided, hash it first."""
        connection = await self.postgres.get_default_connection()
        try:
            if "password" in kwargs:
                kwargs["hashed_password"] = PasswordManager.get_password_hash(
                    kwargs.pop("password")
                )
            async with connection.transaction():
                return await self.repository.update(connection, user_id, **kwargs)
        finally:
            await self.postgres.release_connection(connection)

    async def change_password(self, user_id: UUID, old_password: str, new_password: str) -> bool:
        """Change user password after verifying old password."""
        connection = await self.postgres.get_default_connection()
        try:
            user = await self.repository.get_by_id(connection, user_id)
            if not user or not PasswordManager.verify_password(old_password, user.hashed_password):
                return False

            new_hashed = PasswordManager.get_password_hash(new_password)
            async with connection.transaction():
                await self.repository.update(
                    connection, user_id, hashed_password=new_hashed, must_change_password=False
                )
            return True
        finally:
            await self.postgres.release_connection(connection)

    async def deactivate_user(self, user_id: UUID) -> User:
        """Deactivate a user."""
        return await self.update_user(user_id, is_active=False)

    async def delete_user(self, user_id: UUID) -> bool:
        """Delete a user."""
        connection = await self.postgres.get_default_connection()
        try:
            async with connection.transaction():
                return await self.repository.delete(connection, user_id)
        finally:
            await self.postgres.release_connection(connection)

    async def create_super_admin(self, email: str, password: str, full_name: str) -> User:
        """Create a super-admin user."""
        connection = await self.postgres.get_default_connection()
        try:
            hashed_password = PasswordManager.get_password_hash(password)
            async with connection.transaction():
                return await self.repository.create_super_admin(
                    connection, email, hashed_password, full_name
                )
        finally:
            await self.postgres.release_connection(connection)

    async def authenticate_super_admin(self, email: str, password: str) -> User | None:
        """Authenticate super-admin with email and password across all tenants."""
        connection = await self.postgres.get_default_connection()
        try:
            user = await self.repository.get_by_email_global(connection, email)
            if (
                user
                and user.is_super_admin
                and PasswordManager.verify_password(password, user.hashed_password)
            ):
                return user
            return None
        finally:
            await self.postgres.release_connection(connection)

    async def invite_user(
        self,
        tenant_id: UUID,
        email: str,
        full_name: str,
        role: str,
        invited_by_user_id: UUID,
    ) -> tuple[User, str]:
        """Invite a user with a generated temporary password.

        Returns:
            Tuple of (User, temporary_password)
        """
        # Generate secure temporary password
        temporary_password = secrets.token_urlsafe(16)

        # Create user with must_change_password=True
        user = await self.create_user(
            tenant_id=tenant_id,
            email=email,
            password=temporary_password,
            full_name=full_name,
            role=role,
            invited_by_user_id=invited_by_user_id,
            must_change_password=True,
        )

        return user, temporary_password
