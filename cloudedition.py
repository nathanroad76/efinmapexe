import requests
import numpy as np
from datetime import datetime, time
import pytz
import warnings
import os
import time as time_module
import yfinance as yf

warnings.filterwarnings('ignore')

# ===========================
# 0. Yahoo Finance URL 映射
# ===========================
TICKER_URL_MAP = {
    'AAPL': 'https://finance.yahoo.com/quote/AAPL/',
    'AVGO': 'https://finance.yahoo.com/quote/AVGO/',
    'BAC': 'https://finance.yahoo.com/quote/BAC/',
    'BRK.A': 'https://finance.yahoo.com/quote/BRK.A/',
    'BSX': 'https://finance.yahoo.com/quote/BSX/',
    'COIN': 'https://finance.yahoo.com/quote/COIN/',
    'DASH': 'https://finance.yahoo.com/quote/DASH/',
    'ETHA': 'https://finance.yahoo.com/quote/ETHA/',
    'GOOGL': 'https://finance.yahoo.com/quote/GOOGL/',
    'HOOD': 'https://finance.yahoo.com/quote/HOOD/',
    'ISRG': 'https://finance.yahoo.com/quote/ISRG/',
    'KHC': 'https://finance.yahoo.com/quote/KHC/',
    'LMT': 'https://finance.yahoo.com/quote/LMT/',
    'MARA': 'https://finance.yahoo.com/quote/MARA/',
    'MNST': 'https://finance.yahoo.com/quote/MNST/',
    'NEE': 'https://finance.yahoo.com/quote/NEE/',
    'NVO': 'https://finance.yahoo.com/quote/NVO/',
    'PLTR': 'https://finance.yahoo.com/quote/PLTR/',
    'RTX': 'https://finance.yahoo.com/quote/RTX/',
    'SO': 'https://finance.yahoo.com/quote/SO/',
    'TLH': 'https://finance.yahoo.com/quote/TLH/',
    'TSM': 'https://finance.yahoo.com/quote/TSM/',
    'UPS': 'https://finance.yahoo.com/quote/UPS/',
    'WM': 'https://finance.yahoo.com/quote/WM/',
    'TLT': 'https://finance.yahoo.com/quote/TLT/',
    'RUT': 'https://finance.yahoo.com/quote/%5ERUT/',
    'ABBV': 'https://finance.yahoo.com/quote/ABBV/',
    'AXP': 'https://finance.yahoo.com/quote/AXP/',
    'BEKE': 'https://finance.yahoo.com/quote/BEKE/',
    'BRK-A': 'https://finance.yahoo.com/quote/BRK-A/',
    'BUD': 'https://finance.yahoo.com/quote/BUD/',
    'COST': 'https://finance.yahoo.com/quote/COST/',
    'DHR': 'https://finance.yahoo.com/quote/DHR/',
    'ETN': 'https://finance.yahoo.com/quote/ETN/',
    'GS': 'https://finance.yahoo.com/quote/GS/',
    'HSY': 'https://finance.yahoo.com/quote/HSY/',
    'IWM': 'https://finance.yahoo.com/quote/IWM/',
    'KO': 'https://finance.yahoo.com/quote/KO/',
    'LOW': 'https://finance.yahoo.com/quote/LOW/',
    'MCD': 'https://finance.yahoo.com/quote/MCD/',
    'MS': 'https://finance.yahoo.com/quote/MS/',
    'NFLX': 'https://finance.yahoo.com/quote/NFLX/',
    'ORCL': 'https://finance.yahoo.com/quote/ORCL/',
    'PM': 'https://finance.yahoo.com/quote/PM/',
    'SBUX': 'https://finance.yahoo.com/quote/SBUX/',
    'SPY': 'https://finance.yahoo.com/quote/SPY/',
    'TME': 'https://finance.yahoo.com/quote/TME/',
    'TWST': 'https://finance.yahoo.com/quote/TWST/',
    'USO': 'https://finance.yahoo.com/quote/USO/',
    'WMT': 'https://finance.yahoo.com/quote/WMT/',
    'DX-Y.NYB': 'https://finance.yahoo.com/quote/DX-Y.NYB/',
    'ABNB': 'https://finance.yahoo.com/quote/ABNB/',
    'AZO': 'https://finance.yahoo.com/quote/AZO/',
    'BIDU': 'https://finance.yahoo.com/quote/BIDU/',
    'CAT': 'https://finance.yahoo.com/quote/CAT/',
    'CRCL': 'https://finance.yahoo.com/quote/CRCL/',
    'DIA': 'https://finance.yahoo.com/quote/DIA/',
    'FUTU': 'https://finance.yahoo.com/quote/FUTU/',
    'HD': 'https://finance.yahoo.com/quote/HD/',
    'IBIT': 'https://finance.yahoo.com/quote/IBIT/',
    'JD': 'https://finance.yahoo.com/quote/JD/',
    'LI': 'https://finance.yahoo.com/quote/LI/',
    'LULU': 'https://finance.yahoo.com/quote/LULU/',
    'MDLZ': 'https://finance.yahoo.com/quote/MDLZ/',
    'MSFT': 'https://finance.yahoo.com/quote/MSFT/',
    'NKE': 'https://finance.yahoo.com/quote/NKE/',
    'PDD': 'https://finance.yahoo.com/quote/PDD/',
    'QQQ': 'https://finance.yahoo.com/quote/QQQ/',
    'SCHW': 'https://finance.yahoo.com/quote/SCHW/',
    'T': 'https://finance.yahoo.com/quote/T/',
    'TMO': 'https://finance.yahoo.com/quote/TMO/',
    'UBER': 'https://finance.yahoo.com/quote/UBER/',
    'V': 'https://finance.yahoo.com/quote/V/',
    'XOM': 'https://finance.yahoo.com/quote/XOM/',
    'SPX': 'https://finance.yahoo.com/quote/SPX/',
    'AMD': 'https://finance.yahoo.com/quote/AMD/',
    'BA': 'https://finance.yahoo.com/quote/BA/',
    'BKNG': 'https://finance.yahoo.com/quote/BKNG/',
    'CLSK': 'https://finance.yahoo.com/quote/CLSK/',
    'CRSP': 'https://finance.yahoo.com/quote/CRSP/',
    'EL': 'https://finance.yahoo.com/quote/EL/',
    'GE': 'https://finance.yahoo.com/quote/GE/',
    'HIMS': 'https://finance.yahoo.com/quote/HIMS/',
    'IBKR': 'https://finance.yahoo.com/quote/IBKR/',
    'JNJ': 'https://finance.yahoo.com/quote/JNJ/',
    'LIN': 'https://finance.yahoo.com/quote/LIN/',
    'MA': 'https://finance.yahoo.com/quote/MA/',
    'META': 'https://finance.yahoo.com/quote/META/',
    'MSTR': 'https://finance.yahoo.com/quote/MSTR/',
    'NTES': 'https://finance.yahoo.com/quote/NTES/',
    'PEP': 'https://finance.yahoo.com/quote/PEP/',
    'REGN': 'https://finance.yahoo.com/quote/REGN/',
    'SHEL': 'https://finance.yahoo.com/quote/SHEL/',
    'TCOM': 'https://finance.yahoo.com/quote/TCOM/',
    'TMUS': 'https://finance.yahoo.com/quote/TMUS/',
    'UNH': 'https://finance.yahoo.com/quote/UNH/',
    'VZ': 'https://finance.yahoo.com/quote/VZ/',
    'XPEV': 'https://finance.yahoo.com/quote/XPEV/',
    'DJI': 'https://finance.yahoo.com/quote/DJI/',
    'AMZN': 'https://finance.yahoo.com/quote/AMZN/',
    'BABA': 'https://finance.yahoo.com/quote/BABA/',
    'BLK': 'https://finance.yahoo.com/quote/BLK/',
    'CMG': 'https://finance.yahoo.com/quote/CMG/',
    'CVX': 'https://finance.yahoo.com/quote/CVX/',
    'EMR': 'https://finance.yahoo.com/quote/EMR/',
    'GLD': 'https://finance.yahoo.com/quote/GLD/',
    'HON': 'https://finance.yahoo.com/quote/HON/',
    'INTC': 'https://finance.yahoo.com/quote/INTC/',
    'JPM': 'https://finance.yahoo.com/quote/JPM/',
    'LLY': 'https://finance.yahoo.com/quote/LLY/',
    'MAGS': 'https://finance.yahoo.com/quote/MAGS/',
    'MMM': 'https://finance.yahoo.com/quote/MMM/',
    'MU': 'https://finance.yahoo.com/quote/MU/',
    'NVDA': 'https://finance.yahoo.com/quote/NVDA/',
    'PG': 'https://finance.yahoo.com/quote/PG/',
    'RIOT': 'https://finance.yahoo.com/quote/RIOT/',
    'SHW': 'https://finance.yahoo.com/quote/SHW/',
    'TJX': 'https://finance.yahoo.com/quote/TJX/',
    'TSLA': 'https://finance.yahoo.com/quote/TSLA/',
    'UNP': 'https://finance.yahoo.com/quote/UNP/',
    'WFC': 'https://finance.yahoo.com/quote/WFC/',
    'YMM': 'https://finance.yahoo.com/quote/YMM/',
}

