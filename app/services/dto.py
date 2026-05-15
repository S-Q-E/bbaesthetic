from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class ApplicationCreateDTO:
    full_name: str
    age: int
    city: str
    target_weight_loss: int
    phone: str
    telegram_username: str | None
    telegram_id: int
