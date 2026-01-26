# app/repositories/dividend_repo.py
from decimal import Decimal
from sqlalchemy.orm import Session
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


# # app/repositories/dividend_repo.py
# from decimal import Decimal

# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy import select

# from app.db.models.m_div import Div


# async def get_by_symbol(db: AsyncSession, symbol: str) -> list[Div]:
#     return db.query(Div).filter(Div.symbol == symbol).all()


# async def update_market_data(
#     db: AsyncSession,
#     rows: list[Div],
#     latest_price: Decimal,
#     market_cap: Decimal,
# ) -> int:
#     updated = 0

#     for row in rows:
#         row.latest_price = latest_price
#         row.market_cap = market_cap

#         if row.dividend_rate and latest_price > 0:
#             row.yield_percent = (
#                 Decimal(row.dividend_rate) / latest_price * Decimal("100")
#             )
#         else:
#             row.yield_percent = None

#         updated += 1

#     return updated

