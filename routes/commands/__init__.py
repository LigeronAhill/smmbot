from aiogram import Router

from .start import start_command_router
from .cancel import cancel_router
from .help import help_router

commands_router = Router(name=__name__)
commands_router.include_routers(
    start_command_router, cancel_router, help_router
)