# ===========================
# 1. 代理配置
# ===========================
# Updated Proxy API URL as requested
PROXY_API_URL = "blurpath.net:15132:pdd6wxr7bg-zone-resi-region-HK,JP,TW,US-st--city--session-zPDM-sessionTime-0:NerxBq"

def get_proxy():
    """
    配置固定代理 IP (根据提供的格式直接解析)
    格式: host:port:username:password
    """
    print("  🔄 正在配置代理...", end="")
    try:
        # 解析提供的字符串: blurpath.net:15132:pdd6wxr7bg...:NerxBq
        parts = PROXY_API_URL.split(':')
        if len(parts) == 4:
            host = parts[0]
            port = parts[1]
            username = parts[2]
            password = parts[3]
            
            # 构建带认证的代理字符串
            proxy_str = f"http://{username}:{password}@{host}:{port}"
            print(f" 配置成功: {host}:{port}")
            return proxy_str
        else:
            print(f" 代理格式错误，无法解析: {PROXY_API_URL}")
            return None
    except Exception as e:
        print(f" 配置代理异常: {e}")
    return None

# 全局变量存储当前代理
CURRENT_PROXY = None

# ===========================
# 1. 静态数据配置
# ===========================

# 2024年最后一个交易日收盘价 (基准数据 - 用于计算 25 YoY 的分母)
YTD_BASE_PRICES = {
    'AAPL': 249.29, 'ABBV': 171.70, 'ABNB': 131.41, 'AMD': 120.79, 'AMZN': 219.39,
    'AVGO': 230.20, 'AXP': 293.63, 'AZO': 3202.00, 'BA': 177.00, 'BABA': 83.38,
    'BAC': 42.96, 'BEKE': 18.04, 'BIDU': 84.31, 'BKNG': 4931.77, 'BLK': 1004.52,
    'BRK.A': 680920.00, 'BRK-A': 680920.00,
    'BSX': 89.32, 'BUD': 49.22, 'CAT': 357.36, 'CLSK': 9.21, 'CMG': 60.30,
    'COIN': 248.30, 'COST': 911.51, 'CRCL': 31.00, 'CRSP': 39.36, 'CVX': 138.42,
    'DASH': 167.75, 'DHR': 228.43, 'DIA': 419.87, 'EL': 73.68, 'EMR': 121.85,
    'ETHA': 25.29, 'ETN': 328.55, 'FUTU': 79.99, 'GE': 166.03, 'GLD': 242.13,
    'GOOGL': 188.56, 'GS': 561.17, 'HD': 379.53, 'HIMS': 24.18, 'HON': 208.35,
    'HOOD': 37.26, 'HSY': 163.97, 'IBIT': 53.05, 'IBKR': 43.94, 'INTC': 20.05,
    'ISRG': 521.96, 'IWM': 218.50, 'JD': 33.68, 'JNJ': 140.32, 'JPM': 234.74,
    'KHC': 28.98, 'KO': 60.48, 'LI': 23.99, 'LIN': 413.11, 'LLY': 766.28,
    'LMT': 472.03, 'LOW': 241.95, 'LULU': 382.41, 'MA': 523.56, 'MAGS': 54.42,
    'MARA': 16.77, 'MCD': 283.28, 'MDLZ': 58.43, 'META': 583.67, 'MMM': 126.70,
    'MNST': 52.56, 'MS': 122.30, 'MSFT': 418.41, 'MSTR': 289.62, 'MU': 83.92,
    'NEE': 69.52, 'NFLX': 89.13, 'NKE': 73.93, 'NTES': 86.95, 'NVDA': 134.25,
    'NVO': 83.71, 'ORCL': 165.00, 'PDD': 96.99, 'PEP': 146.22, 'PG': 163.33,
    'PLTR': 75.63, 'PM': 117.30, 'QQQ': 509.31, 'REGN': 708.40, 'RIOT': 10.21,
    'RTX': 113.60, 'SBUX': 88.89, 'SCHW': 73.11, 'SHEL': 60.15, 'SHW': 336.93,
    'SO': 79.65, 'SPY': 580.99, 'T': 21.79, 'TCOM': 68.33, 'TJX': 119.33,
    'TLH': 95.84, 'TME': 11.21, 'TMO': 518.40, 'TMUS': 217.34, 'TSLA': 403.84,
    'TSM': 194.86, 'TWST': 46.47, 'UBER': 60.32, 'UNH': 493.70, 'UNP': 222.73,
    'UPS': 117.99, 'USO': 75.55, 'V': 313.81, 'VZ': 37.41, 'WFC': 68.75,
    'WM': 198.83, 'WMT': 89.49, 'XOM': 103.76, 'XPEV': 11.82, 'YMM': 10.73,
    'TLT': 95.84, 'DX-Y.NYB': 106.0, 'SPX':5881.63, 'IXIC':19310.79, 'DJI':42544.22,
    'RUT':2230.16, 'USDJPY': 157.30  # 新增：2024年底日元汇率基准
}

