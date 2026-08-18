from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schema.trade import TradeCreate, TradeRead
from app.services import trade_service


router = APIRouter(prefix="/trade", tags=["trade"])


@router.post("/buy", response_model=TradeRead)
def buy(
    trade_in: TradeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return trade_service.buy(db, current_user, trade_in.symbol, trade_in.quantity)


@router.post("/sell", response_model=TradeRead)
def sell(
    trade_in: TradeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return trade_service.sell(db, current_user, trade_in.symbol, trade_in.quantity)


@router.get("/history", response_model=list[TradeRead])
def history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return trade_service.get_history(db, current_user.user_id)