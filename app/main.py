from __future__ import annotations

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from app.config import get_settings, setup_logging
from app.database import create_engine_and_session
from app.handlers import get_admin_router, get_user_router
from app.middlewares import DatabaseSessionMiddleware, ErrorMiddleware

logger = logging.getLogger(__name__)


async def main() -> None:
    settings = get_settings()
    setup_logging(settings.log_level)

    engine, session_factory = create_engine_and_session(settings.database_url)

    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dispatcher = Dispatcher(storage=MemoryStorage())

    dispatcher.update.outer_middleware(ErrorMiddleware())
    dispatcher.update.middleware(DatabaseSessionMiddleware(session_factory))
    dispatcher.include_router(get_admin_router(settings))
    dispatcher.include_router(get_user_router(settings))

    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Bot started")

    try:
        await dispatcher.start_polling(bot)
    finally:
        await bot.session.close()
        await engine.dispose()
        logger.info("Bot stopped")


if __name__ == "__main__":
    asyncio.run(main())
