from aiogram import Router, F, html
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.buttons import LIST_USERS
from storage.storage import Storage
from callbacks import Action, UserAction

list_users_router = Router(name=__name__)


@list_users_router.message(F.text == LIST_USERS)
async def list_users_handler(message: Message, storage: Storage):
    await message.delete()
    author = message.from_user
    if author:
        users = await storage.list_users()
        for user in users:
            if user.id != author.id:
                kb = InlineKeyboardBuilder()
                for action in Action:
                    kb.button(
                        text=action.value,
                        callback_data=UserAction(
                            action=action, user_id=user.id
                        ),
                    )
                kb.adjust(2)
                await message.answer(
                    f"{html.italic(user.full_name)}:{html.bold(user.role)}",
                    reply_markup=kb.as_markup(),
                )
