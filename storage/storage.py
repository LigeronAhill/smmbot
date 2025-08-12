from dataclasses import dataclass
from typing import Optional, List

import asyncpg

from models import Role, User
from .migrate import migrate as apply_migrations


@dataclass
class Storage:
    pool: asyncpg.pool.Pool

    async def migrate(self):
        await apply_migrations(self.pool)

    async def upsert_user(
        self, user_id: int, full_name: str, role: Role
    ) -> User:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                "INSERT INTO users (id, full_name, role) VALUES ($1, $2, $3) ON CONFLICT(id) DO UPDATE set role = EXCLUDED.role RETURNING *;",
                user_id,
                full_name,
                role,
            )
            return User(**row)

    async def get_user(self, user_id: int) -> Optional[User]:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM users WHERE id = $1", user_id
            )
            if row is None:
                return None
            return User(**row)

    async def list_users(self) -> List[User]:
        async with self.pool.acquire() as conn:
            rows = await conn.fetch("SELECT * FROM users")
            return [User(**row) for row in rows]

    async def delete_user(self, user_id: int) -> Optional[User]:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                "DELETE FROM users WHERE id = $1 RETURNING *;", user_id
            )
            if row is None:
                return None
            return User(**row)