# 2025年最后一个交易日收盘价 (目标数据 - 用于计算 YTD 基准 和 25 YoY 分子)
TARGET_2025_PRICES = {
    'AAPL': 271.86, 'ABBV': 228.49, 'ABNB': 135.72, 'AMD': 214.16, 'AMZN': 230.82,
    'AVGO': 346.10, 'AXP': 369.13, 'AZO': 3391.50, 'BA': 217.12, 'BABA': 146.58,
    'BAC': 55.00, 'BEKE': 15.76, 'BIDU': 130.66, 'BKNG': 5355.33, 'BLK': 1070.34,
    'BRK.A': 754800.00, 'BRK-A': 754800.00,
    'BSX': 95.35, 'BUD': 64.04, 'CAT': 572.87, 'CLSK': 10.12, 'CMG': 37.00,
    'COIN': 226.14, 'COST': 862.34, 'CRCL': 79.30, 'CRSP': 52.44, 'CVX': 152.41,
    'DASH': 226.48, 'DHR': 228.92, 'DIA': 480.57, 'EL': 104.72, 'EMR': 132.72,
    'ETHA': 22.43, 'ETN': 318.51, 'FUTU': 164.21, 'GE': 308.03, 'GLD': 396.31,
    'GOOGL': 313.00, 'GS': 879.00, 'HD': 344.10, 'HIMS': 32.47, 'HON': 195.09,
    'HOOD': 113.10, 'HSY': 181.98, 'IBIT': 49.65, 'IBKR': 64.31, 'INTC': 36.90,
    'ISRG': 566.36, 'IWM': 246.16, 'JD': 28.70, 'JNJ': 206.95, 'JPM': 322.22,
    'KHC': 24.25, 'KO': 69.91, 'LI': 16.93, 'LIN': 426.39, 'LLY': 1074.68,
    'LMT': 483.67, 'LOW': 241.16, 'LULU': 207.81, 'MA': 570.88, 'MAGS': 65.96,
    'MARA': 8.98, 'MCD': 305.63, 'MDLZ': 53.83, 'META': 660.09, 'MMM': 160.10,
    'MNST': 76.67, 'MS': 177.53, 'MSFT': 483.62, 'MSTR': 151.95, 'MU': 285.41,
    'NEE': 80.28, 'NFLX': 93.76, 'NKE': 63.71, 'NTES': 137.62, 'NVDA': 186.50,
    'NVO': 50.88, 'ORCL': 194.91, 'PDD': 113.39, 'PEP': 143.52, 'PG': 143.31,
    'PLTR': 177.75, 'PM': 160.40, 'QQQ': 614.31, 'REGN': 771.87, 'RIOT': 12.67,
    'RTX': 183.40, 'SBUX': 84.21, 'SCHW': 99.91, 'SHEL': 73.48, 'SHW': 324.03,
    'SO': 87.20, 'SPY': 681.92, 'T': 24.84, 'TCOM': 71.91, 'TJX': 153.61,
    'TLH': 101.67, 'TME': 17.53, 'TMO': 579.45, 'TMUS': 203.04, 'TSLA': 449.72,
    'TSM': 303.89, 'TWST': 31.72, 'UBER': 81.71, 'UNH': 330.11, 'UNP': 231.32,
    'UPS': 99.19, 'USO': 69.16, 'V': 350.71, 'VZ': 40.73, 'WFC': 93.20, 'WM': 219.71,
    'WMT': 111.41, 'XOM': 120.34, 'XPEV': 20.28, 'YMM': 10.73, 'TLT': 87.16,
    'DX-Y.NYB': 98.28, 'SPX':6845.50, 'IXIC':23241.99, 'DJI':48063.29,
    'RUT':2481.91, 'USDJPY': 156.90  # 新增：2025年底日元汇率基准
}

