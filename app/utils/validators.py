from __future__ import annotations

import re


def validate_text_value(
    value: str,
    *,
    field_name: str,
    min_length: int = 2,
    max_length: int = 100,
) -> str:
    normalized = " ".join(value.split()).strip()
    if not normalized:
        raise ValueError(f"Укажите {field_name.lower()}.")
    if len(normalized) < min_length:
        raise ValueError(f"{field_name} слишком короткое.")
    if len(normalized) > max_length:
        raise ValueError(f"{field_name} слишком длинное.")
    return normalized


def validate_name(value: str) -> str:
    normalized = validate_text_value(value, field_name="Имя", max_length=80)
    if not re.fullmatch(r"[A-Za-zА-Яа-яЁёІіҢңҒғҮүҰұҚқӨөҺһӘә\s\-]+", normalized):
        raise ValueError("Введите имя без цифр и лишних символов.")
    return normalized


def validate_age(value: str) -> int:
    normalized = value.strip()
    if not normalized.isdigit():
        raise ValueError("Возраст нужно указать цифрами.")

    age = int(normalized)
    if age < 14 or age > 100:
        raise ValueError("Введите возраст от 14 до 100 лет.")
    return age


def validate_target_weight_loss(value: str) -> int:
    normalized = (
        value.lower()
        .replace("кг", "")
        .replace("килограмм", "")
        .replace(" ", "")
        .strip()
    )
    if not normalized:
        raise ValueError("Укажите, сколько кг хотите сбросить.")

    if normalized.startswith("+"):
        normalized = normalized[1:]

    if normalized.startswith("-"):
        normalized = normalized[1:]

    if not normalized.isdigit():
        raise ValueError("Цель похудения нужно указать цифрами.")

    target = int(normalized)
    if target < 1 or target > 200:
        raise ValueError("Введите значение от 1 до 200 кг.")
    return target


def normalize_phone(phone: str) -> str:
    digits = re.sub(r"\D", "", phone)
    if not digits:
        raise ValueError("Некорректный номер телефона.")
    return f"+{digits}"
