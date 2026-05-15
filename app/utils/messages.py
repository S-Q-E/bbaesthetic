from __future__ import annotations

from html import escape

from app.database.models import Application


def format_admin_application_message(application: Application) -> str:
    username = (
        f"@{escape(application.telegram_username)}"
        if application.telegram_username
        else "не указан"
    )
    created_at = application.created_at.strftime("%Y-%m-%d %H:%M")

    return (
        "<b>Новая заявка 📩</b>\n\n"
        f"👤 <b>Имя:</b> {escape(application.full_name)}\n"
        f"🎂 <b>Возраст:</b> {application.age}\n"
        f"🏙 <b>Город:</b> {escape(application.city)}\n"
        f"⚖ <b>Цель:</b> -{application.target_weight_loss} кг\n"
        f"📱 <b>Телефон:</b> {escape(application.phone)}\n"
        f"🔗 <b>Telegram:</b> {username}\n"
        f"🕒 <b>Дата:</b> {created_at}"
    )
