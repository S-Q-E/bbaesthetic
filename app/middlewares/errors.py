from __future__ import annotations

import logging
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject

logger = logging.getLogger(__name__)


class ErrorMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        try:
            return await handler(event, data)
        except Exception:
            logger.exception("Unhandled bot error")

            if isinstance(event, Message):
                await event.answer("Что-то пошло не так. Попробуйте еще раз чуть позже.")
            elif isinstance(event, CallbackQuery):
                await event.answer(
                    "Не удалось выполнить действие. Попробуйте позже.",
                    show_alert=True,
                )

            return None
