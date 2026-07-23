from sqlalchemy import Column, Integer, String, Numeric, DateTime, func
from app.database import Base

# inherits from base
class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    first_name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    password = Column(String,nullable=False)
    cash_balance = Column(Numeric(12,2), nullable=False, default=10000)
    created_at = Column(DateTime, server_default=func.now())
    

