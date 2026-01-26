# app/repositories/report_repository.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models.m_div import Report

class ReportRepository:

    @staticmethod
    async def bulk_insert(
        db: AsyncSession,
        reports: list[Report],
    ) -> None:
        db.add_all(reports)
        await db.commit()

    @staticmethod
    async def list_reports(
        db: AsyncSession,
    ) -> list[Report]:
        result = await db.execute(select(Report))
        return result.scalars().all()   # type: ignore[return-value]
