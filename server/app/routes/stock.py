from fastapi import APIRouter, Query

from app.schema.stock import StockQuote, StockHistory
from app.services import stock_service


router = APIRouter(prefix="/stock", tags=["stock"])


@router.get("/quote/{symbol}", response_model=StockQuote)
def get_quote(symbol: str):
    return stock_service.get_quote(symbol)


@router.get("/history/{symbol}", response_model=StockHistory)
def get_history(
    symbol: str,
    period: str = Query("1mo", pattern="^(1d|5d|1mo|3mo|6mo|1y|2y|5y|10y|ytd|max)$"),
):
    return stock_service.get_history(symbol, period)