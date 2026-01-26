# app/service/ser_dividend_load.py
import csv
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.m_div import Div  # your ORM model

DATE_FMT = "%m/%d/%Y"  # Nasdaq CSV date format


class DividendCsvLoader:

    @staticmethod
    async def load_csv(db: AsyncSession, filename: str) -> int:
        """
        Read a CSV (normalized) and insert into DB.

        Returns:
            Number of rows inserted
        """
        inserted = 0
        file_path = f"data/dividends/{filename}"

        with open(file_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                dividend = Div(
                    company_name=row["companyName"],
                    symbol=row["symbol"],
                    dividend_ex_date=datetime.strptime(row["dividend_Ex_Date"], DATE_FMT).date(),
                    payment_date=datetime.strptime(row["payment_Date"], DATE_FMT).date(),
                    record_date=datetime.strptime(row["record_Date"], DATE_FMT).date(),
                    dividend_rate=float(row["dividend_Rate"]),
                    indicated_annual_dividend=float(row["indicated_Annual_Dividend"]),
                    announcement_date=datetime.strptime(row["announcement_Date"], DATE_FMT).date(),
                )

                db.add(dividend)
                inserted += 1

        await db.commit()
        return inserted
