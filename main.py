import asyncio
import logging

from aiogram.types import BotCommandScopeDefault
import asyncpg
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from commands import commands

from config import Config
from middlewares import DatabaseMiddleware
from middlewares.vk import VkMiddleware
from routes import main_router
from storage import Storage
from vk_client import VkClient


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
    vk_config = settings.vk
    vk_client = VkClient(vk_config)
    vk_middleware = VkMiddleware(vk_client)
    db_middleware = DatabaseMiddleware(storage)
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    await bot.delete_webhook(drop_pending_updates=True)
    dp = Dispatcher(storage=MemoryStorage())
    dp.update.middleware(db_middleware)
    dp.update.middleware(vk_middleware)
    dp.include_router(main_router)
    try:
        await bot.set_my_commands(commands=commands, scope=BotCommandScopeDefault())
    except Exception as e:
        logging.error(f"{e}")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
