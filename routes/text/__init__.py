from aiogram import Router
from .list_users import list_users_router
from .request_access import request_access_router

text_router = Router(name=__name__)
text_router.include_routers(list_users_router, request_access_router)
