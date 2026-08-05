from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, func, Enum, Index
from sqlalchemy.orm import relationship
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

    trade_id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer,
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False,
    )
    symbol = Column(String(10), nullable=False, index=True)
    action = Column(Enum(TradeAction, name="tradeaction"), nullable=False)
    quantity = Column(Numeric(precision=12, scale=4), nullable=False)
    price = Column(Numeric(precision=12, scale=4), nullable=False)
    executed_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    user = relationship("User", back_populates="trades")

    __table_args__ = (
        Index("ix_trades_user_id_executed_at", "user_id", "executed_at"),
    )