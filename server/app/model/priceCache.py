from sqlalchemy import Column,String,Numeric,Date
from app.database import Base

class PriceCache(Base):
    __tablename__ = "price_cache"
    symbol = Column(String, primary_key=True)
    date = Column(Date, primary_key=True)
    close = Column(Numeric(12,2), nullable=False)