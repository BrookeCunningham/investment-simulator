from datetime import date
from decimal import Decimal
from pydantic import BaseModel


class Holding(BaseModel):
    symbol: str
    quantity: Decimal
    average_cost: Decimal
    current_price: Decimal
    market_value: Decimal
    unrealised_pnl: Decimal
    unrealised_pnl_percent: Decimal


class PortfolioView(BaseModel):
    cash_balance: Decimal
    holdings_value: Decimal
    total_value: Decimal
    total_pnl: Decimal
    total_pnl_percent: Decimal
    holdings: list[Holding]


class PortfolioHistoryPoint(BaseModel):
    date: date
    value: Decimal


class PortfolioHistory(BaseModel):
    points: list[PortfolioHistoryPoint]


class BenchmarkPoint(BaseModel):
    date: date
    portfolio_percent: Decimal
    sp500_percent: Decimal


class PortfolioVsSp500(BaseModel):
    points: list[BenchmarkPoint]