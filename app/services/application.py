from __future__ import annotations

from app.database.models import Application
from app.database.repositories import ApplicationRepository
from app.services.dto import ApplicationCreateDTO


class ApplicationService:
    def __init__(self, repository: ApplicationRepository) -> None:
        self.repository = repository

    async def create_application(self, data: ApplicationCreateDTO) -> Application:
        return await self.repository.create(
            full_name=data.full_name,
            age=data.age,
            city=data.city,
            target_weight_loss=data.target_weight_loss,
            phone=data.phone,
            telegram_username=data.telegram_username,
            telegram_id=data.telegram_id,
        )
