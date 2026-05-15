from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_admin_application_keyboard(
    application_id: int,
    telegram_id: int,
) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Связаться",
                    url=f"tg://user?id={telegram_id}",
                )
            ],
            [
                InlineKeyboardButton(
                    text="Заявка обработана",
                    callback_data=f"processed:{application_id}",
                )
            ],
        ]
    )


def get_processed_admin_keyboard(contact_url: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Связаться",
                    url=contact_url,
                )
            ]
        ]
    )
