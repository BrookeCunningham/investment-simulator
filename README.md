# Investment Simulator
Paper trading simulator. Virtual £10,000, buy and sell real stocks at real prices, track P&L, compare against the S&P 500.

## Stack
- **Frontend** — React, TypeScript, Vite, MUI, Recharts
- **Backend** — Python, FastAPI, SQLAlchemy
- **Database** — PostgreSQL
- **Auth** — JWT
- **Stock data** — yfinance

## Folder structure

```
papertrak/
├── client/
│   └── src/
│       ├── api/
│       ├── components/
│       ├── contexts/
│       └── pages/
└── server/
    ├── alembic/
    └── app/
        ├── main.py
        ├── database.py
        ├── models/
        ├── schemas/
        ├── routers/
        └── services/

```

## Models
**User** — userId, email, firstName, surname, password, cashBalance, createdAt

**Trade** — tradeId, userId, symbol, action (BUY/SELL), quantity, price, executedAt

**PriceCache** — symbol, date, close


## Endpoints
```
POST /auth/register
POST /auth/login

GET  /portfolio/view
GET  /portfolio/history
GET  /portfolio/vs-sp500

POST /trade/buy
POST /trade/sell
GET  /trade/history

GET  /stock/quote/{symbol}
GET  /stock/history/{symbol}
```

https://www.geeksforgeeks.org/postgresql/install-postgresql-on-windows/
prisma = sqlalchemy
express = flask/fastapi/django
postgresql = same