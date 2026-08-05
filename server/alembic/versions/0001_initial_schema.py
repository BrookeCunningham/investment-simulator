"""initial schema

Revision ID: 0001_initial_schema
Revises: 
Create Date: 2026-08-05 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0001_initial_schema'
down_revision = None
branch_labels = None
depend_on = None


def upgrade() -> None:
    # create enum type tradeaction
    # create enum type for trade action
    op.execute("DROP TYPE IF EXISTS tradeaction")
    # attempt to create the enum type; ignore if it already exists due to race
    conn = op.get_bind()
    try:
        conn.execute(sa.text("CREATE TYPE tradeaction AS ENUM ('BUY', 'SELL')"))
    except Exception:
        pass

    # create users table
    op.create_table(
        'users',
        sa.Column('user_id', sa.Integer(), primary_key=True),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('first_name', sa.String(length=100), nullable=False),
        sa.Column('surname', sa.String(length=100), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('cash_balance', sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )
    op.create_index('ix_users_email', 'users', ['email'], unique=True)

    # create price_cache table
    op.create_table(
        'price_cache',
        sa.Column('symbol', sa.String(length=10), primary_key=True),
        sa.Column('date', sa.Date(), primary_key=True),
        sa.Column('close', sa.Numeric(precision=12, scale=4), nullable=False),
    )

    # create trades table
    op.create_table(
        'trades',
        sa.Column('trade_id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False),
        sa.Column('symbol', sa.String(length=10), nullable=False),
        sa.Column('action', postgresql.ENUM('BUY', 'SELL', name='tradeaction', create_type=False), nullable=False),
        sa.Column('quantity', sa.Numeric(precision=12, scale=4), nullable=False),
        sa.Column('price', sa.Numeric(precision=12, scale=4), nullable=False),
        sa.Column('executed_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )
    op.create_index('ix_trades_symbol', 'trades', ['symbol'])
    op.create_index('ix_trades_user_id_executed_at', 'trades', ['user_id', 'executed_at'])


def downgrade() -> None:
    # drop indexes and tables in reverse order
    op.drop_index('ix_trades_user_id_executed_at', table_name='trades')
    op.drop_index('ix_trades_symbol', table_name='trades')
    op.drop_table('trades')

    op.drop_table('price_cache')

    op.drop_index('ix_users_email', table_name='users')
    op.drop_table('users')

    # drop enum type
    tradeaction = postgresql.ENUM('BUY', 'SELL', name='tradeaction')
    tradeaction.drop(op.get_bind(), checkfirst=True)
