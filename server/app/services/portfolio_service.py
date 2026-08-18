from collections import defaultdict
from datetime import date, timedelta
from decimal import Decimal
from sqlalchemy.orm import Session
import yfinance as yf

from app.models.user import User
from app.models.trade import Trade, TradeAction
from app.services import stock_service


STARTING_CASH = Decimal("10000.00")


def get_portfolio(db: Session, user: User) -> dict:
    trades = db.query(Trade).filter(Trade.user_id == user.user_id).all()
    positions = _build_positions(trades)

    holdings = []
    holdings_value = Decimal("0")

    for symbol, pos in positions.items():
        if pos["quantity"] <= 0:
            continue

        quote = stock_service.get_quote(symbol)
        current_price = quote["price"]
        market_value = current_price * pos["quantity"]
        cost_basis = pos["average_cost"] * pos["quantity"]
        pnl = market_value - cost_basis
        pnl_percent = (pnl / cost_basis * 100) if cost_basis > 0 else Decimal("0")

        holdings.append({
            "symbol": symbol,
            "quantity": pos["quantity"],
            "average_cost": pos["average_cost"],
            "current_price": current_price,
            "market_value": market_value,
            "unrealised_pnl": pnl,
            "unrealised_pnl_percent": pnl_percent,
        })
        holdings_value += market_value

    total_value = user.cash_balance + holdings_value
    total_pnl = total_value - STARTING_CASH
    total_pnl_percent = (total_pnl / STARTING_CASH * 100)

    return {
        "cash_balance": user.cash_balance,
        "holdings_value": holdings_value,
        "total_value": total_value,
        "total_pnl": total_pnl,
        "total_pnl_percent": total_pnl_percent,
        "holdings": holdings,
    }


def get_history(db: Session, user: User, days: int = 30) -> dict:
    """Portfolio value per day for the last `days` days."""
    trades = (
        db.query(Trade)
        .filter(Trade.user_id == user.user_id)
        .order_by(Trade.executed_at.asc())
        .all()
    )

    if not trades:
        return {"points": []}

    end = date.today()
    start = end - timedelta(days=days)

    # Get historical closes for every symbol the user has ever held
    symbols = {t.symbol for t in trades}
    price_history = _fetch_price_history(symbols, start, end)

    points = []
    for day_offset in range(days + 1):
        d = start + timedelta(days=day_offset)
        cash, positions = _replay_to_date(trades, d)

        holdings_value = Decimal("0")
        for symbol, pos in positions.items():
            if pos["quantity"] <= 0:
                continue
            close = price_history.get(symbol, {}).get(d)
            if close is None:
                # No trading data for this day (weekend/holiday) — carry last known
                close = _last_known_close(price_history.get(symbol, {}), d)
            if close is not None:
                holdings_value += close * pos["quantity"]

        points.append({"date": d, "value": cash + holdings_value})

    return {"points": points}


def get_vs_sp500(db: Session, user: User, days: int = 30) -> dict:
    """User portfolio return % vs S&P 500 return % over the same period."""
    history = get_history(db, user, days)
    if not history["points"]:
        return {"points": []}

    start_value = history["points"][0]["value"]
    if start_value == 0:
        return {"points": []}

    start = history["points"][0]["date"]
    end = history["points"][-1]["date"]

    sp500 = _fetch_price_history({"^GSPC"}, start, end).get("^GSPC", {})
    sp500_start = _last_known_close(sp500, start) or _first_known_close(sp500)

    if sp500_start is None:
        return {"points": []}

    points = []
    for p in history["points"]:
        portfolio_pct = (p["value"] - start_value) / start_value * 100

        sp_close = sp500.get(p["date"]) or _last_known_close(sp500, p["date"])
        sp_pct = ((sp_close - sp500_start) / sp500_start * 100) if sp_close else Decimal("0")

        points.append({
            "date": p["date"],
            "portfolio_percent": portfolio_pct,
            "sp500_percent": sp_pct,
        })

    return {"points": points}


# ---------- helpers ----------

def _build_positions(trades: list[Trade]) -> dict:
    """Fold trades into current positions with weighted-average cost."""
    positions = defaultdict(lambda: {"quantity": Decimal("0"), "average_cost": Decimal("0")})

    for t in trades:
        pos = positions[t.symbol]
        if t.action == TradeAction.BUY:
            new_qty = pos["quantity"] + t.quantity
            total_cost = (pos["average_cost"] * pos["quantity"]) + (t.price * t.quantity)
            pos["average_cost"] = total_cost / new_qty if new_qty > 0 else Decimal("0")
            pos["quantity"] = new_qty
        else:  # SELL
            pos["quantity"] -= t.quantity
            # average_cost unchanged on sells

    return positions


def _replay_to_date(trades: list[Trade], up_to: date) -> tuple[Decimal, dict]:
    """Return (cash, positions) as they stood at end of `up_to`."""
    cash = STARTING_CASH
    filtered = [t for t in trades if t.executed_at.date() <= up_to]

    for t in filtered:
        if t.action == TradeAction.BUY:
            cash -= t.price * t.quantity
        else:
            cash += t.price * t.quantity

    positions = _build_positions(filtered)
    return cash, positions


def _fetch_price_history(symbols: set[str], start: date, end: date) -> dict:
    """Return {symbol: {date: close}} for a set of symbols."""
    result = {}
    for symbol in symbols:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(start=start.isoformat(), end=(end + timedelta(days=1)).isoformat())
        result[symbol] = {
            idx.date(): Decimal(str(row["Close"]))
            for idx, row in hist.iterrows()
        }
    return result


def _last_known_close(prices: dict, on_date: date) -> Decimal | None:
    """Walk backwards from on_date to find the most recent close."""
    for offset in range(7):
        d = on_date - timedelta(days=offset)
        if d in prices:
            return prices[d]
    return None


def _first_known_close(prices: dict) -> Decimal | None:
    if not prices:
        return None
    return prices[min(prices.keys())]