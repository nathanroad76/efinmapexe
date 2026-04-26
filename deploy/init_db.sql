-- =============================================
-- efinmap Database Schema
-- Run: psql -U postgres -f init_db.sql
--
-- !!! BEFORE RUNNING: replace CHANGE_ME_STRONG_PASSWORD below with a real
--     password, and put the SAME password into .env DATABASE_URL.
-- =============================================

-- Create database and user
CREATE DATABASE efinmap;
CREATE USER efinmap_user WITH ENCRYPTED PASSWORD 'CHANGE_ME_STRONG_PASSWORD';
GRANT ALL PRIVILEGES ON DATABASE efinmap TO efinmap_user;

\c efinmap;
GRANT ALL ON SCHEMA public TO efinmap_user;

-- =============================================
-- Tables
-- =============================================

-- Stock metadata (mostly static)
CREATE TABLE IF NOT EXISTS tickers (
    symbol      TEXT PRIMARY KEY,
    name_cn     TEXT,
    name_en     TEXT,
    market      TEXT NOT NULL,   -- 'US', 'HK', 'JP', 'KR', 'TW'
    domain      TEXT,            -- for favicon: 'nvidia.com'
    tag_type    TEXT             -- 'US', 'ETF', 'Index', 'JP', 'KR', 'TW', 'HK'
);

-- Year-end closing prices (YTD and YoY base)
CREATE TABLE IF NOT EXISTS annual_benchmarks (
    symbol  TEXT    NOT NULL,
    year    INTEGER NOT NULL,
    price   DECIMAL(20, 6) NOT NULL,
    PRIMARY KEY (symbol, year)
);

-- Price snapshots (time-series core)
CREATE TABLE IF NOT EXISTS price_snapshots (
    id          BIGSERIAL PRIMARY KEY,
    symbol      TEXT           NOT NULL,
    price       DECIMAL(20, 6),
    prev_close  DECIMAL(20, 6),
    daily_chg   DECIMAL(8, 4),
    market_cap  BIGINT,
    pe_ratio    DECIMAL(10, 2),
    snapshot_at TIMESTAMPTZ    NOT NULL DEFAULT NOW(),
    market_date DATE           NOT NULL
);

-- Fast lookup: latest snapshot per symbol
CREATE INDEX IF NOT EXISTS idx_snapshots_symbol_time
    ON price_snapshots (symbol, snapshot_at DESC);

CREATE INDEX IF NOT EXISTS idx_snapshots_date
    ON price_snapshots (market_date DESC);

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO efinmap_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO efinmap_user;