# ===========================
# 2. 股票分组配置
# ===========================
MANUAL_DOMAINS = {
    'IBIT': 'ishares.com', 'ETHA': 'ishares.com', 'GBTC': 'grayscale.com',
    'BITO': 'proshares.com', 'MAGS': 'roundhillinvestments.com',
    'GLD': 'spdrgoldshares.com', 'IAU': 'ishares.com', 'SLV': 'ishares.com',
    'USO': 'uscfinvestments.com', 'CPER': 'uscfinvestments.com',
    'TLT': 'ishares.com', 'TQQQ': 'proshares.com', 'SOXL': 'direxion.com',
    'JEPI': 'jpmorgan.com', 'SCHD': 'schwabassetmanagement.com',
    'SPY': 'spglobal.com', 'QQQ': 'invesco.com', 'DIA': 'spdrs.com', 'IWM': 'ishares.com',
    'TSM': 'tsmc.com', 'NVDA': 'nvidia.com', 'AAPL': 'apple.com',
    'BRK.A': 'berkshirehathaway.com', 'BRK-A': 'berkshirehathaway.com'
}

GROUPS = [
    {
        "id": "global", "title": "1. Global Markets (ETF) • 全球市场核心", "sort_rule": "manual",
        "manual_config": [
            {'ticker': '^GSPC', 'display': 'SPX', 'name_cn': '标普500', 'domain': 'spglobal.com', 'type': 'Index'},
            {'ticker': '^IXIC', 'display': 'IXIC', 'name_cn': '纳斯达克', 'domain': 'nasdaq.com', 'type': 'Index'},
            {'ticker': '^DJI', 'display': 'DJI', 'name_cn': '道琼斯', 'domain': 'dowjones.com', 'type': 'Index'},
            {'ticker': '^RUT', 'display': 'RUT', 'name_cn': '罗素2000', 'domain': 'ftserussell.com', 'type': 'Index'},
            {'ticker': 'MAGS', 'display': 'MAG7', 'name_cn': '七姐妹', 'type': 'ETF'},
            {'ticker': 'IBIT', 'display': 'IBIT', 'name_cn': '比特币', 'type': 'ETF'},
            {'ticker': 'GLD', 'display': 'GLD', 'name_cn': '黄金', 'type': 'ETF'},
            {'ticker': 'USO', 'display': 'USO', 'name_cn': '原油', 'type': 'ETF'},
            {'ticker': 'CPER', 'display': 'CPER', 'name_cn': '铜', 'domain': 'uscfinvestments.com', 'type': 'ETF'},
            {'ticker': 'TLT', 'display': 'TLT', 'name_cn': '20年美债', 'type': 'ETF'},
            {'ticker': 'DX-Y.NYB', 'display': 'DXY', 'name_cn': '美元指数', 'type': 'INDEX'},
            {'ticker': 'JPY=X', 'display': 'USDJPY', 'name_cn': '日元汇率', 'domain': 'boj.or.jp', 'type': 'Forex'}
        ]
    },
    {"id": "tech", "title": "2. US Tech Giants • 美股科技巨头", "sort_rule": "market_cap",
     "tickers": ['AAPL', 'NVDA', 'META', 'GOOGL', 'MSFT', 'AMZN', 'AVGO', 'TSM', 'TSLA', 'ORCL', 'NFLX', 'PLTR', 'AMD',
                 'MU', 'INTC']},
    {"id": "crypto", "title": "3. Crypto & Blockchain • 加密货币核心", "sort_rule": "crypto_special",
     "tickers": ['IBIT', 'ETHA', 'HOOD', 'COIN', 'MSTR', 'CRCL', 'RIOT', 'MARA', 'CLSK']},
    {"id": "china", "title": "4. China Core Assets • 中概股核心资产", "sort_rule": "market_cap",
     "tickers": ['BABA', 'PDD', 'NTES', 'JD', 'TCOM', 'LI', 'TME', 'BIDU', 'BEKE', 'FUTU', 'XPEV', 'YMM']},
    {"id": "healthcare", "title": "5. Health Care • 医疗健康", "sort_rule": "market_cap",
     "tickers": ['LLY', 'JNJ', 'ABBV', 'NVO', 'UNH', 'TMO', 'ISRG', 'BSX', 'REGN', 'HIMS', 'TWST', 'CRSP']},
    {"id": "consumer", "title": "6. Global Consumer • 零售/餐饮/旅游", "sort_rule": "market_cap",
     "tickers": ['WMT', 'COST', 'HD', 'MCD', 'BKNG', 'TJX', 'LOW', 'SBUX', 'DASH', 'ABNB', 'CMG', 'AZO']},
    {"id": "staples", "title": "7. Staples & Discretionary • 必需/可选消费", "sort_rule": "market_cap",
     "tickers": ['PG', 'KO', 'PM', 'PEP', 'BUD', 'NKE', 'MDLZ', 'MNST', 'KHC', 'HSY', 'EL', 'LULU']},
    {"id": "industrials", "title": "8. Industrials & Materials • 工业/材料", "sort_rule": "market_cap",
     "tickers": ['GE', 'LIN', 'RTX', 'CAT', 'BA', 'HON', 'ETN', 'DHR', 'LMT', 'MMM', 'SHW', 'EMR']},
    {"id": "energy", "title": "9. Energy, Telecom & Transport • 能源/电信/运输", "sort_rule": "market_cap",
     "tickers": ['XOM', 'CVX', 'TMUS', 'SHEL', 'T', 'UBER', 'VZ', 'NEE', 'UNP', 'SO', 'WM', 'UPS']},
    {"id": "finance", "title": "10. Banks & Finance • 银行/支付/投资", "sort_rule": "market_cap",
     "tickers": ['BRK.A', 'JPM', 'V', 'MA', 'BAC', 'WFC', 'MS', 'GS', 'AXP', 'SCHW', 'BLK', 'IBKR']}
]


# ===========================
# 3. 辅助函数 (颜色计算)
# ===========================

