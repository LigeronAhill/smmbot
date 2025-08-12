from aiogram import Router, F, html
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.buttons import REQUEST_ACCESS
from models.user import Role
from storage.storage import Storage
from callbacks import UserAction, Action

request_access_router = Router(name=__name__)


@request_access_router.message(F.text == REQUEST_ACCESS)
async def request_access_handler(message: Message, storage: Storage):
    await message.delete()
    users = await storage.list_users()
    for user in users:
        if user.role == Role.ADMIN:
            u = message.from_user
            if u:
                id = u.id
                existing = await storage.get_user(id)
                if existing:
                    action = Action.MAKE_EMPLOYEE
                    kb = InlineKeyboardBuilder()
                    kb.button(
                        text=action.value,
                        callback_data=UserAction(
                            action=action, user_id=existing.id
                        ),
                    )
                    await message.bot.send_message(
                        chat_id=user.id,
                        text=f"Пользователь {html.underline(existing.full_name)}:{html.bold(existing.role)} запрашивает доступ",
                        reply_markup=kb.as_markup(),
                    )
                    await message.answer("Доступ запрошен")
