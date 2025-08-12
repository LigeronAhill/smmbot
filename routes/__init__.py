from aiogram import Router

from .commands import commands_router
from .documents import documents_router
from .callbacks import callbacks_router
from .text import text_router

main_router = Router(name=__name__)
main_router.include_routers(
    commands_router, documents_router, callbacks_router, text_router
)
