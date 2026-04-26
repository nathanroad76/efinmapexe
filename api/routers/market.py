"""Market data API routes."""
from datetime import datetime, time, date
from typing import Any
import pytz
import re
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel

from api.database import get_db
from api.market_config import US_GROUPS, HK_GROUPS, ASIA_GROUPS

# Optional yfinance for on-demand fetching
try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False

router = APIRouter(prefix="/market", tags=["market"])

CURRENT_YEAR = 2026   # YTD base = end of previous year (2025)
BENCHMARK_YEAR = 2025  # The year whose year-end price is our YTD base


# ===== On-demand ticker fetching =====

def detect_market(symbol: str) -> tuple[str, str]:
    """
    Detect market type and clean symbol from user input.
    Returns (market, clean_symbol).
    """
    s = symbol.upper().strip()

    # HK: ends with .HK
    if s.endswith('.HK'):
        return 'HK', s

    # Japan: ends with .T
    if s.endswith('.T'):
        return 'JP', s

    # Korea: ends with .KS or .KQ
    if s.endswith('.KS') or s.endswith('.KQ'):
        return 'KR', s

    # Taiwan: ends with .TW or .TWO
    if s.endswith('.TW') or s.endswith('.TWO'):
        return 'TW', s

    # China A-shares (Shanghai/Shenzhen): ends with .SS or .SZ
    if s.endswith('.SS') or s.endswith('.SZ'):
        return 'CN', s

    # Singapore: ends with .SI
    if s.endswith('.SI'):
        return 'SG', s

    # Australia: ends with .AX
    if s.endswith('.AX'):
        return 'AU', s

    # Canada: ends with .TO or .V
    if s.endswith('.TO') or s.endswith('.V'):
        return 'CA', s

    # UK/Europe: .L, .PA, .DE, etc. - treat as generic
    if any(s.endswith('.' + x) for x in ['L', 'PA', 'DE', 'AS', 'BR', 'MI', 'SW', 'ST', 'OL', 'CO', 'HE', 'IR']):
        return 'EU', s

    # Default: US
    return 'US', s


def get_yahoo_ticker(symbol: str, market: str) -> str:
    """
    Convert our symbol format to Yahoo Finance format if needed.
    """
    # Most symbols are the same, but some markets need adjustment
    if market == 'CN':
        # .SS -> .SS, .SZ -> .SZ (same)
        return symbol
    return symbol


def fetch_ticker_from_yahoo(symbol: str) -> dict | None:
    """
    Fetch ticker info and latest price from Yahoo Finance.
    Returns dict with ticker metadata and price data, or None if failed.
    """
    if not YFINANCE_AVAILABLE:
        return None

    try:
        market, clean_symbol = detect_market(symbol)
        yahoo_sym = get_yahoo_ticker(clean_symbol, market)

        ticker = yf.Ticker(yahoo_sym)
        info = ticker.info

        # Get latest price
        hist = ticker.history(period="2d")
        if hist.empty or len(hist) < 1:
            return None

        latest_price = float(hist['Close'].iloc[-1])
        prev_close = float(hist['Close'].iloc[-2]) if len(hist) >= 2 else latest_price
        daily_chg = ((latest_price - prev_close) / prev_close * 100) if prev_close else 0

        # Get market cap (may not be available for all tickers)
        market_cap = info.get('marketCap', 0) or 0
        pe_ratio = info.get('trailingPE') or info.get('forwardPE') or None

        # Company names
        name_en = info.get('longName') or info.get('shortName') or clean_symbol
        name_cn = info.get('longName') or clean_symbol  # Use English as fallback

        # Domain for logo
        domain = info.get('website', '').replace('https://', '').replace('http://', '').split('/')[0] or ''

        return {
            'symbol': clean_symbol,
            'name_cn': name_cn,
            'name_en': name_en,
            'market': market,
            'domain': domain,
            'tag_type': market,
            'price': latest_price,
            'prev_close': prev_close,
            'daily_chg': daily_chg,
            'market_cap': market_cap,
            'pe_ratio': pe_ratio,
        }
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        return None


def save_fetched_ticker(conn, data: dict) -> bool:
    """Save fetched ticker to database."""
    try:
        with conn.cursor() as cur:
            # Insert/update ticker
            cur.execute("""
                INSERT INTO tickers (symbol, name_cn, name_en, market, domain, tag_type)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (symbol) DO UPDATE SET
                    name_cn = EXCLUDED.name_cn,
                    name_en = EXCLUDED.name_en,
                    domain = EXCLUDED.domain,
                    tag_type = EXCLUDED.tag_type
            """, (data['symbol'], data['name_cn'], data['name_en'],
                  data['market'], data['domain'], data['tag_type']))

            # Insert price snapshot
            cur.execute("""
                INSERT INTO price_snapshots
                    (symbol, price, prev_close, daily_chg, market_cap, pe_ratio, snapshot_at, market_date)
                VALUES (%s, %s, %s, %s, %s, %s, NOW(), %s)
            """, (data['symbol'], data['price'], data['prev_close'],
                  data['daily_chg'], data['market_cap'], data['pe_ratio'], date.today()))

            conn.commit()
            return True
    except Exception as e:
        print(f"Error saving ticker {data['symbol']}: {e}")
        conn.rollback()
        return False


