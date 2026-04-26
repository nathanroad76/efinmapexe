"""
US market data collector.
Fetches prices via yfinance and writes to PostgreSQL.
Cron: */15 * * * *  (every 15 minutes)
"""
import os
import time
import warnings
import yfinance as yf
from datetime import datetime
import pytz

from proxy import get_proxy, apply_proxy
from db import get_connection, insert_ticker_if_missing, save_snapshot

warnings.filterwarnings('ignore')

# =============================================
# Group / ticker config
# =============================================
MANUAL_DOMAINS = {
    'IBIT': 'ishares.com', 'ETHA': 'ishares.com', 'MAGS': 'roundhillinvestments.com',
    'GLD': 'spdrgoldshares.com', 'USO': 'uscfinvestments.com', 'CPER': 'uscfinvestments.com',
    'TLT': 'ishares.com', 'SPY': 'spglobal.com', 'QQQ': 'invesco.com',
    'DIA': 'spdrs.com', 'IWM': 'ishares.com',
    'TSM': 'tsmc.com', 'NVDA': 'nvidia.com', 'AAPL': 'apple.com',
    'BRK.A': 'berkshirehathaway.com',
}

# Each entry: (yf_ticker, display_symbol, name_cn, domain_override, tag_type)
# domain_override=None means derive from yfinance info
GROUPS = [
    {
        "id": "global", "sort_rule": "manual",
        "manual_config": [
            ('^GSPC',   'SPX',    '标普500',   'spglobal.com',              'Index'),
            ('^IXIC',   'IXIC',   '纳斯达克',  'nasdaq.com',               'Index'),
            ('^DJI',    'DJI',    '道琼斯',    'dowjones.com',              'Index'),
            ('^RUT',    'RUT',    '罗素2000',  'ftserussell.com',           'Index'),
            ('MAGS',    'MAGS',   '七姐妹',    'roundhillinvestments.com',  'ETF'),
            ('IBIT',    'IBIT',   '比特币ETF', 'ishares.com',               'ETF'),
            ('GLD',     'GLD',    '黄金',      'spdrgoldshares.com',        'ETF'),
            ('USO',     'USO',    '原油',      'uscfinvestments.com',       'ETF'),
            ('CPER',    'CPER',   '铜',        'uscfinvestments.com',       'ETF'),
            ('TLT',     'TLT',    '20年美债',  'ishares.com',               'ETF'),
            ('DX-Y.NYB','DXY',    '美元指数',  'theice.com',                'INDEX'),
            ('JPY=X',   'USDJPY', '日元汇率',  'boj.or.jp',                 'Forex'),
        ]
    },
    {"id": "tech",       "sort_rule": "market_cap",
     "tickers": ['AAPL', 'NVDA', 'META', 'GOOGL', 'MSFT', 'AMZN', 'AVGO', 'TSM', 'TSLA',
                 'ORCL', 'NFLX', 'PLTR', 'AMD', 'MU', 'INTC']},
    {"id": "crypto",     "sort_rule": "market_cap",
     "tickers": ['IBIT', 'ETHA', 'HOOD', 'COIN', 'MSTR', 'CRCL', 'RIOT', 'MARA', 'CLSK']},
    {"id": "china",      "sort_rule": "market_cap",
     "tickers": ['BABA', 'PDD', 'NTES', 'JD', 'TCOM', 'LI', 'TME', 'BIDU', 'BEKE', 'FUTU', 'XPEV', 'YMM']},
    {"id": "healthcare", "sort_rule": "market_cap",
     "tickers": ['LLY', 'JNJ', 'ABBV', 'NVO', 'UNH', 'TMO', 'ISRG', 'BSX', 'REGN', 'HIMS', 'TWST', 'CRSP']},
    {"id": "consumer",   "sort_rule": "market_cap",
     "tickers": ['WMT', 'COST', 'HD', 'MCD', 'BKNG', 'TJX', 'LOW', 'SBUX', 'DASH', 'ABNB', 'CMG', 'AZO']},
    {"id": "staples",    "sort_rule": "market_cap",
     "tickers": ['PG', 'KO', 'PM', 'PEP', 'BUD', 'NKE', 'MDLZ', 'MNST', 'KHC', 'HSY', 'EL', 'LULU']},
    {"id": "industrials","sort_rule": "market_cap",
     "tickers": ['GE', 'LIN', 'RTX', 'CAT', 'BA', 'HON', 'ETN', 'DHR', 'LMT', 'MMM', 'SHW', 'EMR']},
    {"id": "energy",     "sort_rule": "market_cap",
     "tickers": ['XOM', 'CVX', 'TMUS', 'SHEL', 'T', 'UBER', 'VZ', 'NEE', 'UNP', 'SO', 'WM', 'UPS']},
    {"id": "finance",    "sort_rule": "market_cap",
     "tickers": ['BRK.A', 'JPM', 'V', 'MA', 'BAC', 'WFC', 'MS', 'GS', 'AXP', 'SCHW', 'BLK', 'IBKR']},
]

