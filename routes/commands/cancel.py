from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

cancel_router = Router(name=__name__)


@cancel_router.message(Command(commands=["cancel"]))
async def cancel_command_handler(message: Message, state: FSMContext):
    if await state.get_state() is None:
        await message.answer("Состояний нет")
        return

    await state.clear()
    await message.answer("Действие отменено")
