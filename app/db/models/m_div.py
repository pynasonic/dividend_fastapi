from datetime import date

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Date, Numeric

from app.db.models.m_base import Base, BaseMixin

class Div(Base, BaseMixin):
    __tablename__ = "dividends"
    
    company_name: Mapped[str] = mapped_column(String(255), nullable=True, index=True)
    symbol:       Mapped[str] = mapped_column(String(50), nullable=True, index=True)

    dividend_ex_date: Mapped[date] = mapped_column(Date,nullable=False,index=True,)
    record_date: Mapped[date] = mapped_column(Date,nullable=False,)
    payment_date: Mapped[date] = mapped_column(Date,nullable=False,)
    dividend_rate: Mapped[float] = mapped_column(Numeric(10, 4),nullable=False,)
    indicated_annual_dividend: Mapped[float] = mapped_column(Numeric(10, 4),nullable=False,)
    announcement_date: Mapped[date] = mapped_column(Date,nullable=False,)

    