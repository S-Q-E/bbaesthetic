from __future__ import annotations

from aiogram.filters import BaseFilter
from aiogram.types import TelegramObject


class AdminFilter(BaseFilter):
    def __init__(self, admin_id: int) -> None:
        self.admin_id = admin_id

    async def __call__(self, event: TelegramObject) -> bool:
        user = getattr(event, "from_user", None)
        return bool(user and user.id == self.admin_id)