class FetchRequest(BaseModel):
    symbol: str


# Ticker format: 1–10 alphanumerics, optional dot+1–4 char suffix (.HK, .T, .TWO …)
_TICKER_RE = re.compile(r'^[A-Z0-9]{1,10}(\.[A-Z]{1,4})?$')


@router.post("/watchlist/fetch")
def fetch_on_demand(req: FetchRequest) -> Any:
    """
    On-demand fetch a ticker from Yahoo Finance and add to database.
    Returns the fetched stock data.
    """
    if not YFINANCE_AVAILABLE:
        raise HTTPException(status_code=503, detail="YFinance not available on this server")

    symbol = req.symbol.upper().strip()
    if not _TICKER_RE.match(symbol):
        raise HTTPException(status_code=400, detail=f"Invalid ticker format: {symbol}")

    # Check if already exists
    with get_db() as conn:
        stocks = _fetch_latest(conn, ["US", "HK", "JP", "KR", "TW", "CN", "SG", "AU", "CA", "EU"])
        if symbol in stocks:
            return {"message": "Already exists", "stock": stocks[symbol]}

        # Try to fetch from Yahoo
        data = fetch_ticker_from_yahoo(symbol)
        if not data:
            raise HTTPException(status_code=404, detail=f"Could not fetch data for {symbol}")

        # Save to database
        if save_fetched_ticker(conn, data):
            # Return formatted stock data
            return {
                "message": "Fetched and saved",
                "stock": {
                    "symbol": data['symbol'],
                    "name_cn": data['name_cn'],
                    "name_en": data['name_en'],
                    "market": data['market'],
                    "price": round(data['price'], 4),
                    "prev_close": round(data['prev_close'], 4),
                    "daily_chg": round(data['daily_chg'], 2),
                    "ytd_chg": 0.0,  # Will be calculated after we have benchmark
                    "yoy_25_chg": 0.0,
                    "market_cap": int(data['market_cap']) if data['market_cap'] else 0,
                    "pe_ratio": round(data['pe_ratio'], 1) if data['pe_ratio'] else None,
                    "domain": data['domain'],
                    "tag": data['tag_type'],
                }
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to save ticker to database")


# ===== End on-demand fetching =====


def _market_status() -> str:
    tz = pytz.timezone('US/Eastern')
    now = datetime.now(tz)
    t = now.time()
    return "OPEN" if time(9, 30) <= t < time(16, 0) else "CLOSED"


def _fetch_latest(conn, market_filter: str | list[str] | None = None) -> dict[str, dict]:
    """
    Returns {symbol: {...}} with the latest snapshot for each ticker
    in the given market(s), joined with benchmark prices.
    """
    if isinstance(market_filter, str):
        markets = [market_filter]
    else:
        markets = market_filter

    placeholders = ','.join(['%s'] * len(markets))

    query = f"""
        SELECT DISTINCT ON (ps.symbol)
            ps.symbol,
            ps.price,
            ps.prev_close,
            ps.daily_chg,
            ps.market_cap,
            ps.pe_ratio,
            ps.snapshot_at,
            t.name_cn,
            t.name_en,
            t.domain,
            t.tag_type,
            b_ytd.price  AS price_ytd_base,
            b_yoy.price  AS price_yoy_base
        FROM price_snapshots ps
        JOIN tickers t ON ps.symbol = t.symbol
        LEFT JOIN annual_benchmarks b_ytd
            ON ps.symbol = b_ytd.symbol AND b_ytd.year = {BENCHMARK_YEAR}
        LEFT JOIN annual_benchmarks b_yoy
            ON ps.symbol = b_yoy.symbol AND b_yoy.year = {BENCHMARK_YEAR - 1}
        WHERE t.market IN ({placeholders})
        ORDER BY ps.symbol, ps.snapshot_at DESC
    """

    with conn.cursor() as cur:
        cur.execute(query, markets)
        rows = cur.fetchall()

    stocks: dict[str, dict] = {}
    for row in rows:
        (symbol, price, prev_close, daily_chg, market_cap, pe_ratio, snapshot_at,
         name_cn, name_en, domain, tag_type, price_ytd_base, price_yoy_base) = row

        price = float(price) if price else 0.0
        daily_chg = float(daily_chg) if daily_chg else 0.0

        ytd_chg = 0.0
        yoy_chg = 0.0
        if price_ytd_base and float(price_ytd_base) > 0 and price > 0:
            ytd_chg = (price - float(price_ytd_base)) / float(price_ytd_base) * 100
        if price_ytd_base and price_yoy_base and float(price_yoy_base) > 0:
            yoy_chg = ((float(price_ytd_base) - float(price_yoy_base))
                       / float(price_yoy_base) * 100)

        stocks[symbol] = {
            "symbol": symbol,
            "name_cn": name_cn or symbol,
            "name_en": name_en or "",
            "price": round(price, 4),
            "prev_close": round(float(prev_close), 4) if prev_close else 0.0,
            "daily_chg": round(daily_chg, 2),
            "ytd_chg": round(ytd_chg, 2),
            "yoy_25_chg": round(yoy_chg, 2),
            "market_cap": int(market_cap) if market_cap else 0,
            "pe_ratio": round(float(pe_ratio), 1) if pe_ratio and float(pe_ratio) > 0 else None,
            "domain": domain or "",
            "tag": tag_type or "",
            "updated_at": snapshot_at.isoformat() if snapshot_at else None,
        }
    return stocks


def _build_response(groups_config: list, stocks: dict,
                    market_status: str, updated_at: str | None) -> dict:
    groups_out = []
    for g in groups_config:
        syms = g["symbols"]
        items = [stocks[s] for s in syms if s in stocks]

        if g["sort_rule"] == "market_cap":
            items.sort(key=lambda x: x["market_cap"], reverse=True)
        # "manual" / "fixed" → keep insertion order

        if not items:
            continue

        # Group-level stats
        up = sum(1 for x in items if x["daily_chg"] >= 0)
        avg = sum(x["daily_chg"] for x in items) / len(items)
        best_day = max(items, key=lambda x: x["daily_chg"])
        best_ytd = max(items, key=lambda x: x["ytd_chg"])

        groups_out.append({
            "id": g["id"],
            "title": g["title"],
            "stocks": items,
            "stats": {
                "up": up,
                "total": len(items),
                "avg_chg": round(avg, 2),
                "best_day": {"symbol": best_day["symbol"], "chg": best_day["daily_chg"]},
                "best_ytd": {"symbol": best_ytd["symbol"], "chg": best_ytd["ytd_chg"]},
            },
        })

    return {
        "market_status": market_status,
        "updated_at": updated_at,
        "groups": groups_out,
    }


@router.get("/us")
def get_us_market() -> Any:
    with get_db() as conn:
        stocks = _fetch_latest(conn, "US")
    if not stocks:
        raise HTTPException(status_code=503, detail="No US data available yet")

    updated_at = max((s["updated_at"] for s in stocks.values() if s["updated_at"]),
                     default=None)
    return _build_response(US_GROUPS, stocks, _market_status(), updated_at)


@router.get("/hk")
def get_hk_market() -> Any:
    with get_db() as conn:
        stocks = _fetch_latest(conn, "HK")
    if not stocks:
        raise HTTPException(status_code=503, detail="No HK data available yet")

    updated_at = max((s["updated_at"] for s in stocks.values() if s["updated_at"]),
                     default=None)

    # HK market status (HKT = UTC+8)
    hk_tz = pytz.timezone('Asia/Hong_Kong')
    now_hk = datetime.now(hk_tz)
    t = now_hk.time()
    hk_status = "OPEN" if (time(9, 30) <= t < time(12, 0) or
                            time(13, 0) <= t < time(16, 0)) else "CLOSED"

    return _build_response(HK_GROUPS, stocks, hk_status, updated_at)


@router.get("/asia")
def get_asia_market() -> Any:
    with get_db() as conn:
        stocks = _fetch_latest(conn, ["JP", "KR", "TW"])
    if not stocks:
        raise HTTPException(status_code=503, detail="No Asia data available yet")

    updated_at = max((s["updated_at"] for s in stocks.values() if s["updated_at"]),
                     default=None)
    return _build_response(ASIA_GROUPS, stocks, "VARIES", updated_at)


@router.get("/ticker/{symbol}")
def get_ticker(symbol: str) -> Any:
    symbol = symbol.upper()
    with get_db() as conn:
        stocks = _fetch_latest(conn, ["US", "HK", "JP", "KR", "TW"])
    if symbol not in stocks:
        raise HTTPException(status_code=404, detail=f"{symbol} not found")
    return stocks[symbol]


@router.get("/ticker/{symbol}/history")
def get_ticker_history(symbol: str, days: int = 30) -> Any:
    symbol = symbol.upper()
    days = min(days, 365)
    query = """
        SELECT price, daily_chg, market_cap, snapshot_at, market_date
        FROM price_snapshots
        WHERE symbol = %s
          AND snapshot_at >= NOW() - make_interval(days => %s)
        ORDER BY snapshot_at DESC
        LIMIT 500
    """
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (symbol, days))
            rows = cur.fetchall()

    if not rows:
        raise HTTPException(status_code=404, detail=f"No history for {symbol}")

    return {
        "symbol": symbol,
        "history": [
            {
                "price": float(r[0]) if r[0] else 0,
                "daily_chg": float(r[1]) if r[1] else 0,
                "market_cap": int(r[2]) if r[2] else 0,
                "snapshot_at": r[3].isoformat(),
                "market_date": r[4].isoformat(),
            }
            for r in rows
        ],
    }
