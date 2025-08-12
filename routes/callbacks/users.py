from aiogram import Router, F, html, Bot
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from callbacks import UserAction, Action
from keyboards.guest_keyboard import guest_keyboard
from models.user import Role
from storage import Storage
from keyboards import main_keyboard

users_router = Router(name=__name__)


@users_router.callback_query(
    UserAction.filter(F.action == Action.MAKE_EMPLOYEE)
)
async def make_employee_handler(
    query: CallbackQuery,
    callback_data: UserAction,
    storage: Storage,
    bot: Bot,
):
    await query.answer()
    author = query.from_user
    author_from_db = await storage.get_user(author.id)
    if author_from_db:
        if author_from_db.role != Role.ADMIN:
            await query.message.answer("Вы не администратор")
        else:
            user_id = callback_data.user_id
            existing = await storage.get_user(user_id)
            if existing:
                updated = await storage.upsert_user(
                    user_id, existing.full_name, Role.EMPLOYEE
                )
                action = Action.MAKE_GUEST
                kb = InlineKeyboardBuilder()
                kb.button(
                    text=action.value,
                    callback_data=UserAction(action=action, user_id=updated.id),
                )
                await query.message.edit_text(
                    f"{html.italic(updated.full_name)}:{html.bold(updated.role)}",
                    reply_markup=kb.as_markup(),
                )
                await bot.send_message(
                    updated.id,
                    "Доступ предоставлен",
                    reply_markup=main_keyboard(),
                )


@users_router.callback_query(UserAction.filter(F.action == Action.MAKE_GUEST))
async def make_guest_handler(
    query: CallbackQuery,
    callback_data: UserAction,
    storage: Storage,
    bot: Bot,
):
    await query.answer()
    author = query.from_user
    author_from_db = await storage.get_user(author.id)
    if author_from_db:
        if author_from_db.role != Role.ADMIN:
            await query.message.answer("Вы не администратор")
        else:
            user_id = callback_data.user_id
            existing = await storage.get_user(user_id)
            if existing:
                updated = await storage.upsert_user(
                    user_id, existing.full_name, Role.GUEST
                )
                action = Action.MAKE_EMPLOYEE
                kb = InlineKeyboardBuilder()
                kb.button(
                    text=action.value,
                    callback_data=UserAction(action=action, user_id=updated.id),
                )
                await query.message.edit_text(
                    f"{html.italic(updated.full_name)}:{html.bold(updated.role)}",
                    reply_markup=kb.as_markup(),
                )
                await bot.send_message(
                    updated.id, "Доступ отозван", reply_markup=guest_keyboard()
                )
