from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from keyboards.buttons import ADD_USER, CREATE_POST, LIST_POSTS, LIST_USERS


def main_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    create_post = KeyboardButton(text=CREATE_POST)
    list_posts = KeyboardButton(text=LIST_POSTS)
    kb.row(create_post, list_posts)
    add_user = KeyboardButton(text=ADD_USER)
    list_users = KeyboardButton(text=LIST_USERS)
    kb.row(add_user, list_users)
    return kb.as_markup(resize_keyboard=True)
