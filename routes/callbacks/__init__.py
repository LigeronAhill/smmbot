from aiogram import Router
from .users import users_router

callbacks_router = Router(name=__name__)
callbacks_router.include_routers(users_router)
