from aiogram import Router, html
from aiogram.filters import CommandStart
from aiogram.types import Message
import logging as log

from keyboards import main_keyboard, guest_keyboard
from models import Role
from storage import Storage

start_command_router = Router(name=__name__)


@start_command_router.message(CommandStart())
async def start_command_handler(message: Message, storage: Storage):
    await message.delete()
    if message.from_user:
        user_id = message.from_user.id
        existing_user = await storage.get_user(user_id)
        if existing_user is None:
            full_name = message.from_user.full_name
            role = Role.ADMIN
            all_users = await storage.list_users()
            for user in all_users:
                if user.role == Role.ADMIN:
                    role = Role.GUEST
                    break
            created = await storage.upsert_user(user_id, full_name, role)
            log.info(
                f"Добавлен пользователь {created.full_name}:{created.role}"
            )
            if created.role != Role.GUEST:
                await message.answer(
                    f"Приветствую, {html.bold(created.full_name)}!",
                    reply_markup=main_keyboard(),
                )
            else:
                await message.answer(
                    f"Приветствую, {html.bold(created.full_name)}!",
                    reply_markup=guest_keyboard(),
                )
        else:
            log.info(
                f"Пользователь уже в базе {existing_user.full_name}:{existing_user.role}"
            )
            if existing_user.role != Role.GUEST:
                await message.answer(
                    f"Приветствую, {html.bold(message.from_user.full_name)}!",
                    reply_markup=main_keyboard(),
                )
            else:
                await message.answer(
                    f"Приветствую, {html.bold(message.from_user.full_name)}!",
                    reply_markup=guest_keyboard(),
                )
