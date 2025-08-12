from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

help_router = Router(name=__name__)


@help_router.message(Command(commands=["help"]))
async def help_command_handler(message: Message):
    await message.delete()
    await message.answer("Тут будет справка")