# =============================================
# Fetch logic
# =============================================
_current_proxy = None


def _ensure_proxy():
    global _current_proxy
    if not _current_proxy:
        _current_proxy = get_proxy()
        apply_proxy(_current_proxy)


def _rotate_proxy():
    global _current_proxy
    _current_proxy = get_proxy()
    apply_proxy(_current_proxy)
    print("  [proxy rotated]", flush=True)


def fetch_ticker(yf_symbol: str, display: str, name_cn: str,
                 domain: str | None, tag: str) -> dict | None:
    """Fetch one ticker from yfinance, returns a flat dict or None on failure."""
    _ensure_proxy()
    # BRK.A fix
    if 'BRK.A' in yf_symbol:
        yf_symbol = 'BRK-A'

    for attempt in range(3):
        try:
            info = yf.Ticker(yf_symbol).info
            price = (info.get('currentPrice') or info.get('regularMarketPrice')
                     or info.get('previousClose'))
            if price is None:
                return None
            price = float(price)
            prev_close = info.get('previousClose') or info.get('regularMarketPreviousClose') or price
            daily_chg = ((price - prev_close) / prev_close * 100) if prev_close else 0.0
            market_cap = info.get('marketCap', 0) or 0
            pe = info.get('trailingPE') or info.get('forwardPE')

            # Resolve domain
            resolved_domain = domain
            if not resolved_domain:
                website = info.get('website', '')
                if website:
                    from urllib.parse import urlparse
                    resolved_domain = urlparse(website).netloc.replace('www.', '')
                if not resolved_domain:
                    resolved_domain = f"{display.lower()}.com"

            # Resolve name
            if not name_cn:
                raw = info.get('shortName') or info.get('longName') or display
                name_cn = raw.split(' ')[0][:8]

            tag_resolved = tag
            if not tag_resolved:
                country = info.get('country', 'US')
                tag_resolved = country if country != 'United States' else 'US'

            print(f"  {display} OK  ${price:.2f}  {daily_chg:+.2f}%", flush=True)
            return {
                'symbol': display,
                'name_cn': name_cn,
                'domain': resolved_domain,
                'tag': tag_resolved,
                'price': price,
                'prev_close': float(prev_close),
                'daily_chg': daily_chg,
                'market_cap': int(market_cap),
                'pe_ratio': float(pe) if pe and pe > 0 else None,
            }
        except Exception as e:
            print(f"  {display} attempt {attempt+1} failed: {e}", flush=True)
            _rotate_proxy()
            time.sleep(2)

    print(f"  {display} SKIPPED after 3 attempts", flush=True)
    return None


def collect():
    seen = set()
    results = []

    for group in GROUPS:
        tasks = group.get('manual_config', [])
        if not tasks:
            tasks = [(t, t, '', None, '') for t in group.get('tickers', [])]

        for entry in tasks:
            yf_sym, display, name_cn, domain, tag = entry
            if display in seen:
                continue
            seen.add(display)

            # Override domain from MANUAL_DOMAINS if available
            if display in MANUAL_DOMAINS and not domain:
                domain = MANUAL_DOMAINS[display]

            data = fetch_ticker(yf_sym, display, name_cn, domain, tag)
            if data:
                results.append(data)
            time.sleep(0.15)

    return results


def main():
    print(f"[US collector] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", flush=True)
    results = collect()
    if not results:
        print("No data fetched, aborting DB write.", flush=True)
        return

    conn = get_connection()
    try:
        cur = conn.cursor()
        for r in results:
            insert_ticker_if_missing(cur, r['symbol'], r['name_cn'], '',
                                     'US', r['domain'], r['tag'])
            save_snapshot(cur, r['symbol'], r['price'], r['prev_close'],
                          r['daily_chg'], r['market_cap'], r['pe_ratio'])
        conn.commit()
        cur.close()
        print(f"Saved {len(results)} snapshots to DB.", flush=True)
    finally:
        conn.close()


if __name__ == '__main__':
    main()
