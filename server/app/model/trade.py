from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, func, Enum
from app.database import Base
import enum

# how u make an enum
# inherits so value is string
# enum.Enum = 
class TradeAction(str, enum.Enum):
    BUY = "BUY"
    SELL = "SELL"

class Trade(Base):
    __tablename__ = "trades"
    trade_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False, index=True)
    symbol = Column(String, nullable=False,index=True)
    action= Column(Enum(TradeAction), nullable=False)
    quantity = Column(Numeric(12,2), nullable=False)
    price = Column(Numeric(12,4), nullable=False)
    executed_at = Column(DateTime, server_default=func.now(), index=True)