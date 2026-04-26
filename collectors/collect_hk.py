"""
HK market data collector.
Cron: */15 * * * *  (runs during HK trading hours)
"""
import os
import re
import time
import random
import string
import yfinance as yf
from datetime import date, datetime

from proxy import get_proxy, apply_proxy
from db import get_connection, upsert_ticker, save_snapshot

# =============================================
# Ticker list (code without .HK suffix, 5 digits)
# =============================================
ALL_HK_TICKERS = [
    '00001', '00005', '00006', '00016', '00020', '00066', '00100', '00101', '00135',
    '00175', '00179', '00189', '00241', '00257', '00267', '00285', '00291', '00371',
    '00388', '00425', '00522', '00551', '00669', '00688', '00700', '00728', '00762',
    '00772', '00788', '00836', '00883', '00939', '00941', '00960', '00968', '00981',
    '00992', '01024', '01093', '01109', '01171', '01177', '01208', '01209', '01211',
    '01299', '01308', '01347', '01357', '01378', '01398', '01519', '01530', '01548',
    '01585', '01788', '01801', '01810', '01816', '01818', '01888', '01918', '01951',
    '02007', '02018', '02020', '02057', '02097', '02228', '02269', '02313', '02318',
    '02319', '02328', '02331', '02367', '02382', '02400', '02498', '02577', '02588',
    '02602', '02618', '02628', '02688', '02899', '03360', '03690', '03692', '03887',
    '03931', '06082', '06181', '06618', '06862', '06969', '09626', '09633', '09660',
    '09863', '09926', '09956', '09979', '09985', '09987', '09988', '09992', '09995',
]

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


def fetch_hk_ticker(code: str) -> dict | None:
    """code is 5-digit string like '00700'. Returns dict or None."""
    _ensure_proxy()
    yf_symbol = f"{int(code):04d}.HK"  # '00700' → '0700.HK'

    for attempt in range(3):
        try:
            info = yf.Ticker(yf_symbol).info
            price = (info.get('currentPrice') or info.get('regularMarketPrice')
                     or info.get('previousClose'))
            if price is None:
                return None
            price = float(price)
            prev_close = info.get('previousClose') or price
            daily_chg = ((price - prev_close) / prev_close * 100) if prev_close else 0.0
            market_cap_hkd = info.get('marketCap', 0) or 0

            pe = info.get('trailingPE')

            print(f"  {yf_symbol} OK  {price:.2f}  {daily_chg:+.2f}%", flush=True)
            return {
                'symbol': yf_symbol,
                'price': price,
                'prev_close': float(prev_close),
                'daily_chg': daily_chg,
                'market_cap': int(market_cap_hkd),
                'pe_ratio': float(pe) if pe and pe > 0 else None,
            }
        except Exception as e:
            print(f"  {yf_symbol} attempt {attempt+1} failed: {e}", flush=True)
            _rotate_proxy()
            time.sleep(2)

    print(f"  {yf_symbol} SKIPPED", flush=True)
    return None


def main():
    print(f"[HK collector] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", flush=True)
    _ensure_proxy()

    conn = get_connection()
    saved = 0
    try:
        cur = conn.cursor()
        for i, code in enumerate(ALL_HK_TICKERS):
            print(f"[{i+1}/{len(ALL_HK_TICKERS)}]", end=' ')
            data = fetch_hk_ticker(code)
            if data:
                # Ticker metadata is already seeded; just save the snapshot
                save_snapshot(cur, data['symbol'], data['price'], data['prev_close'],
                              data['daily_chg'], data['market_cap'], data['pe_ratio'])
                saved += 1
            time.sleep(0.5)

        conn.commit()
        cur.close()
        print(f"Saved {saved} HK snapshots.", flush=True)
    finally:
        conn.close()


if __name__ == '__main__':
    main()
