from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv

# load vars from .env
load_dotenv()

# engine = sqlalchemys connection to database
engine = create_engine(os.getenv("DATABASE_URL"))

# temp workspace factory to make session
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# base class/model that all inherits from
# how you define a table
Base = declarative_base()

# this funct opens a session and gives to controller
# then closes when done
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
