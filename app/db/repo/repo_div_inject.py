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

        if row.indicated_annual_dividend and latest_price > 0:
            row.yield_percent = (Decimal(row.indicated_annual_dividend) / latest_price * Decimal("100"))
        else:
            row.yield_percent = None
        updated += 1
    return updated



def get_all(db: Session) -> list[Div]:
    return db.query(Div).all()