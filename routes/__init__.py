from aiogram import Router

from .commands import commands_router

main_router = Router(name=__name__)
main_router.include_routers(commands_router)
