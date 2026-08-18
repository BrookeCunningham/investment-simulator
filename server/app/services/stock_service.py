from datetime import datetime, timezone
from decimal import Decimal
import yfinance as yf

from fastapi import HTTPException, status


def get_quote(symbol: str) -> dict:
    ticker = yf.Ticker(symbol)
    # fast_info is quicker than .info and less prone to breaking
    try:
        price = ticker.fast_info["last_price"]
    except (KeyError, Exception):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Symbol '{symbol}' not found",
        )

    if price is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Symbol '{symbol}' not found",
        )

    return {
        "symbol": symbol.upper(),
        "price": Decimal(str(price)),
        "timestamp": datetime.now(timezone.utc),
    }


def get_history(symbol: str, period: str = "1mo") -> dict:
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period=period)

    if hist.empty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No history for symbol '{symbol}'",
        )

    points = [
        {"date": idx.date(), "close": Decimal(str(row["Close"]))}
        for idx, row in hist.iterrows()
    ]

    return {"symbol": symbol.upper(), "points": points}