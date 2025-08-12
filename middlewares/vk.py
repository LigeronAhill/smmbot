from typing import Dict, Any, Callable, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from vk_client import VkClient


class VkMiddleware(BaseMiddleware):
    def __init__(self, vk_client: VkClient):
        self.vk_client = vk_client

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        data["vk_client"] = self.vk_client
        return await handler(event, data)
