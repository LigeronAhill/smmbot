from enum import StrEnum

from aiogram.filters.callback_data import CallbackData


class Action(StrEnum):
    MAKE_EMPLOYEE = "Повысить до сотрудника"
    MAKE_GUEST = "Понизить до гостя"


class UserAction(CallbackData, prefix="user"):
    action: Action
    user_id: int
