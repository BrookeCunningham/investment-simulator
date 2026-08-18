# Papertrak — Backend

Paper trading simulator. Virtual £10,000 starting balance, buy and sell real stocks at real prices, track P&L, benchmark against the S&P 500.

## Stack

- Python, FastAPI, SQLAlchemy
- PostgreSQL, Alembic
- JWT auth (bcrypt password hashing)
- yfinance for market data

## Folder structure

```
server/
├── alembic/
├── app/
│   ├── core/          # config, security (JWT + password hashing)
│   ├── models/        # SQLAlchemy models
│   ├── routes/        # FastAPI routers
│   ├── schema/        # Pydantic request/response schemas
│   ├── services/      # business logic
│   ├── database.py
│   └── main.py
└── requirements.txt
```

## Setup

Requires Python 3.13+ and PostgreSQL 17.

1. Create and activate a virtual environment:
```
   python -m venv venv
   .\venv\Scripts\activate      # Windows
   source venv/bin/activate      # macOS/Linux
```

2. Install dependencies:
```
   pip install -r requirements.txt
```

3. Create a Postgres database called `papertrak`.

4. Copy `.env.example` to `.env` and fill in real values. Generate a JWT secret with:
```
   python -c "import secrets; print(secrets.token_urlsafe(32))"
```

5. Run migrations:
```
   alembic upgrade head
```

6. Start the server:
```
   uvicorn app.main:app --reload
```

API docs: http://localhost:8000/docs

## Endpoints

Auth
- `POST /auth/register` — create account, £10,000 starting balance
- `POST /auth/login` — returns JWT
- `GET  /auth/me` — current user

Stock
- `GET /stock/quote/{symbol}` — live price
- `GET /stock/history/{symbol}?period=1mo` — historical closes

Trade (requires auth)
- `POST /trade/buy` — `{ symbol, quantity }`
- `POST /trade/sell` — `{ symbol, quantity }`
- `GET  /trade/history`

Portfolio (requires auth)
- `GET /portfolio/view` — current holdings, cash, total value, P&L
- `GET /portfolio/history?days=30` — total value per day
- `GET /portfolio/vs-sp500?days=30` — return % vs S&P 500

## Design notes

- Holdings are derived from the trades table rather than stored — no sync bugs, matches how Investopedia's simulator works.
- Average cost basis on holdings is weighted across all buys.
- `Numeric` (Decimal) throughout for money — no floats.
- All trade operations run in a single DB transaction — cash balance and trade record commit together or roll back together.
- yfinance is called on demand. `PriceCache` table exists in the schema but is not yet used; will cache quotes and daily closes when performance requires it.