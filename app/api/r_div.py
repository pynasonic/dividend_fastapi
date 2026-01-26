# app/api/routes/wage.py
import requests

from fastapi import APIRouter, Depends, Path, UploadFile, File, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.db_async import get_db

from app.service.ser_grab_dividends import grab_dividends_to_csv
from app.service.ser_dividend_load import DividendCsvLoader

from app.config import get_settings_singleton
settings = get_settings_singleton()
ALPHA_API_KEY = settings.ALPHAVANTAGE_API_KEY
EOD_API_KEY = settings.EOD_API_KEY
FINNHUB_API_KEY = settings.FINNHUB_API_KEY


divRou = APIRouter()

@divRou.post("/grab")
def grab_dividends(date: str = Query(..., example="2026-01-30")):
    csv_path = grab_dividends_to_csv(target_date=date)

    return {
        "status": "ok",
        "csv": str(csv_path),
    }


@divRou.post("/load")
async def load_dividends(
    filename: str = Query(..., example="dividends_2026-01-30.csv"),
    db: AsyncSession = Depends(get_db),
):
    count = await DividendCsvLoader.load_csv(db, filename)

    return {
        "status": "ok",
        "file": filename,
        "inserted": count,
    }
# @divRou.post("/upload")
# async def upload_reports(
#     file: UploadFile = File(...),
#     db: AsyncSession = Depends(get_db),
# ):
#     content = await file.read()
#     await WageService.upload_csv(db, content)
#     return {"status": "ok"}


# @divRou.get("/")
# async def list_reports(
#     db: AsyncSession = Depends(get_db),
# ):
#     return await WageService.list_wages(db)



# @divRou.get("/pagination")
# async def list_wages(
#     db: AsyncSession = Depends(get_db),
#     page: int = Query(1, ge=1),
#     page_size: int = Query(10, le=100),
# ):
#     return await WageService.list_paginated(
#         db=db,
#         page=page,
#         page_size=page_size,
#     )
    
    



@divRou.get("/alpha_stock/{symbol}")
def get_alpha_stock(symbol: str):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={ALPHA_API_KEY}"
    response = requests.get(url)
    return response.json()



@divRou.get("/eod_stock/{symbol}")
def get_eod_stock(symbol: str):
    url = f"https://eodhistoricaldata.com/api/eod/{symbol}.US?api_token={EOD_API_KEY}&fmt=json"
    response = requests.get(url)
    return response.json()



@divRou.get("/finnhub_quote/{symbol}")
def get_finnhub_quote(symbol: str):
    url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={FINNHUB_API_KEY}"
    response = requests.get(url)
    return response.json()


