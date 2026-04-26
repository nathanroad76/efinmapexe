"""
Asia (JP / KR / TW) market data collector.
Cron: */20 * * * *
"""
import time
import yfinance as yf
from datetime import datetime

from proxy import get_proxy, apply_proxy
from db import get_connection, insert_ticker_if_missing, save_snapshot

# =============================================
# All Asia tickers with their exchange suffix
# =============================================
ASIA_TICKERS = [
    # Japan
    '9984.T', '6758.T', '6501.T', '6752.T', '6702.T', '7974.T', '8035.T', '6857.T',
    '4063.T', '6920.T', '6723.T', '6971.T', '6981.T', '6301.T', '6594.T', '6954.T',
    '6367.T', '6273.T', '7203.T', '7267.T', '7269.T', '6902.T', '9983.T', '4911.T',
    '8001.T', '8058.T', '3382.T', '2914.T', '7581.T', '4502.T', '4568.T', '4519.T',
    '4503.T', '7741.T', '7733.T', '4543.T', '6098.T',
    # Korea
    '005930.KS', '000660.KS', '066570.KS', '009150.KS', '373220.KS', '006400.KS',
    '051910.KS', '005490.KS', '005380.KS', '000270.KS', '012330.KS', '329180.KS',
    '241560.KS', '207940.KS', '068270.KS', '035420.KS', '035720.KS', '090430.KS',
    '097950.KS', '352820.KS', '105560.KS',
    # Taiwan
    '2330.TW', '2454.TW', '3711.TW', '2303.TW', '3034.TW', '2317.TW', '2382.TW',
    '2308.TW', '3231.TW', '3008.TW', '2357.TW', '2395.TW', '5274.TWO', '1301.TW',
    '2603.TW',
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


def get_exchange_rates() -> dict:
    """Fetch USD/JPY, USD/KRW, USD/TWD exchange rates."""
    print("Fetching exchange rates...", flush=True)
    rates = {'JP': 150.0, 'KR': 1300.0, 'TW': 32.0}
    pairs = {'JP': 'JPY=X', 'KR': 'KRW=X', 'TW': 'TWD=X'}
    try:
        data = yf.Tickers(" ".join(pairs.values()))
        for region, sym in pairs.items():
            info = data.tickers[sym].info
            price = info.get('regularMarketPrice') or info.get('currentPrice')
            if price:
                rates[region] = float(price)
    except Exception as e:
        print(f"  Exchange rate fetch failed: {e}", flush=True)
    return rates


def market_of(symbol: str) -> str:
    if symbol.endswith('.T'):
        return 'JP'
    if symbol.endswith('.KS') or symbol.endswith('.KQ'):
        return 'KR'
    return 'TW'


def fetch_asia_ticker(symbol: str, rates: dict) -> dict | None:
    _ensure_proxy()
    mkt = market_of(symbol)

    for attempt in range(3):
        try:
            info = yf.Ticker(symbol).info
            price = (info.get('currentPrice') or info.get('regularMarketPrice')
                     or info.get('previousClose'))
            if price is None:
                return None
            price = float(price)
            prev_close = info.get('previousClose') or price
            daily_chg = ((price - prev_close) / prev_close * 100) if prev_close else 0.0

            # Convert local market cap to USD
            mcap_local = info.get('marketCap', 0) or 0
            rate = rates.get(mkt, 1.0)
            market_cap_usd = int(mcap_local / rate) if mcap_local else 0

            pe = info.get('trailingPE')

            # Yahoo metadata for first-time registration (overwritten only by re-seed)
            name_en = info.get('shortName') or info.get('longName') or symbol
            website = info.get('website', '')
            domain = ''
            if website:
                from urllib.parse import urlparse
                domain = urlparse(website).netloc.replace('www.', '')

            print(f"  {symbol} OK  {price:.0f}  {daily_chg:+.2f}%", flush=True)
            return {
                'symbol': symbol,
                'name_cn': name_en,  # placeholder; seed_data.py provides curated 中文名
                'name_en': name_en,
                'domain': domain,
                'market': mkt,
                'price': price,
                'prev_close': float(prev_close),
                'daily_chg': daily_chg,
                'market_cap': market_cap_usd,
                'pe_ratio': float(pe) if pe and pe > 0 else None,
            }
        except Exception as e:
            print(f"  {symbol} attempt {attempt+1} failed: {e}", flush=True)
            _rotate_proxy()
            time.sleep(2)

    print(f"  {symbol} SKIPPED", flush=True)
    return None


def main():
    print(f"[Asia collector] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", flush=True)
    _ensure_proxy()
    rates = get_exchange_rates()

    conn = get_connection()
    saved = 0
    try:
        cur = conn.cursor()
        for i, symbol in enumerate(ASIA_TICKERS):
            print(f"[{i+1}/{len(ASIA_TICKERS)}]", end=' ')
            data = fetch_asia_ticker(symbol, rates)
            if data:
                insert_ticker_if_missing(cur, data['symbol'], data['name_cn'],
                                         data['name_en'], data['market'],
                                         data['domain'], data['market'])
                save_snapshot(cur, data['symbol'], data['price'], data['prev_close'],
                              data['daily_chg'], data['market_cap'], data['pe_ratio'])
                saved += 1
            time.sleep(0.5)

        conn.commit()
        cur.close()
        print(f"Saved {saved} Asia snapshots.", flush=True)
    finally:
        conn.close()


if __name__ == '__main__':
    main()
