import logging
from pathlib import Path

import asyncpg

from models import Role


async def migrate(pool: asyncpg.pool.Pool):
    migrations_dir = Path("migrations")
    if not migrations_dir.exists():
        logging.warning("Migrations directory does not exist")
        return

    async with pool.acquire() as conn:
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS _migrations (
                                                       filename TEXT PRIMARY KEY,
                                                       applied_at TIMESTAMP DEFAULT now()
            );
            """
        )

        applied_migrations = await conn.fetch("SELECT filename FROM _migrations")
        applied = {m["filename"] for m in applied_migrations}

        migration_files = sorted(
            f
            for f in migrations_dir.glob("*.sql")
            if f.is_file() and f.name not in applied
        )

        if not migration_files:
            logging.info("No new migrations to apply")
            return

        logging.info(f"Found {len(migration_files)} new migrations to apply")

        async with conn.transaction():
            for migration_file in migration_files:
                try:
                    sql = migration_file.read_text(encoding="utf-8")
                    await conn.execute(sql)
                    await conn.execute(
                        "INSERT INTO _migrations (filename) VALUES ($1)",
                        migration_file.name,
                    )
                    logging.info(f"Applied migration: {migration_file.name}")
                except Exception as e:
                    logging.error(
                        f"Failed to apply migration {migration_file.name}: {e}"
                    )
                    raise
            await conn.set_type_codec(
                "user_role",
                encoder=str,
                decoder=lambda x: Role(x),
                schema="pg_catalog",
                format="text",
            )
