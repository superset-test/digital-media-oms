"""PostgreSQL database provider using asyncpg."""

import json
import os
import traceback
from typing import Any, Optional

import asyncpg

from app.utils import SingletonMeta


class PostgresProvider(metaclass=SingletonMeta):
    """Singleton PostgreSQL connection pool provider."""

    def __init__(self):
        self.pool: Optional[asyncpg.Pool] = None
        self.schema = os.getenv("POSTGRES_SCHEMA", "public")

    async def init(self):
        """Initialize the connection pool."""
        try:
            self.pool = await asyncpg.create_pool(
                user=os.getenv("POSTGRES_DB_USER"),
                password=os.getenv("POSTGRES_DB_PASSWORD"),
                host=os.getenv("POSTGRES_DB_HOST"),
                port=int(os.getenv("POSTGRES_DB_PORT", "5432")),
                database=os.getenv("POSTGRES_DATABASE"),
                ssl=os.getenv("POSTGRES_SSL_MODE", "prefer"),
                server_settings={"search_path": self.schema},
                min_size=5,
                max_size=20,
            )

            # Set up JSONB codec
            async def _init_connection(conn):
                await conn.set_type_codec(
                    "jsonb",
                    encoder=json.dumps,
                    decoder=json.loads,
                    schema="pg_catalog",
                )

            if self.pool:
                async with self.pool.acquire() as conn:
                    await _init_connection(conn)

            print(f"PostgreSQL pool initialized for schema: {self.schema}")
        except Exception as e:
            traceback.print_exc()
            raise RuntimeError(f"Failed to initialize PostgreSQL pool: {e}")

    async def get_default_connection(self) -> asyncpg.Connection:
        """Acquire a connection from the pool."""
        if not self.pool:
            await self.init()
        if not self.pool:
            raise RuntimeError("PostgreSQL pool not initialized")
        return await self.pool.acquire()

    async def release_connection(self, connection: asyncpg.Connection):
        """Release a connection back to the pool."""
        if self.pool and connection:
            await self.pool.release(connection)

    async def shutdown(self):
        """Close the connection pool."""
        if self.pool:
            await self.pool.close()
            print("PostgreSQL pool closed")
