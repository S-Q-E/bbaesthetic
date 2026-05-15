from __future__ import annotations

from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Application


class ApplicationRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(
        self,
        *,
        full_name: str,
        age: int,
        city: str,
        target_weight_loss: int,
        phone: str,
        telegram_username: str | None,
        telegram_id: int,
    ) -> Application:
        application = Application(
            full_name=full_name,
            age=age,
            city=city,
            target_weight_loss=target_weight_loss,
            phone=phone,
            telegram_username=telegram_username,
            telegram_id=telegram_id,
        )
        self.session.add(application)
        await self.session.flush()
        await self.session.refresh(application)
        return application

    async def get_all(self) -> Sequence[Application]:
        result = await self.session.scalars(
            select(Application).order_by(Application.created_at.desc())
        )
        return result.all()
