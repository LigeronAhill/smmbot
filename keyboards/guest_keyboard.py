from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from keyboards.buttons import REQUEST_ACCESS


def guest_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text=REQUEST_ACCESS)
    return kb.as_markup(resize_keyboard=True)