def interpolate_rgb(val, min_val, max_val, start_rgb, end_rgb):
    """线性插值计算颜色"""
    if val < min_val: val = min_val
    if val > max_val: val = max_val

    ratio = (val - min_val) / (max_val - min_val)

    r = int(start_rgb[0] + ratio * (end_rgb[0] - start_rgb[0]))
    g = int(start_rgb[1] + ratio * (end_rgb[1] - start_rgb[1]))
    b = int(start_rgb[2] + ratio * (end_rgb[2] - start_rgb[2]))

    return r, g, b


def get_color_style(change):
    """
    根据涨跌幅返回背景色和文字颜色
    逻辑：
    1. 阈值设定为 5% (超过5%颜色不再加深)
    2. 0% 为白色
    3. 随着涨跌幅增加，颜色逐渐向深绿/深红过渡
    """
    threshold = 5.0
    abs_change = abs(change)

    # 颜色定义 (RGB)
    white = (255, 255, 255)

    # 浅色方案 (用于低涨跌幅)
    light_green = (220, 252, 231)  # green-100
    light_red = (254, 226, 226)  # red-100

    # 深色方案 (用于高涨跌幅)
    deep_green = (22, 163, 74)  # green-600
    deep_red = (220, 38, 38)  # red-600

    bg_rgb = white
    text_color = "#1f2937"  # 默认深灰
    pill_bg = "rgba(255,255,255, 0.6)"

    if change >= 0:
        # 上涨
        if abs_change < 0.5:
            bg_rgb = white
        else:
            # 插值：从白色过渡到深绿
            bg_rgb = interpolate_rgb(abs_change, 0, threshold, white, deep_green)

        # 如果涨幅较大，背景深，文字变白
        if abs_change > 2.5:
            text_color = "#ffffff"
            pill_bg = "rgba(255,255,255, 0.25)"
        else:
            text_color = "#14532d"  # dark green text
    else:
        # 下跌
        if abs_change < 0.5:
            bg_rgb = white
        else:
            # 插值：从白色过渡到深红
            bg_rgb = interpolate_rgb(abs_change, 0, threshold, white, deep_red)

        if abs_change > 2.5:
            text_color = "#ffffff"
            pill_bg = "rgba(255,255,255, 0.25)"
        else:
            text_color = "#7f1d1d"  # dark red text

    bg_color_css = f"rgb({bg_rgb[0]}, {bg_rgb[1]}, {bg_rgb[2]})"
    return bg_color_css, text_color, pill_bg


# ===========================
# 4. 数据获取逻辑
# ===========================

def get_market_status():
    tz = pytz.timezone('US/Eastern')
    now = datetime.now(tz)
    current_time = now.time()
    market_open = time(9, 30)
    settlement_time = time(17, 0)
    if market_open <= current_time < settlement_time:
        return 'INTRADAY'
    else:
        return 'POST_MARKET'


def fetch_yfinance_complete(ticker_config):
    global CURRENT_PROXY
    
    ticker = ticker_config['ticker'] if isinstance(ticker_config, dict) else ticker_config
    display_symbol = ticker_config['display'] if isinstance(ticker_config, dict) else ticker
    fixed_name = ticker_config['name_cn'] if isinstance(ticker_config, dict) else None
    fixed_type = ticker_config['type'] if isinstance(ticker_config, dict) else None
    fixed_domain = ticker_config.get('domain') if isinstance(ticker_config, dict) else None

    # Yahoo Finance 符号处理
    yf_ticker = ticker
    if 'BRK.A' in ticker:
        yf_ticker = 'BRK-A'
    elif 'BRK.B' in ticker:
        yf_ticker = 'BRK-B'
    
    print(f"    Fetching {display_symbol} ({yf_ticker})...", end="", flush=True)

    # 代理处理：如果还没有代理，先获取一个
    if not CURRENT_PROXY:
        CURRENT_PROXY = get_proxy()

    try:
        # 关键修改：通过设置环境变量来使用代理，而不是传递 session 对象
        # 这样 yfinance 内部的 curl_cffi session 可以自动读取代理配置
        if CURRENT_PROXY:
            os.environ['HTTP_PROXY'] = CURRENT_PROXY
            os.environ['HTTPS_PROXY'] = CURRENT_PROXY
            os.environ['http_proxy'] = CURRENT_PROXY
            os.environ['https_proxy'] = CURRENT_PROXY
        
        # 不传递 session 参数，让 yfinance 自己处理
        stock = yf.Ticker(yf_ticker)
        
        # 获取 info
        try:
            info = stock.info
        except Exception as e:
            print(f" (Proxy Error: {e}, retrying with new proxy)...", end="")
            # 代理失效，获取新代理
            CURRENT_PROXY = get_proxy()
            if CURRENT_PROXY:
                os.environ['HTTP_PROXY'] = CURRENT_PROXY
                os.environ['HTTPS_PROXY'] = CURRENT_PROXY
                os.environ['http_proxy'] = CURRENT_PROXY
                os.environ['https_proxy'] = CURRENT_PROXY
            
            # 重新实例化 Ticker
            stock = yf.Ticker(yf_ticker)
            info = stock.info

        # 1. 价格与涨跌幅
        # 优先使用 currentPrice, 其次 regularMarketPrice, 最后 previousClose
        current_price = info.get('currentPrice') or info.get('regularMarketPrice') or info.get('previousClose')
        
        # 如果是指数 (如 DX-Y.NYB)，可能字段不同
        if current_price is None and 'regularMarketPrice' in info:
             current_price = info['regularMarketPrice']

        if current_price is None:
            print(" [No Price Data]")
            return None

        current_price = float(current_price)

        # 计算涨跌幅
        previous_close = info.get('previousClose') or info.get('regularMarketPreviousClose')
        daily_change_pct = 0.0
        if previous_close:
            daily_change_pct = ((current_price - previous_close) / previous_close) * 100

        # 2. 市值
        market_cap = info.get('marketCap', 0)
        
        # 3. PE Ratio
        pe_ttm = info.get('trailingPE')
        if pe_ttm is None:
            pe_ttm = info.get('forwardPE') # 如果没有 TTM，尝试 Forward PE

        # 4. 网站与国家
        website = info.get('website', '')
        country = info.get('country', 'US')

        # 5. YTD Calculation (New Logic: Current vs 2025 End)
        ytd_change = 0
        price_2025 = TARGET_2025_PRICES.get(display_symbol)
        if not price_2025: price_2025 = TARGET_2025_PRICES.get(ticker)

        if price_2025 and price_2025 > 0:
            ytd_change = ((current_price - price_2025) / price_2025) * 100

        # 6. 25 YoY Calculation (New Logic: 2025 End vs 2024 End)
        yoy_25_change = 0
        price_2024 = YTD_BASE_PRICES.get(display_symbol)
        if not price_2024: price_2024 = YTD_BASE_PRICES.get(ticker)

        if price_2025 and price_2024 and price_2024 > 0:
            yoy_25_change = ((price_2025 - price_2024) / price_2024) * 100

        print(" [OK]")

        # Domain & Name Processing
        domain = ""
        if fixed_domain:
            domain = fixed_domain
        elif display_symbol in MANUAL_DOMAINS:
            domain = MANUAL_DOMAINS[display_symbol]
        elif ticker in MANUAL_DOMAINS:
            domain = MANUAL_DOMAINS[ticker]
        else:
            if website:
                try:
                    from urllib.parse import urlparse
                    domain = urlparse(website).netloc.replace('www.', '')
                except:
                    pass
            if not domain: domain = f"{ticker}.com".lower()

        if fixed_name:
            name_display = fixed_name
        else:
            name_raw = info.get('shortName') or info.get('longName') or display_symbol
            name_display = name_raw.split(' ')[0] if name_raw else display_symbol
            name_display = name_display.replace(',', '').replace('.', '')
            if len(name_display) > 8: name_display = name_display[:8]

        if fixed_type:
            tag_display = fixed_type
        else:
            tag_display = country if country != 'United States' else 'US'

        return {
            'symbol': display_symbol,
            'name_cn': name_display,
            'price': current_price,
            'daily_change': daily_change_pct,
            'ytd_change': ytd_change,
            'yoy_25_change': yoy_25_change,
            'market_cap': market_cap,
            'pe_ratio': pe_ttm,
            'domain': domain,
            'tag': tag_display
        }

    except Exception as e:
        print(f" [Error: {e}]")
        return None


