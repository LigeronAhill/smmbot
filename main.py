import asyncio
import logging

import asyncpg
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import Config
from middlewares import DatabaseMiddleware
from routes import main_router
from storage import Storage


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    settings = Config("settings.toml")
    dsn = settings.db_config.dsn()
    pool = await asyncpg.create_pool(dsn=dsn, min_size=4, max_size=32)
    storage = Storage(pool)
    await storage.migrate()
    db_middleware = DatabaseMiddleware(storage)
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=MemoryStorage())
    dp.update.middleware(db_middleware)
    dp.include_router(main_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
