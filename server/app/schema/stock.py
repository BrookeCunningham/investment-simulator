from datetime import date, datetime
from decimal import Decimal
from pydantic import BaseModel


class StockQuote(BaseModel):
    symbol: str
    price: Decimal
    timestamp: datetime


class StockHistoryPoint(BaseModel):
    date: date
    close: Decimal


class StockHistory(BaseModel):
    symbol: str
    points: list[StockHistoryPoint]