def get_all_market_data():
    print(f"🚀 开始获取数据 (Yahoo Finance) | YTD基准: 2025年底价格")
    all_groups_data = []
    for group in GROUPS:
        print(f"\n📂 正在处理: {group['title']}...")
        tasks = group.get('manual_config', group.get('tickers'))
        group_results = []
        for task in tasks:
            res = fetch_yfinance_complete(task)
            if res: group_results.append(res)
            time_module.sleep(0.1) # 稍微减少间隔，因为 yfinance 内部有重试

        sort_rule = group.get('sort_rule', 'manual')
        if sort_rule == 'market_cap':
            group_results.sort(key=lambda x: x['market_cap'] if x['market_cap'] else 0, reverse=True)
        elif sort_rule == 'crypto_special':
            top_picks = [x for x in group_results if x['symbol'] in ['IBIT', 'ETHA']]
            others = [x for x in group_results if x['symbol'] not in ['IBIT', 'ETHA']]
            others.sort(key=lambda x: x['market_cap'] if x['market_cap'] else 0, reverse=True)
            group_results = top_picks + others

        all_groups_data.append({'meta': group, 'data': group_results})
    return all_groups_data


# ===========================
# 5. HTML 生成 (UI 修改 + 缓存控制 + 头部信息调整)
# ===========================

