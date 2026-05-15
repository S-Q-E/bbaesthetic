from __future__ import annotations

import logging

from aiogram import F, Router
from aiogram.enums import ChatAction
from aiogram.filters import Command
from aiogram.types import CallbackQuery, FSInputFile, Message

from app.config import Settings
from app.database.repositories import ApplicationRepository
from app.filters import AdminFilter
from app.keyboards import get_processed_admin_keyboard
from app.services import ExportService

logger = logging.getLogger(__name__)


def get_admin_router(settings: Settings) -> Router:
    router = Router(name="admin")
    router.message.filter(AdminFilter(settings.admin_id))
    router.callback_query.filter(AdminFilter(settings.admin_id))

    @router.message(Command("export"))
    async def export_handler(
        message: Message,
        application_repository: ApplicationRepository,
    ) -> None:
        await message.answer("📊 Экспортирую заявки...")

        export_service = ExportService(application_repository, settings.tmp_dir)
        export_result = await export_service.export_applications()

        if export_result is None:
            await message.answer("Заявок пока нет.")
            logger.info("Export skipped: no applications found")
            return

        await message.bot.send_chat_action(
            chat_id=message.chat.id,
            action=ChatAction.UPLOAD_DOCUMENT,
        )

        try:
            document = FSInputFile(
                path=export_result.path,
                filename=export_result.filename,
            )
            await message.answer_document(document=document)
            logger.info(
                "Applications exported by admin_id=%s file=%s",
                message.from_user.id,
                export_result.filename,
            )
        except Exception:
            logger.exception("Failed to export applications")
            await message.answer("Не удалось сформировать Excel-файл. Попробуйте позже.")
        finally:
            export_result.path.unlink(missing_ok=True)

    @router.callback_query(F.data.startswith("processed:"))
    async def processed_handler(callback: CallbackQuery) -> None:
        if not callback.message or not callback.data:
            await callback.answer()
            return

        contact_url = "tg://resolve"
        reply_markup = callback.message.reply_markup
        if reply_markup and reply_markup.inline_keyboard:
            contact_button = reply_markup.inline_keyboard[0][0]
            contact_url = contact_button.url or contact_url

        current_text = callback.message.html_text or callback.message.text or ""
        if "Статус:" not in current_text:
            current_text = f"{current_text}\n\n✅ <b>Статус:</b> обработана"

        await callback.message.edit_text(
            current_text,
            reply_markup=get_processed_admin_keyboard(contact_url),
        )
        await callback.answer("Заявка отмечена как обработанная.")

    return router
