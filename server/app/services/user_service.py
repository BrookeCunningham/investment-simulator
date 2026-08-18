from decimal import Decimal
from sqlalchemy.orm import Session

from app.models.user import User
from app.schema.user import UserCreate


STARTING_CASH = Decimal("10000.00")


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.user_id == user_id).first()


def create_user(db: Session, user_in: UserCreate, password_hash: str) -> User:
    user = User(
        email=user_in.email,
        first_name=user_in.first_name,
        surname=user_in.surname,
        password_hash=password_hash,
        cash_balance=STARTING_CASH,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user