# app/service/ser_dividend_grab.py
import requests
import pandas as pd
from pathlib import Path

NASDAQ_URL = "https://api.nasdaq.com/api/calendar/dividends"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Origin": "https://www.nasdaq.com",
    "Referer": "https://www.nasdaq.com/",
}

# Hardcoded CSV folder
CSV_FOLDER = Path("data/dividends")

# Expected columns for validation
EXPECTED_COLUMNS = {
    "companyName",
    "symbol",
    "dividend_Ex_Date",
    "payment_Date",
    "record_Date",
    "dividend_Rate",
    "indicated_Annual_Dividend",
    "announcement_Date",
}


def grab_dividends_to_csv(target_date: str) -> Path:
    # Ensure folder exists
    CSV_FOLDER.mkdir(parents=True, exist_ok=True)

    # Fetch data from Nasdaq
    r = requests.get(
        NASDAQ_URL,
        params={"date": target_date},
        headers=HEADERS,
        timeout=30,
    )
    r.raise_for_status()

    rows = r.json()["data"]["calendar"]["rows"]
    df = pd.DataFrame(rows)

    # Validate CSV columns
    missing = EXPECTED_COLUMNS - set(df.columns)
    if missing:
        raise RuntimeError(f"Missing columns from Nasdaq payload: {missing}")

    # Save CSV
    csv_path = CSV_FOLDER / f"dividends_{target_date}.csv"
    df.to_csv(csv_path, index=False)

    return csv_path
