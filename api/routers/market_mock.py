"""
Mock data router for local testing without database.
Drop-in replacement for market.py during frontend development.
"""
from fastapi import APIRouter
from typing import Any
import random
from datetime import datetime

router = APIRouter(prefix="/market", tags=["market"])

# Mock stock data generator
def mock_stock(symbol: str, name_cn: str, market: str, base_price: float) -> dict:
    daily_chg = round(random.uniform(-5, 5), 2)
    price = round(base_price * (1 + daily_chg/100), 2)
    return {
        "symbol": symbol,
        "name_cn": name_cn,
        "name_en": symbol,
        "price": price,
        "prev_close": base_price,
        "daily_chg": daily_chg,
        "ytd_chg": round(random.uniform(-20, 30), 2),
        "yoy_25_chg": round(random.uniform(-15, 40), 2),
        "market_cap": int(random.uniform(10, 2000) * 1e9),
        "pe_ratio": round(random.uniform(10, 50), 1) if random.random() > 0.3 else None,
        "domain": f"{symbol.lower()}.com",
        "tag": "US" if market == "US" else market,
        "updated_at": datetime.now().isoformat(),
    }

# US Market mock data
US_MOCK = {
    "SPX": mock_stock("SPX", "标普500", "US", 5200),
    "IXIC": mock_stock("IXIC", "纳斯达克", "US", 16500),
    "AAPL": mock_stock("AAPL", "苹果", "US", 180),
    "NVDA": mock_stock("NVDA", "英伟达", "US", 880),
    "TSLA": mock_stock("TSLA", "特斯拉", "US", 175),
    "META": mock_stock("META", "Meta", "US", 500),
    "MSFT": mock_stock("MSFT", "微软", "US", 420),
    "AMZN": mock_stock("AMZN", "亚马逊", "US", 180),
    "GOOGL": mock_stock("GOOGL", "谷歌", "US", 165),
    "BABA": mock_stock("BABA", "阿里巴巴", "US", 75),
    "JD": mock_stock("JD", "京东", "US", 28),
    "COIN": mock_stock("COIN", "Coinbase", "US", 220),
    "PLTR": mock_stock("PLTR", "Palantir", "US", 80),
}

# HK Market mock data
HK_MOCK = {
    "0700.HK": mock_stock("0700.HK", "腾讯控股", "HK", 380),
    "9988.HK": mock_stock("9988.HK", "阿里巴巴", "HK", 85),
    "3690.HK": mock_stock("3690.HK", "美团", "HK", 120),
    "1810.HK": mock_stock("1810.HK", "小米集团", "HK", 18),
    "1211.HK": mock_stock("1211.HK", "比亚迪", "HK", 220),
}

# Asia Market mock data
ASIA_MOCK = {
    "9984.T": mock_stock("9984.T", "软银集团", "JP", 8500),
    "6758.T": mock_stock("6758.T", "索尼", "JP", 13500),
    "005930.KS": mock_stock("005930.KS", "三星电子", "KR", 72000),
    "2330.TW": mock_stock("2330.TW", "台积电", "TW", 850),
}

@router.get("/us")
def get_us_market() -> Any:
    return {
        "market_status": "OPEN",
        "updated_at": datetime.now().isoformat(),
        "groups": [{
            "id": "tech",
            "title": "美股科技 (Mock Data)",
            "stocks": list(US_MOCK.values()),
            "stats": {
                "up": 7,
                "total": 13,
                "avg_chg": 1.25,
                "best_day": {"symbol": "NVDA", "chg": 4.5},
                "best_ytd": {"symbol": "COIN", "chg": 45.2},
            }
        }]
    }

@router.get("/hk")
def get_hk_market() -> Any:
    return {
        "market_status": "CLOSED",
        "updated_at": datetime.now().isoformat(),
        "groups": [{
            "id": "core",
            "title": "港股核心 (Mock Data)",
            "stocks": list(HK_MOCK.values()),
            "stats": {
                "up": 3,
                "total": 5,
                "avg_chg": -0.5,
                "best_day": {"symbol": "0700.HK", "chg": 2.1},
                "best_ytd": {"symbol": "1211.HK", "chg": 15.3},
            }
        }]
    }

@router.get("/asia")
def get_asia_market() -> Any:
    return {
        "market_status": "VARIES",
        "updated_at": datetime.now().isoformat(),
        "groups": [{
            "id": "asia",
            "title": "日韩台科技 (Mock Data)",
            "stocks": list(ASIA_MOCK.values()),
            "stats": {
                "up": 2,
                "total": 4,
                "avg_chg": 0.8,
                "best_day": {"symbol": "2330.TW", "chg": 3.2},
                "best_ytd": {"symbol": "005930.KS", "chg": 22.1},
            }
        }]
    }

@router.get("/ticker/{symbol}")
def get_ticker(symbol: str) -> Any:
    symbol = symbol.upper()
    all_stocks = {**US_MOCK, **HK_MOCK, **ASIA_MOCK}
    if symbol not in all_stocks:
        return {"error": f"{symbol} not found"}
    return all_stocks[symbol]
