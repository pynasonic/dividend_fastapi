from datetime import date
import uuid
from typing import Optional, Dict, Any, List, TYPE_CHECKING

from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Column, ForeignKey, Index, String, Integer, Date, Numeric

from app.db.models.m_base import Base, BaseMixin

class Div(Base, BaseMixin):
    __tablename__ = "dividends"
    __table_args__ = (Index("ix_dividends_symbol_exdate","symbol","dividend_ex_date",unique=True,),)
    
    company_name: Mapped[str] = mapped_column(String(255), nullable=True, index=True)
    symbol:       Mapped[str] = mapped_column(String(50), nullable=True, index=True)

    dividend_ex_date: Mapped[date] = mapped_column(Date,nullable=True,index=True,)
    record_date: Mapped[date] = mapped_column(Date,nullable=True,)
    payment_date: Mapped[date] = mapped_column(Date,nullable=True,)
    dividend_rate: Mapped[float] = mapped_column(Numeric(10, 4),nullable=True,)
    indicated_annual_dividend: Mapped[float] = mapped_column(Numeric(10, 4),nullable=True,)
    announcement_date: Mapped[date] = mapped_column(Date,nullable=True,)
    
    # from finnhub
    latest_price: Mapped[float] = mapped_column(Numeric(10, 4),nullable=True,)
    yield_percent: Mapped[float] = mapped_column(Numeric(5, 2),nullable=True,)
    market_cap: Mapped[float] = mapped_column(Numeric(20, 2),nullable=True,)


class DivChunk(Base, BaseMixin):
    __tablename__ = "dividend_chunks"

    div_id: Mapped[uuid.UUID] = mapped_column(nullable=True,)

    chunk_index: Mapped[int] = mapped_column(
        Integer,
        nullable=True,
    )

    content: Mapped[str] = mapped_column(
        String,
        nullable=True,
    )

    embedding: Mapped[Optional[List[float]]] = mapped_column(
        Vector(1536),
        nullable=True,
    )

    __table_args__ = (
        Index(
            "ix_dividend_chunks_div_chunk",
            "div_id",
            "chunk_index",
            unique=True,
        ),
    )