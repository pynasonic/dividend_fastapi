# app/repositories/wage_repository.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models.m_wage import CanadaWage

class WageRepository:

    @staticmethod
    async def bulk_insert(
        db: AsyncSession,
        wages: list[CanadaWage],
    ) -> None:
        db.add_all(wages)
        await db.commit()


    @staticmethod
    async def list_wages(
        db: AsyncSession,
    ) -> list[CanadaWage]:
        stmt = select(CanadaWage).limit(10)
        result = await db.execute(stmt)
        return result.scalars().all()   # type: ignore[return-value]
