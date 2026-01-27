# app/api/routes/wage.py
import requests

from fastapi import APIRouter, Depends, Path, UploadFile, File, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.db_async import get_db

from app.service.ser_dividend_grab_nasdaq import grab_dividends_to_csv
from app.service.ser_dividend_load import DividendCsvLoader

from app.config import get_settings_singleton
settings = get_settings_singleton()
ALPHA_API_KEY = settings.ALPHAVANTAGE_API_KEY
EOD_API_KEY = settings.EOD_API_KEY
FINNHUB_API_KEY = settings.FINNHUB_API_KEY


reserveRou = APIRouter()

@reserveRou.post("/grab")
def grab_dividends(date: str = Query(..., examples="2026-01-30")):
    csv_path = grab_dividends_to_csv(target_date=date)

    return {
        "status": "ok",
        "csv": str(csv_path),
    }


@reserveRou.post("/load")
async def load_dividends(
    filename: str = Query(..., examples="dividends_2026-01-30.csv"),
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
    
    



@reserveRou.get("/alpha_stock/{symbol}")
def get_alpha_stock(symbol: str):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={ALPHA_API_KEY}"
    response = requests.get(url)
    return response.json()


@reserveRou.get("/eod_stock/{symbol}")
def get_eod_stock(symbol: str):
    url = f"https://eodhistoricaldata.com/api/eod/{symbol}.US?api_token={EOD_API_KEY}&fmt=json"
    response = requests.get(url)
    return response.json()


@reserveRou.get("/finnhub_quote/{symbol}")
def get_finnhub_quote(symbol: str):
    url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={FINNHUB_API_KEY}"
    response = requests.get(url)
    return response.json()



@reserveRou.get("/alpha_stock2/{symbol}")
def get_alpha_stock2(symbol: str):
    price_url = (
        "https://www.alphavantage.co/query"
        f"?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={ALPHA_API_KEY}"
    )
    overview_url = (
        "https://www.alphavantage.co/query"
        f"?function=OVERVIEW&symbol={symbol}&apikey={ALPHA_API_KEY}"
    )

    price_res = requests.get(price_url).json()
    overview_res = requests.get(overview_url).json()

    ts = price_res.get("Time Series (Daily)", {})
    latest_date = max(ts.keys()) if ts else None
    latest_price = ts[latest_date]["4. close"] if latest_date else None

    return {
        "provider": "alpha_vantage",
        "symbol": symbol,
        "latest_price": float(latest_price) if latest_price else None,
        "market_cap": int(overview_res.get("MarketCapitalization", 0)) or None
    }



def safe_get_json(url: str):
    res = requests.get(url, timeout=10)
    if res.status_code != 200 or not res.text.strip():
        return None
    try:
        return res.json()
    except ValueError:
        return None


@reserveRou.get("/eod_stock2/{symbol}")
def get_eod_stock2(symbol: str):
    eod_url = (
        f"https://eodhistoricaldata.com/api/eod/{symbol}.US"
        f"?api_token={EOD_API_KEY}&fmt=json"
    )

    fundamentals_url = (
        f"https://eodhistoricaldata.com/api/fundamentals/{symbol}.US"
        f"?api_token={EOD_API_KEY}"
    )

    eod_data = safe_get_json(eod_url) or []
    fundamentals = safe_get_json(fundamentals_url) or {}

    latest_price = eod_data[-1]["close"] if eod_data else None
    market_cap = fundamentals.get("General", {}).get("MarketCapitalization")

    return {
        "provider": "eod",
        "symbol": symbol,
        "latest_price": latest_price,
        "market_cap": market_cap
    }


@reserveRou.get("/finnhub_stock2/{symbol}")
def get_finnhub_stock2(symbol: str):
    quote_url = (
        f"https://finnhub.io/api/v1/quote"
        f"?symbol={symbol}&token={FINNHUB_API_KEY}"
    )
    profile_url = (
        f"https://finnhub.io/api/v1/stock/profile2"
        f"?symbol={symbol}&token={FINNHUB_API_KEY}"
    )

    quote = requests.get(quote_url).json()
    profile = requests.get(profile_url).json()

    return {
        "provider": "finnhub",
        "symbol": symbol,
        "latest_price": quote.get("c"),
        "market_cap": profile.get("marketCapitalization")
    }
