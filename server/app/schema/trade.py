from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field

from app.models.trade import TradeAction


class TradeCreate(BaseModel):
    symbol: str = Field(min_length=1, max_length=10)
    quantity: Decimal = Field(gt=0, max_digits=12, decimal_places=4)


class TradeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    trade_id: int
    symbol: str
    action: TradeAction
    quantity: Decimal
    price: Decimal
    executed_at: datetime