# app/repositories/dividend_repo.py
from decimal import Decimal
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.m_div import Div


class DivRepository:

    @staticmethod
    async def list_divs(
        db: AsyncSession,
    ) -> list[Div]:
        result = await db.execute(select(Div))
        return result.scalars().all()   # type: ignore[return-value]
