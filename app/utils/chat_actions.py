from __future__ import annotations

import asyncio

from aiogram import Bot
from aiogram.utils.chat_action import ChatActionSender


async def send_typing_action(
    bot: Bot,
    chat_id: int,
    duration: float = 0.4,
) -> None:
    async with ChatActionSender.typing(bot=bot, chat_id=chat_id):
        await asyncio.sleep(duration)
