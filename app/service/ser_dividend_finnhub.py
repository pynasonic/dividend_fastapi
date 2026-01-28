# app/services/dividend_service.py
from decimal import Decimal
from app.db.db_sync import get_db_sync_contextmanager
from app.providers.finnhub_client import FinnhubClient
from app.db.repo.repo_div_inject import get_by_symbol, update_market_data

def refresh_finnhub_market_data(symbol: str) -> dict:
    client = FinnhubClient()
    data = client.get_quote_and_profile(symbol)

    if data["latest_price"] is None or data["market_cap"] is None:
        raise ValueError("Incomplete data from Finnhub")

    latest_price = Decimal(str(data["latest_price"]))
    market_cap = Decimal(str(data["market_cap"]))

    # Service handles DB session internally
    with get_db_sync_contextmanager() as db:
        rows = get_by_symbol(db, symbol)
        if not rows:
            raise LookupError(f"No dividend rows for symbol {symbol}")
        updated = update_market_data(db, rows, latest_price, market_cap)
        db.commit()

    return {
        "symbol": symbol,
        "latest_price": latest_price,
        "market_cap": market_cap,
        "rows_updated": updated,
    }
