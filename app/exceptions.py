from __future__ import annotations


class BotException(Exception):
    """Базовое исключение для всех ошибок бота."""

    def __init__(self, message: str, user_message: str | None = None) -> None:
        """
        Args:
            message: Сообщение для логирования
            user_message: Сообщение для отправки пользователю (если None, используется message)
        """
        self.message = message
        self.user_message = user_message or message
        super().__init__(self.message)


class ValidationError(BotException):
    """Ошибка валидации данных."""

    pass


class DatabaseError(BotException):
    """Ошибка работы с базой данных."""

    def __init__(self, message: str) -> None:
        super().__init__(
            message,
            user_message="❌ Ошибка при сохранении данных. Попробуйте позже.",
        )


class ExportError(BotException):
    """Ошибка при экспорте данных."""

    def __init__(self, message: str) -> None:
        super().__init__(
            message,
            user_message="❌ Не удалось сформировать Excel-файл. Попробуйте позже.",
        )


class TelegramAPIError(BotException):
    """Ошибка Telegram API."""

    def __init__(self, message: str) -> None:
        super().__init__(
            message,
            user_message="⚠️ Временная ошибка при отправке сообщения. Попробуйте позже.",
        )
