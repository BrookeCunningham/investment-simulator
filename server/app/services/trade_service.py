from decimal import Decimal
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User
from app.models.trade import Trade, TradeAction
from app.services import stock_service


def buy(db: Session, user: User, symbol: str, quantity: Decimal) -> Trade:
    symbol = symbol.upper()

    quote = stock_service.get_quote(symbol)
    price = quote["price"]
    cost = price * quantity

    if cost > user.cash_balance:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient funds. Cost: £{cost:.2f}, Balance: £{user.cash_balance:.2f}",
        )

    trade = Trade(
        user_id=user.user_id,
        symbol=symbol,
        action=TradeAction.BUY,
        quantity=quantity,
        price=price,
    )
    user.cash_balance -= cost

    db.add(trade)
    db.commit()
    db.refresh(trade)
    return trade


def sell(db: Session, user: User, symbol: str, quantity: Decimal) -> Trade:
    symbol = symbol.upper()

    held = _get_holding(db, user.user_id, symbol)
    if quantity > held:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient holdings. Trying to sell {quantity}, own {held}",
        )

    quote = stock_service.get_quote(symbol)
    price = quote["price"]
    proceeds = price * quantity

    trade = Trade(
        user_id=user.user_id,
        symbol=symbol,
        action=TradeAction.SELL,
        quantity=quantity,
        price=price,
    )
    user.cash_balance += proceeds

    db.add(trade)
    db.commit()
    db.refresh(trade)
    return trade


def get_history(db: Session, user_id: int) -> list[Trade]:
    return (
        db.query(Trade)
        .filter(Trade.user_id == user_id)
        .order_by(Trade.executed_at.desc())
        .all()
    )


def _get_holding(db: Session, user_id: int, symbol: str) -> Decimal:
    """Sum of buys minus sells for a given symbol."""
    trades = (
        db.query(Trade)
        .filter(Trade.user_id == user_id, Trade.symbol == symbol)
        .all()
    )
    total = Decimal("0")
    for t in trades:
        if t.action == TradeAction.BUY:
            total += t.quantity
        else:
            total -= t.quantity
    return total