def generate_html(groups_data):
    tz = pytz.timezone('US/Eastern')
    current_time_et = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S ET')
    status = get_market_status()
    status_text = "🟢 Market Open" if status == 'INTRADAY' else "🔴 Market Closed"

    # 定义导航栏 HTML 结构
    nav_html = """
    <div class="nav-bar">
        <span class="nav-icon">👉</span>
        <a href="https://efinmap.com">US</a>
        <span class="nav-sep">|</span>
        <a href="https://efinmap.com/hk.html">HK</a>
        <span class="nav-sep">|</span>
        <a href="https://efinmap.com/asia.html">JP/KR/TW</a>
    </div>
    """

    # CSS 重点修改：Grid 3列，极小的 Padding 和 Font Size
    css_styles = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
        :root { --bg-color: #f3f4f6; }
        body { font-family: 'Inter', sans-serif; background-color: var(--bg-color); margin: 0; padding: 20px 10px; color: #1f2937; }
        .container { max-width: 1000px; margin: 0 auto; padding-bottom: 40px; }

        /* Header Compact */
        .main-header { text-align: center; margin-bottom: 20px; }
        .main-header h1 { font-size: 24px; font-weight: 800; color: #111; margin-bottom: 5px; }
        .main-header p { color: #6b7280; font-size: 11px; margin: 0; }
        .status-badge { display: inline-block; padding: 2px 8px; border-radius: 12px; font-size: 10px; font-weight: 700; margin-top: 5px; }
        .status-open { background: #d1fae5; color: #065f46; }
        .status-closed { background: #fee2e2; color: #991b1b; }

        /* 刷新按钮样式 */
        .refresh-btn {
            display: inline-block;
            margin-top: 10px;
            padding: 6px 16px;
            background-color: #f3f4f6;
            color: #374151;
            border: 1px solid #d1d5db;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
            text-decoration: none;
            transition: all 0.2s;
            -webkit-tap-highlight-color: transparent;
        }
        .refresh-btn:active { background-color: #e5e7eb; transform: scale(0.98); }

        /* 导航栏样式 */
        .nav-bar {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 15px;
            padding: 12px 0;
            margin: 15px 0;
            border-top: 1px solid #e5e7eb;
            border-bottom: 1px solid #e5e7eb;
            font-size: 14px;
            font-weight: 600;
            color: #4b5563;
        }
        .nav-bar a {
            text-decoration: none;
            color: #1f2937;
            transition: color 0.2s;
        }
        .nav-bar a:hover {
            color: #2563eb;
        }
        .nav-icon {
            font-size: 16px;
        }
        .nav-sep {
            color: #d1d5db;
            font-weight: 400;
        }

        /* Section */
        .section-card { background: #fff; border-radius: 16px; padding: 15px 10px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
        .section-title { font-size: 16px; font-weight: 800; margin-bottom: 15px; color: #111827; border-left: 4px solid #f59e0b; padding-left: 10px; }

        /* GRID LAYOUT: 强制3列，间距极小 */
        .grid { 
            display: grid; 
            grid-template-columns: repeat(3, 1fr); 
            gap: 6px; 
            width: 100%;
        }

        /* CARD DESIGN: 紧凑型 */
        .asset-card { 
            border-radius: 12px; 
            padding: 10px 4px; 
            position: relative; 
            display: flex; 
            flex-direction: column; 
            align-items: center; 
            min-height: 185px; /* 增加高度以容纳新的一行 */
            justify-content: space-between; 
            transition: transform 0.2s; 
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
            border: 1px solid rgba(0,0,0,0.03);
        }

        /* Badges: 极小字体 */
        .market-cap-badge { position: absolute; top: 4px; left: 4px; font-size: 8px; font-weight: 700; background: rgba(255,255,255,0.7); padding: 1px 4px; border-radius: 4px; color: #374151; z-index: 2; }
        .type-badge { position: absolute; top: 4px; right: 4px; font-size: 8px; font-weight: 600; opacity: 0.5; letter-spacing: 0.5px; }

        /* Icon & Title */
        .card-header { display: flex; flex-direction: column; align-items: center; margin-bottom: 5px; width: 100%; margin-top: 12px; }
        .logo-wrapper { width: 32px; height: 32px; border-radius: 50%; background: white; padding: 2px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); margin-bottom: 4px; display: flex; align-items: center; justify-content: center; overflow: hidden; }
        .logo-img { width: 100%; height: 100%; object-fit: contain; border-radius: 50%; }

        .ticker-symbol { font-size: 15px; font-weight: 900; line-height: 1.1; margin-bottom: 0px; color: inherit; }
        .ticker-name { font-size: 9px; opacity: 0.8; font-weight: 600; text-align: center; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 95%; margin-bottom: 4px; }

        /* Data Pills: 极紧凑 */
        .data-pills-container { width: 96%; display: flex; flex-direction: column; gap: 4px; margin-bottom: 2px; }
        .data-pill { 
            border-radius: 6px; 
            padding: 3px 0; 
            text-align: center; 
            font-size: 11px; /* 字体调小 */
            font-weight: 800; 
            width: 100%; 
            line-height: 1.2;
        }
        .pill-label { font-size: 8px; font-weight: 500; opacity: 0.7; margin-right: 2px; }

        /* Footer PE */
        .card-footer-pe { width: 100%; text-align: center; font-size: 9px; font-weight: 600; opacity: 0.6; margin-top: 4px; padding-top: 2px; border-top: 1px solid rgba(0,0,0,0.05); }

        /* Stats Footer */
        .stats-footer { margin-top: 15px; background: #f9fafb; border-radius: 12px; padding: 10px; display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; }
        .stat-item { display: flex; flex-direction: column; align-items: center; justify-content: center; background: #fff; padding: 8px; border-radius: 8px; box-shadow: 0 1px 2px rgba(0,0,0,0.02); }
        .stat-title { font-size: 9px; color: #9ca3af; margin-bottom: 2px; text-transform: uppercase; }
        .stat-value { font-size: 13px; font-weight: 800; color: #111; }

        /* PC端适配 (可选，如果在大屏看可以变成6列) */
        @media (min-width: 768px) { 
            .grid { grid-template-columns: repeat(6, 1fr); gap: 10px; } 
            .asset-card { min-height: 200px; }
        }
    </style>
    """

    status_class = "status-open" if status == 'INTRADAY' else "status-closed"

    html_content = f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="default">
        <meta name="apple-mobile-web-app-title" content="US Market">
        
        <!-- 1. 禁止缓存 Meta 标签 -->
        <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
        <meta http-equiv="Pragma" content="no-cache" />
        <meta http-equiv="Expires" content="0" />
        
        <title>efinmap</title>
        {css_styles}
    </head>
    <body>
        <div class="container">
            <div class="main-header">
                <h1>US Market Watch</h1>
                <p>{current_time_et}</p>
                
                <!-- 移动到这里的数据来源和邮箱信息 -->
                <div class="header-info" style="font-size: 10px; color: #6b7280; margin: 4px 0 8px 0;">
                    <div>Data: Yahoo Finance (15m update)</div>
                    <div><a href="mailto:jasonlee325@gmail.com" style="color: inherit; text-decoration: none;">jasonlee325@gmail.com</a></div>
                </div>               
            </div>
            {nav_html}
    """

    for group in groups_data:
        meta = group['meta']
        data_list = group['data']
        if not data_list: continue

        total_assets = len(data_list)
        up_assets = sum(1 for x in data_list if x['daily_change'] >= 0)
        avg_change = np.mean([x['daily_change'] for x in data_list])
        best_performer = max(data_list, key=lambda x: x['daily_change'])
        best_ytd = max(data_list, key=lambda x: x['ytd_change'])

        html_content += f"""
            <div class="section-card">
                <div class="section-title">{meta['title']}</div>
                <div class="grid">
        """

        for item in data_list:
            # 获取动态颜色
            bg_color, text_color, pill_bg = get_color_style(item['daily_change'])

            # YTD 颜色逻辑 (如果是深色背景，YTD也需要反白)
            ytd_val = item['ytd_change']
            if text_color == "#ffffff":
                ytd_text_color = "#ffffff"
            else:
                # 浅色背景下，YTD 保持红绿区分
                ytd_text_color = '#15803d' if ytd_val >= 0 else '#b91c1c'

            # 25 YoY 颜色逻辑
            yoy_val = item['yoy_25_change']
            if text_color == "#ffffff":
                yoy_text_color = "#ffffff"
            else:
                yoy_text_color = '#15803d' if yoy_val >= 0 else '#b91c1c'

            # 价格格式化
            price = item['price']
            
            # 特殊处理：SPX, IXIC, DJI, RUT
            # 不显示美元符号，不使用k单位，保留一位小数
            if item['symbol'] in ['SPX', 'IXIC', 'DJI', 'RUT']:
                price_fmt = f"{price:.1f}"
            else:
                if price < 10:
                    price_fmt = f"${price:.2f}"
                elif price > 20000:
                    price_fmt = f"${price / 1000:.0f}k"  # 缩短 BRK.A 显示
                else:
                    price_fmt = f"${price:.1f}"  # 减少小数位

            # 市值格式化
            mkt_cap_str = ""
            if item['market_cap'] and item['market_cap'] > 0:
                # 原始 market_cap 单位是“元” (USD)
                val_trillion = item['market_cap'] / 1_000_000_000_000
                val_billion = item['market_cap'] / 1_000_000_000

                if val_trillion >= 1.0:
                    # 大于1万亿，显示 T，保留1位小数 (e.g., 3.4T)
                    mkt_cap_str = f"{val_trillion:.1f}T"
                elif val_billion >= 1.0:
                    # 大于10亿，显示 B，保留0位小数 (e.g., 348B) 或者 1位小数
                    # 为了节省空间，如果超过100B通常不看小数，但为了精确，这里统一保留1位小数或取整
                    # 根据您的反馈 AMD 347.5B，我们这里保留1位小数更准确
                    mkt_cap_str = f"{val_billion:.1f}B"
                else:
                    # 小于10亿 (百万级)，显示 M
                    val_million = item['market_cap'] / 1_000_000
                    mkt_cap_str = f"{val_million:.0f}M"

            # PE 格式化
            pe_str = "PE --"
            if item['pe_ratio'] and item['pe_ratio'] > 0:
                pe_str = f"PE {item['pe_ratio']:.0f}"  # 去掉小数位

            logo_url = f"https://www.google.com/s2/favicons?domain={item['domain']}&sz=128"

            # 获取 Yahoo Finance URL
            ticker_symbol = item['symbol']
            yahoo_url = TICKER_URL_MAP.get(ticker_symbol, '')
            card_link = f'<a href="{yahoo_url}" target="_blank" style="text-decoration: none; color: inherit;">' if yahoo_url else ''

            html_content += f"""
                {card_link}<div class="asset-card" style="background-color: {bg_color}; color: {text_color};">
                    <div class="market-cap-badge">{mkt_cap_str}</div>
                    <div class="type-badge" style="color:{text_color}">{item['tag']}</div>
                    <div class="card-header">
                        <div class="logo-wrapper">
                            <img class="logo-img" src="{logo_url}" onerror="this.style.display='none';">
                        </div>
                        <div class="ticker-symbol">{item['symbol']}</div>
                        <div class="ticker-name">{item['name_cn']}</div>
                    </div>
                    <div class="data-pills-container">
                        <div class="data-pill" style="background: {pill_bg}; color: {text_color}; opacity: 0.9;">{price_fmt}</div>
                        <div class="data-pill" style="background: {pill_bg}; color: {text_color};">
                            {'+' if item['daily_change'] >= 0 else ''}{item['daily_change']:.2f}%
                        </div>
                        <div class="data-pill" style="background: {pill_bg}; color: {ytd_text_color}; font-size: 9px;">
                            <span class="pill-label">YTD</span>{'+' if ytd_val >= 0 else ''}{ytd_val:.1f}%
                        </div>
                        <div class="data-pill" style="background: {pill_bg}; color: {yoy_text_color}; font-size: 9px;">
                            <span class="pill-label">25 YoY</span>{'+' if yoy_val >= 0 else ''}{yoy_val:.1f}%
                        </div>
                    </div>
                    <div class="card-footer-pe" style="border-color: {text_color}20">{pe_str}</div>
                </div>{"</a>" if yahoo_url else ""}
            """
        html_content += f"""
                </div>
                <div class="stats-footer">
                    <div class="stat-item"><span class="stat-title">上涨</span><span class="stat-value">{up_assets}/{total_assets}</span></div>
                    <div class="stat-item"><span class="stat-title">平均</span><span class="stat-value" style="color: {'#059669' if avg_change >= 0 else '#dc2626'}">{avg_change:+.2f}%</span></div>
                    <div class="stat-item"><span class="stat-title">今日最佳</span><span class="stat-value" style="color: #059669; font-size: 11px;">{best_performer['symbol']} {best_performer['daily_change']:+.1f}%</span></div>
                    <div class="stat-item"><span class="stat-title">YTD 最佳</span><span class="stat-value" style="color: #059669; font-size: 11px;">{best_ytd['symbol']} {best_ytd['ytd_change']:+.1f}%</span></div>
                </div>
            </div>
        """
    
    # 2. & 3. 增加 JavaScript 处理自动刷新和 URL 时间戳欺骗
    html_content += f"""
            {nav_html}
        </div>
        <script>
            // 强制刷新函数：通过添加时间戳参数绕过缓存
            function forceReload() {{
                var url = window.location.href.split('?')[0];
                var timestamp = new Date().getTime();
                // 使用 replace 而不是 assign，避免产生历史记录
                window.location.replace(url + '?t=' + timestamp);
            }}

            // 自动检测：当页面重新可见时（从后台切回）
            var lastLoadTime = new Date().getTime();
            
            document.addEventListener('visibilitychange', function() {{
                if (document.visibilityState === 'visible') {{
                    var currentTime = new Date().getTime();
                    // 600000 ms = 10 minutes
                    // 如果距离上次加载超过 10 分钟，则自动刷新
                    if (currentTime - lastLoadTime > 600000) {{
                        console.log("Page stale, reloading...");
                        forceReload();
                    }}
                }}
            }});
        </script>
    </body>
    </html>
    """
    return html_content


if __name__ == "__main__":
    data = get_all_market_data()
    html = generate_html(data)
    filename = "/www/wwwroot/efinmap.com/index.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"\n✨ 成功! 手机端适配 HTML 已生成: {os.path.abspath(filename)}")