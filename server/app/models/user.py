from sqlalchemy import Column, Integer, String, Numeric, DateTime, func
from app.database import Base
from sqlalchemy.orm import relationship

# inherits from base
class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    first_name = Column(String(100), nullable=False)
    surname = Column(String(100), nullable=False)
    password_hash = Column(String(255), nullable=False)
    cash_balance = Column(Numeric(precision=12, scale=2), nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    trades = relationship(
        "Trade",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    

