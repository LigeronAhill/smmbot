from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class Role(str, Enum):
    ADMIN = "Администратор"
    EMPLOYEE = "Сотрудник"
    GUEST = "Гость"


@dataclass
class User:
    id: int
    full_name: str
    role: Role
    created_at: datetime
