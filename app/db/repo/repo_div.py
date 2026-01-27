# app/repositories/dividend_repo.py
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.m_div import Div

def get_by_symbol(db: Session, symbol: str) -> list[Div]:
    return db.query(Div).filter(Div.symbol == symbol).all()

def update_market_data(
    db: Session,
    rows: list[Div],
    latest_price: Decimal,
    market_cap: Decimal,
) -> int:
    updated = 0
    for row in rows:
        row.latest_price = latest_price
        row.market_cap = market_cap

        if row.dividend_rate and latest_price > 0:
            row.yield_percent = (Decimal(row.dividend_rate) / latest_price * Decimal("100"))
        else:
            row.yield_percent = None
        updated += 1
    return updated



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
