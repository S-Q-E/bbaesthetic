from __future__ import annotations

import logging

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.config import Settings
from app.database.repositories import ApplicationRepository
from app.keyboards import (
    get_admin_application_keyboard,
    get_contact_keyboard,
    get_start_keyboard,
    remove_keyboard,
)
from app.services import ApplicationCreateDTO, ApplicationService
from app.states import ApplicationForm
from app.utils import (
    format_admin_application_message,
    normalize_phone,
    send_typing_action,
    validate_age,
    validate_name,
    validate_target_weight_loss,
    validate_text_value,
)

logger = logging.getLogger(__name__)


def get_user_router(settings: Settings) -> Router:
    router = Router(name="user")

    @router.message(CommandStart())
    async def start_handler(message: Message, state: FSMContext) -> None:
        await state.clear()
        await send_typing_action(message.bot, message.chat.id)
        await message.answer(
            "Здравствуйте 👋\n"
            "Добро пожаловать в BB Aesthetic Lab.\n\n"
            "Оставьте свои данные для записи на консультацию\n"
            "Это займет меньше минуты 😊",
            reply_markup=get_start_keyboard(),
        )

    @router.message(Command("cancel"))
    async def cancel_handler(message: Message, state: FSMContext) -> None:
        await state.clear()
        await message.answer(
            "Текущая заявка отменена. Если захотите начать заново, нажмите кнопку ниже.",
            reply_markup=get_start_keyboard(),
        )

    @router.message(F.text, F.text.casefold() == "оставить заявку")
    async def begin_application_handler(message: Message, state: FSMContext) -> None:
        await state.set_state(ApplicationForm.full_name)
        await send_typing_action(message.bot, message.chat.id)
        await message.answer("Как вас зовут?", reply_markup=remove_keyboard())

    @router.message(ApplicationForm.full_name)
    async def full_name_handler(message: Message, state: FSMContext) -> None:
        if not message.text:
            await message.answer("Напишите ваше имя текстом.")
            return

        try:
            full_name = validate_name(message.text)
        except ValueError as error:
            await message.answer(str(error))
            return

        await state.update_data(full_name=full_name)
        await state.set_state(ApplicationForm.age)
        await send_typing_action(message.bot, message.chat.id)
        await message.answer("Сколько вам лет?")

    @router.message(ApplicationForm.age)
    async def age_handler(message: Message, state: FSMContext) -> None:
        if not message.text:
            await message.answer("Возраст нужно указать цифрами.")
            return

        try:
            age = validate_age(message.text)
        except ValueError as error:
            await message.answer(str(error))
            return

        await state.update_data(age=age)
        await state.set_state(ApplicationForm.city)
        await send_typing_action(message.bot, message.chat.id)
        await message.answer("Из какого вы города?")

    @router.message(ApplicationForm.city)
    async def city_handler(message: Message, state: FSMContext) -> None:
        if not message.text:
            await message.answer("Напишите город текстом.")
            return

        try:
            city = validate_text_value(message.text, field_name="Город")
        except ValueError as error:
            await message.answer(str(error))
            return

        await state.update_data(city=city)
        await state.set_state(ApplicationForm.target_weight_loss)
        await send_typing_action(message.bot, message.chat.id)
        await message.answer("Сколько кг хотите сбросить?")

    @router.message(ApplicationForm.target_weight_loss)
    async def target_weight_loss_handler(message: Message, state: FSMContext) -> None:
        if not message.text:
            await message.answer("Укажите цель похудения цифрами.")
            return

        try:
            target_weight_loss = validate_target_weight_loss(message.text)
        except ValueError as error:
            await message.answer(str(error))
            return

        await state.update_data(target_weight_loss=target_weight_loss)
        await state.set_state(ApplicationForm.phone)
        await send_typing_action(message.bot, message.chat.id)
        await message.answer(
            "Отправьте номер телефона",
            reply_markup=get_contact_keyboard(),
        )

    @router.message(ApplicationForm.phone, F.contact)
    async def phone_handler(
        message: Message,
        state: FSMContext,
        application_repository: ApplicationRepository,
    ) -> None:
        if not message.contact:
            await message.answer("Пожалуйста, используйте кнопку для отправки номера.")
            return

        if message.contact.user_id and message.contact.user_id != message.from_user.id:
            await message.answer("Отправьте, пожалуйста, свой номер через кнопку ниже.")
            return

        try:
            phone = normalize_phone(message.contact.phone_number)
        except ValueError as error:
            await message.answer(str(error))
            return

        form_data = await state.get_data()
        application_service = ApplicationService(application_repository)
        application = await application_service.create_application(
            ApplicationCreateDTO(
                full_name=form_data["full_name"],
                age=form_data["age"],
                city=form_data["city"],
                target_weight_loss=form_data["target_weight_loss"],
                phone=phone,
                telegram_username=message.from_user.username,
                telegram_id=message.from_user.id,
            )
        )

        logger.info(
            "Application created: id=%s telegram_id=%s",
            application.id,
            application.telegram_id,
        )

        await message.bot.send_message(
            chat_id=settings.admin_id,
            text=format_admin_application_message(application),
            reply_markup=get_admin_application_keyboard(
                application_id=application.id,
                telegram_id=application.telegram_id,
            ),
        )

        await state.clear()
        await send_typing_action(message.bot, message.chat.id)
        await message.answer(
            "Спасибо! Заявка отправлена. Скоро с вами свяжутся.",
            reply_markup=remove_keyboard(),
        )

    @router.message(ApplicationForm.phone)
    async def phone_text_fallback_handler(message: Message) -> None:
        await message.answer(
            "Нажмите кнопку ниже, чтобы отправить номер телефона.",
            reply_markup=get_contact_keyboard(),
        )

    return router
