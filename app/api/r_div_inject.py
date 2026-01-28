# app/api/routes/wage.py
from fastapi import APIRouter, Depends, HTTPException, Path, UploadFile, File, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db_async import get_db

from app.service.ser_dividend_finnhub import refresh_finnhub_market_data
from app.service.ser_dividend_grab_nasdaq import grab_dividends_to_csv
from app.service.ser_dividend_load import DividendCsvLoader


injRou = APIRouter()


@injRou.post("/grab2csv")
def grab_dividends(date: str = Query(..., example="2026-01-30")):
    csv_path = grab_dividends_to_csv(target_date=date)
    return {
        "status": "grab done",
        "csv": str(csv_path),
    }


@injRou.post("/load2pg")
async def load_dividends(
    filename: str = Query(..., example="dividends_2026-01-30.csv"),
    db: AsyncSession = Depends(get_db),
):
    count = await DividendCsvLoader.load_csv(db, filename)

    return {
        "status": "load to pg done",
        "file": filename,
        "inserted": count,
    }


@injRou.post("/grab-finnhub/{symbol}")
def grab_finnhub(symbol: str):
    try:
        return refresh_finnhub_market_data(symbol)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=502, detail=str(e))
