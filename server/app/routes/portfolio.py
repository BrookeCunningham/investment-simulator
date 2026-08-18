from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schema.portfolio import PortfolioView, PortfolioHistory, PortfolioVsSp500
from app.services import portfolio_service


router = APIRouter(prefix="/portfolio", tags=["portfolio"])


@router.get("/view", response_model=PortfolioView)
def view(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return portfolio_service.get_portfolio(db, current_user)


@router.get("/history", response_model=PortfolioHistory)
def history(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return portfolio_service.get_history(db, current_user, days)


@router.get("/vs-sp500", response_model=PortfolioVsSp500)
def vs_sp500(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return portfolio_service.get_vs_sp500(db, current_user, days)