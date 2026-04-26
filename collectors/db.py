"""Database write helpers for collectors."""
import os
import psycopg
from datetime import date, datetime
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://efinmap_user:yourpassword@localhost:5432/efinmap")


def get_connection():
    return psycopg.connect(DATABASE_URL)


def insert_ticker_if_missing(cur, symbol: str, name_cn: str, name_en: str,
                             market: str, domain: str, tag_type: str):
    """
    Insert ticker only if it doesn't already exist. Preserves curated metadata
    (especially Chinese names) seeded by deploy/seed_data.py — collectors must
    not overwrite those with yfinance's English shortNames every cron run.

    To intentionally change ticker metadata, edit seed_data.py and re-run it
    (it uses ON CONFLICT DO UPDATE, so a re-seed is the explicit refresh path).
    """
    cur.execute("""
        INSERT INTO tickers (symbol, name_cn, name_en, market, domain, tag_type)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (symbol) DO NOTHING
    """, (symbol, name_cn, name_en, market, domain, tag_type))


def save_snapshot(cur, symbol: str, price: float, prev_close: float,
                  daily_chg: float, market_cap: int, pe_ratio: float | None):
    cur.execute("""
        INSERT INTO price_snapshots
            (symbol, price, prev_close, daily_chg, market_cap, pe_ratio, market_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (symbol, price, prev_close, daily_chg,
          int(market_cap) if market_cap else None,
          pe_ratio if pe_ratio and pe_ratio > 0 else None,
          date.today()))
