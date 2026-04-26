"""
One-time seed script: import ticker metadata and annual benchmarks from
the existing cloudedition.py / hkmap.py / eastasian.py configs into PostgreSQL.

Run once on the server after init_db.sql:
    python deploy/seed_data.py
"""
import os
import sys
import psycopg
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://efinmap_user:yourpassword@localhost:5432/efinmap")

# =============================================
# US: Annual benchmarks (from cloudedition.py)
# =============================================
YTD_BASE_PRICES_2024 = {
    'AAPL': 249.29, 'ABBV': 171.70, 'ABNB': 131.41, 'AMD': 120.79, 'AMZN': 219.39,
    'AVGO': 230.20, 'AXP': 293.63, 'AZO': 3202.00, 'BA': 177.00, 'BABA': 83.38,
    'BAC': 42.96, 'BEKE': 18.04, 'BIDU': 84.31, 'BKNG': 4931.77, 'BLK': 1004.52,
    'BRK.A': 680920.00, 'BSX': 89.32, 'BUD': 49.22, 'CAT': 357.36, 'CLSK': 9.21,
    'CMG': 60.30, 'COIN': 248.30, 'COST': 911.51, 'CRCL': 31.00, 'CRSP': 39.36,
    'CVX': 138.42, 'DASH': 167.75, 'DHR': 228.43, 'DIA': 419.87, 'EL': 73.68,
    'EMR': 121.85, 'ETHA': 25.29, 'ETN': 328.55, 'FUTU': 79.99, 'GE': 166.03,
    'GLD': 242.13, 'GOOGL': 188.56, 'GS': 561.17, 'HD': 379.53, 'HIMS': 24.18,
    'HON': 208.35, 'HOOD': 37.26, 'HSY': 163.97, 'IBIT': 53.05, 'IBKR': 43.94,
    'INTC': 20.05, 'ISRG': 521.96, 'IWM': 218.50, 'JD': 33.68, 'JNJ': 140.32,
    'JPM': 234.74, 'KHC': 28.98, 'KO': 60.48, 'LI': 23.99, 'LIN': 413.11,
    'LLY': 766.28, 'LMT': 472.03, 'LOW': 241.95, 'LULU': 382.41, 'MA': 523.56,
    'MAGS': 54.42, 'MARA': 16.77, 'MCD': 283.28, 'MDLZ': 58.43, 'META': 583.67,
    'MMM': 126.70, 'MNST': 52.56, 'MS': 122.30, 'MSFT': 418.41, 'MSTR': 289.62,
    'MU': 83.92, 'NEE': 69.52, 'NFLX': 89.13, 'NKE': 73.93, 'NTES': 86.95,
    'NVDA': 134.25, 'NVO': 83.71, 'ORCL': 165.00, 'PDD': 96.99, 'PEP': 146.22,
    'PG': 163.33, 'PLTR': 75.63, 'PM': 117.30, 'QQQ': 509.31, 'REGN': 708.40,
    'RIOT': 10.21, 'RTX': 113.60, 'SBUX': 88.89, 'SCHW': 73.11, 'SHEL': 60.15,
    'SHW': 336.93, 'SO': 79.65, 'SPY': 580.99, 'T': 21.79, 'TCOM': 68.33,
    'TJX': 119.33, 'TLH': 95.84, 'TME': 11.21, 'TMO': 518.40, 'TMUS': 217.34,
    'TSLA': 403.84, 'TSM': 194.86, 'TWST': 46.47, 'UBER': 60.32, 'UNH': 493.70,
    'UNP': 222.73, 'UPS': 117.99, 'USO': 75.55, 'V': 313.81, 'VZ': 37.41,
    'WFC': 68.75, 'WM': 198.83, 'WMT': 89.49, 'XOM': 103.76, 'XPEV': 11.82,
    'YMM': 10.73, 'TLT': 95.84, 'DXY': 106.0, 'SPX': 5881.63, 'IXIC': 19310.79,
    'DJI': 42544.22, 'RUT': 2230.16, 'USDJPY': 157.30, 'CPER': 25.0,
}

TARGET_2025_PRICES = {
    'AAPL': 271.86, 'ABBV': 228.49, 'ABNB': 135.72, 'AMD': 214.16, 'AMZN': 230.82,
    'AVGO': 346.10, 'AXP': 369.13, 'AZO': 3391.50, 'BA': 217.12, 'BABA': 146.58,
    'BAC': 55.00, 'BEKE': 15.76, 'BIDU': 130.66, 'BKNG': 5355.33, 'BLK': 1070.34,
    'BRK.A': 754800.00, 'BSX': 95.35, 'BUD': 64.04, 'CAT': 572.87, 'CLSK': 10.12,
    'CMG': 37.00, 'COIN': 226.14, 'COST': 862.34, 'CRCL': 79.30, 'CRSP': 52.44,
    'CVX': 152.41, 'DASH': 226.48, 'DHR': 228.92, 'DIA': 480.57, 'EL': 104.72,
    'EMR': 132.72, 'ETHA': 22.43, 'ETN': 318.51, 'FUTU': 164.21, 'GE': 308.03,
    'GLD': 396.31, 'GOOGL': 313.00, 'GS': 879.00, 'HD': 344.10, 'HIMS': 32.47,
    'HON': 195.09, 'HOOD': 113.10, 'HSY': 181.98, 'IBIT': 49.65, 'IBKR': 64.31,
    'INTC': 36.90, 'ISRG': 566.36, 'IWM': 246.16, 'JD': 28.70, 'JNJ': 206.95,
    'JPM': 322.22, 'KHC': 24.25, 'KO': 69.91, 'LI': 16.93, 'LIN': 426.39,
    'LLY': 1074.68, 'LMT': 483.67, 'LOW': 241.16, 'LULU': 207.81, 'MA': 570.88,
    'MAGS': 65.96, 'MARA': 8.98, 'MCD': 305.63, 'MDLZ': 53.83, 'META': 660.09,
    'MMM': 160.10, 'MNST': 76.67, 'MS': 177.53, 'MSFT': 483.62, 'MSTR': 151.95,
    'MU': 285.41, 'NEE': 80.28, 'NFLX': 93.76, 'NKE': 63.71, 'NTES': 137.62,
    'NVDA': 186.50, 'NVO': 50.88, 'ORCL': 194.91, 'PDD': 113.39, 'PEP': 143.52,
    'PG': 143.31, 'PLTR': 177.75, 'PM': 160.40, 'QQQ': 614.31, 'REGN': 771.87,
    'RIOT': 12.67, 'RTX': 183.40, 'SBUX': 84.21, 'SCHW': 99.91, 'SHEL': 73.48,
    'SHW': 324.03, 'SO': 87.20, 'SPY': 681.92, 'T': 24.84, 'TCOM': 71.91,
    'TJX': 153.61, 'TLH': 101.67, 'TME': 17.53, 'TMO': 579.45, 'TMUS': 203.04,
    'TSLA': 449.72, 'TSM': 303.89, 'TWST': 31.72, 'UBER': 81.71, 'UNH': 330.11,
    'UNP': 231.32, 'UPS': 99.19, 'USO': 69.16, 'V': 350.71, 'VZ': 40.73,
    'WFC': 93.20, 'WM': 219.71, 'WMT': 111.41, 'XOM': 120.34, 'XPEV': 20.28,
    'YMM': 10.73, 'TLT': 87.16, 'DXY': 98.28, 'SPX': 6845.50, 'IXIC': 23241.99,
    'DJI': 48063.29, 'RUT': 2481.91, 'USDJPY': 156.90, 'CPER': 28.0,
}

# =============================================
# US Ticker metadata
# =============================================
US_TICKERS = [
    # symbol, name_cn, name_en, domain, tag_type
    ('SPX',   '标普500',   'S&P 500',          'spglobal.com',         'Index'),
    ('IXIC',  '纳斯达克',  'NASDAQ',           'nasdaq.com',           'Index'),
    ('DJI',   '道琼斯',    'Dow Jones',        'dowjones.com',         'Index'),
    ('RUT',   '罗素2000',  'Russell 2000',     'ftserussell.com',      'Index'),
    ('MAGS',  '七姐妹',    'MAG7 ETF',         'roundhillinvestments.com','ETF'),
    ('IBIT',  '比特币ETF', 'iShares Bitcoin',  'ishares.com',          'ETF'),
    ('GLD',   '黄金',      'SPDR Gold',        'spdrgoldshares.com',   'ETF'),
    ('USO',   '原油',      'US Oil Fund',      'uscfinvestments.com',  'ETF'),
    ('CPER',  '铜',        'US Copper Index',  'uscfinvestments.com',  'ETF'),
    ('TLT',   '20年美债',  'iShares 20Y Tsy',  'ishares.com',          'ETF'),
    ('DXY',   '美元指数',  'US Dollar Index',  'theice.com',           'INDEX'),
    ('USDJPY','日元汇率',  'USD/JPY',          'boj.or.jp',            'Forex'),
    ('AAPL',  'Apple',     'Apple Inc',        'apple.com',            'US'),
    ('NVDA',  '英伟达',    'NVIDIA',           'nvidia.com',           'US'),
    ('META',  'Meta',      'Meta Platforms',   'meta.com',             'US'),
    ('GOOGL', '谷歌',      'Alphabet',         'google.com',           'US'),
    ('MSFT',  '微软',      'Microsoft',        'microsoft.com',        'US'),
    ('AMZN',  '亚马逊',    'Amazon',           'amazon.com',           'US'),
    ('AVGO',  '博通',      'Broadcom',         'broadcom.com',         'US'),
    ('TSM',   '台积电',    'TSMC',             'tsmc.com',             'US'),
    ('TSLA',  '特斯拉',    'Tesla',            'tesla.com',            'US'),
    ('ORCL',  '甲骨文',    'Oracle',           'oracle.com',           'US'),
    ('NFLX',  '奈飞',      'Netflix',          'netflix.com',          'US'),
    ('PLTR',  '博睿',      'Palantir',         'palantir.com',         'US'),
    ('AMD',   'AMD',       'AMD',              'amd.com',              'US'),
    ('MU',    '美光',      'Micron',           'micron.com',           'US'),
    ('INTC',  '英特尔',    'Intel',            'intel.com',            'US'),
    ('ETHA',  '以太坊ETF', 'iShares Ethereum', 'ishares.com',          'ETF'),
    ('HOOD',  'Robinhood', 'Robinhood',        'robinhood.com',        'US'),
    ('COIN',  'Coinbase',  'Coinbase',         'coinbase.com',         'US'),
    ('MSTR',  'MicroStrategy','MicroStrategy', 'microstrategy.com',    'US'),
    ('CRCL',  'Circle',    'Circle',           'circle.com',           'US'),
    ('RIOT',  'Riot Platforms','Riot Platforms','riotplatforms.com',   'US'),
    ('MARA',  'MARA',      'MARA Holdings',    'mara.com',             'US'),
    ('CLSK',  'CleanSpark','CleanSpark',       'cleanspark.com',       'US'),
    ('BABA',  '阿里巴巴',  'Alibaba',          'alibaba.com',          'CN'),
    ('PDD',   '拼多多',    'PDD Holdings',     'pinduoduo.com',        'CN'),
    ('NTES',  '网易',      'NetEase',          'netease.com',          'CN'),
    ('JD',    '京东',      'JD.com',           'jd.com',               'CN'),
    ('TCOM',  '携程',      'Trip.com',         'trip.com',             'CN'),
    ('LI',    '理想汽车',  'Li Auto',          'lixiang.com',          'CN'),
    ('TME',   '腾讯音乐',  'Tencent Music',    'tencentmusic.com',     'CN'),
    ('BIDU',  '百度',      'Baidu',            'baidu.com',            'CN'),
    ('BEKE',  '贝壳',      'KE Holdings',      'ke.com',               'CN'),
    ('FUTU',  '富途',      'Futu Holdings',    'futuhk.com',           'CN'),
    ('XPEV',  '小鹏',      'XPeng',            'xiaopeng.com',         'CN'),
    ('YMM',   '运满满',    'Full Truck',       'fulltruckalliance.com','CN'),
    ('LLY',   '礼来',      'Eli Lilly',        'lilly.com',            'US'),
    ('JNJ',   'J&J',       'Johnson & Johnson','jnj.com',              'US'),
    ('ABBV',  '艾伯维',    'AbbVie',           'abbvie.com',           'US'),
    ('NVO',   '诺和诺德',  'Novo Nordisk',     'novonordisk.com',      'US'),
    ('UNH',   '联合健康',  'UnitedHealth',     'unitedhealthgroup.com','US'),
    ('TMO',   '赛默飞',    'Thermo Fisher',    'thermofisher.com',     'US'),
    ('ISRG',  '直觉外科',  'Intuitive Surgical','intuitive.com',       'US'),
    ('BSX',   '波士顿科学','Boston Scientific', 'bostonscientific.com','US'),
    ('REGN',  '再生元',    'Regeneron',        'regeneron.com',        'US'),
    ('HIMS',  'Hims',      'Hims & Hers',      'hims.com',             'US'),
    ('TWST',  'Twist Bio', 'Twist Bioscience', 'twistbioscience.com',  'US'),
    ('CRSP',  'CRISPR',    'CRISPR Therapeutics','crisprtx.com',       'US'),
    ('WMT',   '沃尔玛',    'Walmart',          'walmart.com',          'US'),
    ('COST',  '好市多',    'Costco',           'costco.com',           'US'),
    ('HD',    '家得宝',    'Home Depot',       'homedepot.com',        'US'),
    ('MCD',   '麦当劳',    "McDonald's",       'mcdonalds.com',        'US'),
    ('BKNG',  'Booking',   'Booking Holdings', 'booking.com',          'US'),
    ('TJX',   'TJX',       'TJX Companies',    'tjx.com',              'US'),
    ('LOW',   'Lowe\'s',   'Lowe\'s',          'lowes.com',            'US'),
    ('SBUX',  '星巴克',    'Starbucks',        'starbucks.com',        'US'),
    ('DASH',  'DoorDash',  'DoorDash',         'doordash.com',         'US'),
    ('ABNB',  'Airbnb',    'Airbnb',           'airbnb.com',           'US'),
    ('CMG',   '墨西哥烤鸡','Chipotle',         'chipotle.com',         'US'),
    ('AZO',   'AutoZone',  'AutoZone',         'autozone.com',         'US'),
    ('PG',    '宝洁',      'Procter & Gamble', 'pg.com',               'US'),
    ('KO',    '可口可乐',  'Coca-Cola',        'coca-cola.com',        'US'),
    ('PM',    '菲利普莫里斯','Philip Morris',   'pmi.com',              'US'),
    ('PEP',   '百事可乐',  'PepsiCo',          'pepsico.com',          'US'),
    ('BUD',   '百威',      'AB InBev',         'ab-inbev.com',         'US'),
    ('NKE',   '耐克',      'Nike',             'nike.com',             'US'),
    ('MDLZ',  '亿滋',      'Mondelez',         'mondelezinternational.com','US'),
    ('MNST',  '魔爪',      'Monster Beverage', 'monsterbevcorp.com',   'US'),
    ('KHC',   '卡夫亨氏',  'Kraft Heinz',      'kraftheinz.com',       'US'),
    ('HSY',   '好时',      'Hershey',          'thehersheycompany.com','US'),
    ('EL',    '雅诗兰黛',  'Estee Lauder',     'esteelauder.com',      'US'),
    ('LULU',  '露露柠檬',  'Lululemon',        'lululemon.com',        'US'),
    ('GE',    '通用电气',  'GE Aerospace',     'geaerospace.com',      'US'),
    ('LIN',   '林德',      'Linde',            'linde.com',            'US'),
    ('RTX',   '雷神',      'RTX Corp',         'rtx.com',              'US'),
    ('CAT',   '卡特彼勒',  'Caterpillar',      'cat.com',              'US'),
    ('BA',    '波音',      'Boeing',           'boeing.com',           'US'),
    ('HON',   '霍尼韦尔',  'Honeywell',        'honeywell.com',        'US'),
    ('ETN',   '伊顿',      'Eaton',            'eaton.com',            'US'),
    ('DHR',   '丹纳赫',    'Danaher',          'danaher.com',          'US'),
    ('LMT',   '洛克希德',  'Lockheed Martin',  'lockheedmartin.com',   'US'),
    ('MMM',   '3M',        '3M Company',       '3m.com',               'US'),
    ('SHW',   '宣伟',      'Sherwin-Williams',  'sherwin.com',         'US'),
    ('EMR',   '艾默生',    'Emerson Electric', 'emerson.com',          'US'),
    ('XOM',   '埃克森',    'ExxonMobil',       'exxonmobil.com',       'US'),
    ('CVX',   '雪佛龙',    'Chevron',          'chevron.com',          'US'),
    ('TMUS',  'T-Mobile',  'T-Mobile',         'tmobile.com',          'US'),
    ('SHEL',  '壳牌',      'Shell',            'shell.com',            'US'),
    ('T',     'AT&T',      'AT&T',             'att.com',              'US'),
    ('UBER',  'Uber',      'Uber',             'uber.com',             'US'),
    ('VZ',    '威瑞森',    'Verizon',          'verizon.com',          'US'),
    ('NEE',   '新能源',    'NextEra Energy',   'nexteraenergy.com',    'US'),
    ('UNP',   '联合太平洋','Union Pacific',    'up.com',               'US'),
    ('SO',    '南方公司',  'Southern Company', 'southerncompany.com',  'US'),
    ('WM',    '废物管理',  'Waste Management', 'wm.com',               'US'),
    ('UPS',   '联合包裹',  'UPS',              'ups.com',              'US'),
    ('BRK.A', '伯克希尔',  'Berkshire Hathaway','berkshirehathaway.com','US'),
    ('JPM',   '摩根大通',  'JPMorgan Chase',   'jpmorganchase.com',    'US'),
    ('V',     'Visa',      'Visa',             'visa.com',             'US'),
    ('MA',    '万事达',    'Mastercard',       'mastercard.com',       'US'),
    ('BAC',   '美国银行',  'Bank of America',  'bankofamerica.com',    'US'),
    ('WFC',   '富国银行',  'Wells Fargo',      'wellsfargo.com',       'US'),
    ('MS',    '摩根士丹利','Morgan Stanley',   'morganstanley.com',    'US'),
    ('GS',    '高盛',      'Goldman Sachs',    'goldmansachs.com',     'US'),
    ('AXP',   '美国运通',  'American Express', 'americanexpress.com',  'US'),
    ('SCHW',  '嘉信理财',  'Charles Schwab',   'schwab.com',           'US'),
    ('BLK',   '贝莱德',    'BlackRock',        'blackrock.com',        'US'),
    ('IBKR',  '盈透证券',  'Interactive Brokers','interactivebrokers.com','US'),
    ('SPY',   'SPY ETF',   'SPDR S&P 500',     'spglobal.com',         'ETF'),
    ('QQQ',   'QQQ ETF',   'Invesco QQQ',      'invesco.com',          'ETF'),
    ('IWM',   'IWM ETF',   'iShares Russell',  'ishares.com',          'ETF'),
    ('DIA',   'DIA ETF',   'SPDR Dow Jones',   'spdrs.com',            'ETF'),
    ('TLH',   'TLH ETF',   'iShares 10-20Y',   'ishares.com',          'ETF'),
]

# =============================================
# HK: 2024 and 2025 benchmarks
# =============================================
HK_PRICES_2024 = {
    '0001.HK': 39.5578,  '0005.HK': 71.7606,  '0006.HK': 51.2827,  '0016.HK': 71.6159,
    '0020.HK': 1.4900,   '0066.HK': 25.8285,  '0101.HK': 5.7574,   '0135.HK': 8.0243,
    '0175.HK': 14.5409,  '0179.HK': 10.6501,  '0189.HK': 8.0326,   '0241.HK': 3.3200,
    '0257.HK': 3.6600,   '0267.HK': 8.7331,   '0285.HK': 41.2527,  '0291.HK': 24.3977,
    '0371.HK': 2.3567,   '0388.HK': 286.8313, '0425.HK': 14.8061,  '0522.HK': 74.1891,
    '0551.HK': 15.5794,  '0669.HK': 99.9402,  '0688.HK': 11.9340,  '0700.HK': 413.3913,
    '0728.HK': 4.6337,   '0762.HK': 7.0259,   '0772.HK': 25.2000,  '0788.HK': 10.1192,
    '0836.HK': 17.9231,  '0883.HK': 17.7841,  '0939.HK': 5.9098,   '0941.HK': 72.1725,
    '0960.HK': 9.6647,   '0968.HK': 3.0995,   '0981.HK': 31.8000,  '0992.HK': 9.7029,
    '1024.HK': 41.0798,  '1093.HK': 4.6477,   '1109.HK': 21.3822,  '1171.HK': 8.2137,
    '1177.HK': 3.1563,   '1208.HK': 2.5600,   '1209.HK': 27.2512,  '1211.HK': 87.8953,
    '1299.HK': 54.7934,  '1308.HK': 18.5210,  '1347.HK': 21.6500,  '1357.HK': 2.8637,
    '1378.HK': 10.9760,  '1398.HK': 4.7902,   '1519.HK': 6.1300,   '1530.HK': 6.0315,
    '1548.HK': 9.8400,   '1585.HK': 12.4786,  '1788.HK': 1.0899,   '1801.HK': 36.6000,
    '1810.HK': 34.5000,  '1816.HK': 2.7375,   '1818.HK': 10.9313,  '1888.HK': 6.7637,
    '1918.HK': 2.3200,   '1951.HK': 2.6900,   '2007.HK': 0.4850,   '2018.HK': 37.2632,
    '2020.HK': 75.7687,  '2057.HK': 145.9905, '2097.HK': 202.5000, '2228.HK': 5.9800,
    '2269.HK': 17.5600,  '2313.HK': 59.2075,  '2318.HK': 43.6123,  '2319.HK': 17.0034,
    '2328.HK': 11.8021,  '2331.HK': 15.8962,  '2367.HK': 48.7764,  '2382.HK': 68.2446,
    '2400.HK': 24.8832,  '2498.HK': 30.7000,  '2577.HK': 31.2500,  '2588.HK': 57.4167,
    '2602.HK': 18.7612,  '2618.HK': 12.8000,  '2628.HK': 14.1252,  '2688.HK': 53.2811,
    '2899.HK': 13.7791,  '3360.HK': 5.2159,   '3690.HK': 151.7000, '3692.HK': 17.0889,
    '3931.HK': 12.8600,  '6082.HK': 0.0,      '6181.HK': 235.3051, '6618.HK': 28.1000,
    '6862.HK': 15.0159,  '6969.HK': 13.1256,  '9626.HK': 142.0000, '9633.HK': 33.2278,
    '9660.HK': 3.6000,   '9863.HK': 32.5500,  '9926.HK': 60.7000,  '9956.HK': 7.8240,
    '9979.HK': 2.9276,   '9985.HK': 6.9407,   '9987.HK': 366.4606, '9988.HK': 81.0392,
    '9992.HK': 89.2825,  '9995.HK': 14.4000,  '3887.HK': 0.0,      '0100.HK': 0.0,
}

HK_PRICES_2025 = {
    '0001.HK': 52.80,   '0005.HK': 122.20,  '0006.HK': 55.25,   '0016.HK': 94.35,
    '0020.HK': 2.20,    '0066.HK': 29.72,   '0101.HK': 8.58,    '0135.HK': 7.38,
    '0175.HK': 17.94,   '0179.HK': 29.74,   '0189.HK': 10.84,   '0241.HK': 5.06,
    '0257.HK': 4.82,    '0267.HK': 12.06,   '0285.HK': 33.64,   '0291.HK': 26.22,
    '0371.HK': 2.46,    '0388.HK': 407.80,  '0425.HK': 31.72,   '0522.HK': 77.70,
    '0551.HK': 15.96,   '0669.HK': 89.95,   '0688.HK': 12.25,   '0700.HK': 599.00,
    '0728.HK': 5.40,    '0762.HK': 7.76,    '0772.HK': 32.90,   '0788.HK': 11.56,
    '0836.HK': 17.26,   '0883.HK': 21.28,   '0939.HK': 7.67,    '0941.HK': 81.70,
    '0960.HK': 8.54,    '0968.HK': 2.97,    '0981.HK': 71.35,   '0992.HK': 9.26,
    '1024.HK': 63.75,   '1093.HK': 8.44,    '1109.HK': 27.20,   '1171.HK': 9.60,
    '1177.HK': 6.18,    '1208.HK': 8.81,    '1209.HK': 42.98,   '1211.HK': 95.10,
    '1299.HK': 80.10,   '1308.HK': 27.90,   '1347.HK': 74.10,   '1357.HK': 6.97,
    '1378.HK': 32.54,   '1398.HK': 6.24,    '1519.HK': 10.47,   '1530.HK': 24.26,
    '1548.HK': 12.39,   '1585.HK': 11.32,   '1788.HK': 2.54,    '1801.HK': 76.25,
    '1810.HK': 39.20,   '1816.HK': 2.93,    '1818.HK': 30.66,   '1888.HK': 13.18,
    '1918.HK': 1.31,    '1951.HK': 2.38,    '2007.HK': 0.415,   '2018.HK': 39.08,
    '2020.HK': 80.30,   '2057.HK': 162.20,  '2097.HK': 410.80,  '2228.HK': 9.46,
    '2269.HK': 31.44,   '2313.HK': 60.95,   '2318.HK': 65.30,   '2319.HK': 14.86,
    '2328.HK': 16.32,   '2331.HK': 18.66,   '2367.HK': 33.14,   '2382.HK': 65.55,
    '2400.HK': 65.25,   '2498.HK': 36.60,   '2577.HK': 78.30,   '2588.HK': 72.65,
    '2602.HK': 18.41,   '2618.HK': 11.42,   '2628.HK': 27.44,   '2688.HK': 68.90,
    '2899.HK': 35.66,   '3360.HK': 8.04,    '3690.HK': 102.80,  '3692.HK': 36.08,
    '3931.HK': 25.10,   '6082.HK': 0.0,     '6181.HK': 618.00,  '6618.HK': 55.55,
    '6862.HK': 14.20,   '6969.HK': 11.85,   '9626.HK': 192.00,  '9633.HK': 46.84,
    '9660.HK': 8.61,    '9863.HK': 48.74,   '9926.HK': 113.10,  '9956.HK': 11.82,
    '9979.HK': 2.77,    '9985.HK': 11.27,   '9987.HK': 368.20,  '9988.HK': 142.60,
    '9992.HK': 189.30,  '9995.HK': 71.85,   '3887.HK': 6.66,    '0100.HK': 165.00,
}

HK_TICKERS = [
    # symbol, name_cn, name_en, domain, tag_type
    ('0700.HK',  '腾讯控股',  'TENCENT',          'tencent.com',              'HK'),
    ('9988.HK',  '阿里巴巴',  'BABA-W',           'taobao.com',               'HK'),
    ('1810.HK',  '小米集团',  'XIAOMI-W',         'mi.com',                   'HK'),
    ('3690.HK',  '美团',      'MEITUAN-W',        'meituan.com',              'HK'),
    ('1024.HK',  '快手',      'KUAISHOU-W',       'kuaishou.com',             'HK'),
    ('9626.HK',  '哔哩哔哩',  'BILIBILI-W',       'bilibili.com',             'HK'),
    ('0981.HK',  '中芯国际',  'SMIC',             'smics.com',                'HK'),
    ('0020.HK',  '商汤',      'SENSETIME-W',      'sensetime.com',            'HK'),
    ('0100.HK',  'MiniMax',   'MiniMax',          'minimax.io',               'HK'),
    ('0772.HK',  '阅文集团',  'CHINA LIT',        'yuewen.com',               'HK'),
    ('1357.HK',  '美图公司',  'MEITU',            'meitu.com',                'HK'),
    ('2400.HK',  '心动公司',  'XD INC',           'xd.com',                   'HK'),
    ('9992.HK',  '泡泡玛特',  'POP MART',         'popmart.com',              'HK'),
    ('0992.HK',  '联想集团',  'LENOVO GROUP',     'lenovo.com',               'HK'),
    ('6618.HK',  '京东健康',  'JD HEALTH',        'jdhealth.com',             'HK'),
    ('0241.HK',  '阿里健康',  'ALI HEALTH',       'alihealth.cn',             'HK'),
    ('2618.HK',  '京东物流',  'JD LOGISTICS',     'jdl.com',                  'HK'),
    ('1211.HK',  '比亚迪',    'BYD COMPANY',      'byd.com',                  'HK'),
    ('0175.HK',  '吉利汽车',  'GEELY AUTO',       'geely.com',                'HK'),
    ('9863.HK',  '零跑汽车',  'LEAPMOTOR',        'leapmotor.com',            'HK'),
    ('2018.HK',  '瑞声科技',  'AAC TECH',         'aactechnologies.com',      'HK'),
    ('2382.HK',  '舜宇光学',  'SUNNY OPTICAL',    'sunnyoptical.com',         'HK'),
    ('6969.HK',  '思摩尔',    'SMOORE INTL',      'smooreholdings.com',       'HK'),
    ('0669.HK',  '创科实业',  'TECHTRONIC IND',   'ttigroup.com',             'HK'),
    ('1585.HK',  '雅迪控股',  'YADEA',            'yadea.com',                'HK'),
    ('0968.HK',  '信义光能',  'XINYI SOLAR',      'xinyisolar.com',           'HK'),
    ('0425.HK',  '敏实集团',  'MINTH GROUP',      'minthgroup.com',           'HK'),
    ('2020.HK',  '安踏体育',  'ANTA SPORTS',      'anta.com',                 'HK'),
    ('2331.HK',  '李宁',      'LI NING',          'lining.com',               'HK'),
    ('9633.HK',  '农夫山泉',  'NONGFU SPRING',    'nongfuspring.com',         'HK'),
    ('6862.HK',  '海底捞',    'HAIDILAO',         'haidilao.com',             'HK'),
    ('9987.HK',  '百胜中国',  'YUM CHINA',        'yumchina.com',             'HK'),
    ('2319.HK',  '蒙牛乳业',  'MENGNIU DAIRY',    'mengniu.com.cn',           'HK'),
    ('0291.HK',  '华润啤酒',  'CHINA RES BEER',   'crbeer.com.hk',            'HK'),
    ('2097.HK',  '蜜雪集团',  'MIXUE GROUP',      'mixue.com',                'HK'),
    ('2367.HK',  '巨子生物',  'GIANT BIOGENE',    'giantbiogene.com',         'HK'),
    ('9985.HK',  '卫龙美味',  'WL DELICIOUS',     'weiliangfood.com',         'HK'),
    ('6181.HK',  '老铺黄金',  'LAOPU GOLD',       'laopugold.com',            'HK'),
    ('2318.HK',  '中国平安',  'PING AN',          'pingan.com',               'HK'),
    ('0939.HK',  '建设银行',  'CCB',              'ccb.com',                  'HK'),
    ('1299.HK',  '友邦保险',  'AIA',              'aia.com',                  'HK'),
    ('2628.HK',  '中国人寿',  'China Life',       'chinalife.com.cn',         'HK'),
    ('0388.HK',  '港交所',    'HKEX',             'hkex.com.hk',              'HK'),
    ('0005.HK',  '汇丰控股',  'HSBC HOLDINGS',    'hsbc.com',                 'HK'),
    ('2328.HK',  '中国财险',  'PICC P&C',         'picc.com.cn',              'HK'),
    ('2588.HK',  '中银航空租赁','BOC AVIATION',   'bocaviation.com',          'HK'),
    ('3360.HK',  '远东宏信',  'FE HORIZON',       'fehorizon.com',            'HK'),
    ('3887.HK',  'HashKey',   'HASHKEY HLDGS',    'hashkey.com',              'HK'),
    ('1398.HK',  '工商银行',  'ICBC',             'icbc.com.cn',              'HK'),
    ('1788.HK',  '国泰君安',  'GUOTAI JUNAN I',   'gtja.com',                 'HK'),
    ('1801.HK',  '信达生物',  'INNOVENT BIO',     'innoventbio.com',          'HK'),
    ('2269.HK',  '药明生物',  'WUXI BIO',         'wuxibiologics.com',        'HK'),
    ('1093.HK',  '石药集团',  'CSPC PHARMA',      'cspc.com.hk',              'HK'),
    ('9926.HK',  '康方生物',  'AKESO',            'akesobio.com',             'HK'),
    ('1530.HK',  '三生制药',  '3SBIO',            '3sbio.com',                'HK'),
    ('1177.HK',  '中国生物制药','SINO BIOPHARM',  'sinobiopharm.com',         'HK'),
    ('9995.HK',  '荣昌生物',  'REMEGEN',          'remegen.com',              'HK'),
    ('3692.HK',  '翰森制药',  'HANSOH PHARMA',    'hansoh.cn',                'HK'),
    ('1548.HK',  '金斯瑞',    'GENSCRIPT BIO',    'genscript.com',            'HK'),
    ('1951.HK',  '锦欣生殖',  'JXR',              'jxr.com',                  'HK'),
    ('1109.HK',  '华润置地',  'CHINA RES LAND',   'crland.com.hk',            'HK'),
    ('0001.HK',  '长和',      'CKH HOLDINGS',     'ckh.com.hk',               'HK'),
    ('0016.HK',  '新鸿基地产','SHK PPT',          'shkp.com',                 'HK'),
    ('0688.HK',  '中国海外',  'CHINA OVERSEAS',   'coli.com.hk',              'HK'),
    ('0267.HK',  '中信股份',  'CITIC',            'citic.com',                'HK'),
    ('1918.HK',  '融创中国',  'SUNAC',            'sunac.com.cn',             'HK'),
    ('0960.HK',  '龙湖集团',  'LONGFOR GROUP',    'longfor.com',              'HK'),
    ('2602.HK',  '万物云',    'ONEWO',            'onewo.com',                'HK'),
    ('9979.HK',  '绿城管理',  'GREENTOWN MGMT',   'greentownmanagement.com',  'HK'),
    ('0101.HK',  '恒隆地产',  'HANG LUNG PPT',    'hanglung.com',             'HK'),
    ('2007.HK',  '碧桂园',    'COUNTRY GARDEN',   'bgy.com.cn',               'HK'),
    ('1209.HK',  '华润万象',  'CHINA RES MIXC',   'crmixc.com',               'HK'),
    ('2899.HK',  '紫金矿业',  'ZIJIN MINING',     'zijinmining.com',          'HK'),
    ('0883.HK',  '中国海洋石油','CNOOC',          'cnoocltd.com',             'HK'),
    ('1378.HK',  '中国宏桥',  'CHINAHONGQIAO',    'hongqiaochina.com',        'HK'),
    ('1208.HK',  '五矿资源',  'MMG',              'mmg.com',                  'HK'),
    ('1818.HK',  '招金矿业',  'ZHAOJIN MINING',   'zhaojin.com.cn',           'HK'),
    ('1171.HK',  '兖矿能源',  'YANKUANG ENERGY',  'yankuang.com.cn',          'HK'),
    ('2688.HK',  '新奥能源',  'ENN ENERGY',       'ennenergy.com',            'HK'),
    ('0836.HK',  '华润电力',  'CHINA RES POWER',  'cr-power.com',             'HK'),
    ('1816.HK',  '中广核电力','CGN POWER',        'cgnpower.com',             'HK'),
    ('0135.HK',  '昆仑能源',  'KUNLUN ENERGY',    'kunlunenergy.com',         'HK'),
    ('0189.HK',  '东岳集团',  'DONGYUE GROUP',    'dongyue.com',              'HK'),
    ('0006.HK',  '电能实业',  'POWER ASSETS',     'powerassets.com',          'HK'),
    ('0941.HK',  '中国移动',  'CHINA MOBILE',     'chinamobileltd.com',       'HK'),
    ('0728.HK',  '中国电信',  'CHINA TELECOM',    'chinatelecom-h.com',       'HK'),
    ('0762.HK',  '中国联通',  'CHINA UNICOM',     'chinaunicom.com.hk',       'HK'),
    ('0788.HK',  '中国铁塔',  'CHINA TOWER',      'chinatowercom.cn',         'HK'),
    ('0066.HK',  '港铁公司',  'MTR CORPORATION',  'mtr.com.hk',               'HK'),
    ('1519.HK',  '极兔速递',  "J&T EXPRESS-W",    'jtexpress.com',            'HK'),
    ('0371.HK',  '北控水务',  'BJ ENT WATER',     'bjentwater.com',           'HK'),
    ('0257.HK',  '光大环境',  'EB ENVIRONMENT',   'ebenv.com',                'HK'),
    ('1308.HK',  '海丰国际',  'SITC',             'sitcline.com',             'HK'),
    ('9956.HK',  '安能物流',  'ANE',              'ane56.com',                'HK'),
    ('2057.HK',  '中通快递',  'ZTO EXPRESS-W',    'zto.com',                  'HK'),
    ('0285.HK',  '比亚迪电子','BYD ELECTRONIC',   'byd.com',                  'HK'),
    ('0551.HK',  '裕元集团',  'YUE YUEN IND',     'yueyuen.com',              'HK'),
    ('2313.HK',  '申洲国际',  'SHENZHOU INTL',    'shenzhouintl.com',         'HK'),
    ('0522.HK',  'ASMPT',     'ASMPT',            'asmpt.com',                'HK'),
    ('3931.HK',  '中创新航',  'CALB',             'calb.cn',                  'HK'),
    ('0179.HK',  '德昌电机',  'JOHNSON ELEC H',   'johnsonelectric.com',      'HK'),
    ('1888.HK',  '建滔积层板','KB LAMINATES',     'ktbs.com.hk',              'HK'),
    ('2498.HK',  '速腾聚创',  'ROBOSENSE',        'robosense.ai',             'HK'),
    ('6082.HK',  '壁仞科技',  'BIREN',            'biren.ai',                 'HK'),
    ('2228.HK',  '晶泰控股',  'XTALPI',           'xtalpi.com',               'HK'),
    ('9660.HK',  '地平线',    'HORIZONROBOT-W',   'horizon.auto',             'HK'),
]

# =============================================
# Asia: 2024 and 2025 benchmarks
# =============================================
ASIA_PRICES_2024 = {
    # Japan
    '9984.T': 2287.28, '6758.T': 3350.35, '6501.T': 3890.98, '6752.T': 1598.54,
    '6702.T': 2775.23, '7974.T': 9162.91, '8035.T': 23593.20, '6857.T': 9154.07,
    '4063.T': 5176.15, '6920.T': 14949.68, '6723.T': 2046.50, '6971.T': 1533.99,
    '6981.T': 2501.77, '6301.T': 4172.86, '6594.T': 2833.61, '6954.T': 4078.76,
    '6367.T': 18327.16, '6273.T': 60963.11, '7203.T': 3043.56, '7267.T': 1467.35,
    '7269.T': 1752.96, '6902.T': 2147.69, '9983.T': 53246.72, '4911.T': 2740.83,
    '8001.T': 1526.85, '8058.T': 2518.60, '3382.T': 2434.72, '2914.T': 3890.98,
    '7581.T': 5321.19, '4502.T': 3999.08, '4568.T': 4266.76, '4519.T': 6781.31,
    '4503.T': 1461.21, '7741.T': 19565.60, '7733.T': 2347.01, '4543.T': 3029.27,
    '6098.T': 11112.00,
    # Korea
    '005930.KS': 52329.90, '000660.KS': 172099.42, '066570.KS': 82453.71,
    '009150.KS': 123800.00, '373220.KS': 348000.00, '006400.KS': 247500.00,
    '051910.KS': 249070.62, '005490.KS': 244582.03, '005380.KS': 198801.50,
    '000270.KS': 94075.00, '012330.KS': 230948.14, '329180.KS': 284329.84,
    '241560.KS': 40974.14, '207940.KS': 1459121.62, '068270.KS': 179537.27,
    '035420.KS': 197929.12, '035720.KS': 38142.40, '090430.KS': 103695.03,
    '097950.KS': 247358.89, '352820.KS': 193233.98, '105560.KS': 80082.95,
    # Taiwan
    '2330.TW': 1057.72, '2454.TW': 1359.24, '3711.TW': 156.10, '2303.TW': 40.44,
    '3034.TW': 475.68, '2317.TW': 177.55, '2382.TW': 273.93, '2308.TW': 422.98,
    '3231.TW': 100.56, '3008.TW': 2583.84, '2357.TW': 586.08, '2395.TW': 337.88,
    '5274.TWO': 3286.96, '1301.TW': 35.00, '2603.TW': 195.33,
}

ASIA_PRICES_2025 = {
    # Japan
    '9984.T': 4400.00, '6758.T': 4024.00, '6501.T': 4902.00, '6752.T': 2023.50,
    '6702.T': 4329.00, '7974.T': 10595.00, '8035.T': 34320.00, '6857.T': 19635.00,
    '4063.T': 4873.00, '6920.T': 29645.00, '6723.T': 2140.00, '6971.T': 2196.50,
    '6981.T': 3246.00, '6301.T': 5000.00, '6594.T': 2132.00, '6954.T': 6084.00,
    '6367.T': 20080.00, '6273.T': 54460.00, '7203.T': 3356.00, '7267.T': 1536.00,
    '7269.T': 2334.50, '6902.T': 2158.00, '9983.T': 56940.00, '4911.T': 2278.00,
    '8001.T': 1975.00, '8058.T': 3586.00, '3382.T': 2250.50, '2914.T': 5640.00,
    '7581.T': 5480.00, '4502.T': 4835.00, '4568.T': 3348.00, '4519.T': 8243.00,
    '4503.T': 2093.00, '7741.T': 23685.00, '7733.T': 1984.50, '4543.T': 2270.00,
    '6098.T': 8847.00,
    # Korea
    '005930.KS': 119900.00, '000660.KS': 651000.00, '066570.KS': 91900.00,
    '009150.KS': 255000.00, '373220.KS': 368500.00, '006400.KS': 269500.00,
    '051910.KS': 333000.00, '005490.KS': 305000.00, '005380.KS': 296500.00,
    '000270.KS': 121800.00, '012330.KS': 373000.00, '329180.KS': 509000.00,
    '241560.KS': 57700.00, '207940.KS': 1695000.00, '068270.KS': 181000.00,
    '035420.KS': 242500.00, '035720.KS': 60100.00, '090430.KS': 119500.00,
    '097950.KS': 208000.00, '352820.KS': 330000.00, '105560.KS': 124700.00,
    # Taiwan
    '2330.TW': 1550.00, '2454.TW': 1430.00, '3711.TW': 250.50, '2303.TW': 49.25,
    '3034.TW': 374.00, '2317.TW': 230.50, '2382.TW': 272.00, '2308.TW': 963.00,
    '3231.TW': 150.50, '3008.TW': 2495.00, '2357.TW': 548.00, '2395.TW': 288.00,
    '5274.TWO': 7260.00, '1301.TW': 39.00, '2603.TW': 190.00,
}

ASIA_TICKERS = [
    # symbol, name_cn, name_en, market, domain, tag_type
    ('9984.T',    '软银集团',  'SoftBank Group',    'JP', 'group.softbank',      'JP'),
    ('6758.T',    '索尼集团',  'Sony Group',        'JP', 'sony.com',            'JP'),
    ('6501.T',    '日立制作所','Hitachi',           'JP', 'hitachi.com',         'JP'),
    ('6752.T',    '松下控股',  'Panasonic',         'JP', 'holdings.panasonic',  'JP'),
    ('6702.T',    '富士通',    'Fujitsu',           'JP', 'fujitsu.com',         'JP'),
    ('7974.T',    '任天堂',    'Nintendo',          'JP', 'nintendo.co.jp',      'JP'),
    ('8035.T',    '东京电子',  'Tokyo Electron',    'JP', 'tel.com',             'JP'),
    ('6857.T',    '爱德万测试','Advantest',         'JP', 'advantest.com',       'JP'),
    ('4063.T',    '信越化学',  'Shin-Etsu Chemical','JP', 'shinetsu.co.jp',      'JP'),
    ('6920.T',    '激光科技',  'Lasertec',          'JP', 'lasertec.co.jp',      'JP'),
    ('6723.T',    '瑞萨电子',  'Renesas Elec',      'JP', 'renesas.com',         'JP'),
    ('6971.T',    '京瓷',      'Kyocera',           'JP', 'kyocera.co.jp',       'JP'),
    ('6981.T',    '村田制作所','Murata Manufact',   'JP', 'murata.com',          'JP'),
    ('6301.T',    '小松制作所','Komatsu',           'JP', 'komatsu.com',         'JP'),
    ('6594.T',    '尼得科',    'Nidec',             'JP', 'nidec.com',           'JP'),
    ('6954.T',    '发那科',    'FANUC',             'JP', 'fanuc.co.jp',         'JP'),
    ('6367.T',    '大金工业',  'Daikin Industries', 'JP', 'daikin.com',          'JP'),
    ('6273.T',    'SMC',       'SMC Corp',          'JP', 'smcworld.com',        'JP'),
    ('7203.T',    '丰田汽车',  'Toyota Motor',      'JP', 'toyota.com',          'JP'),
    ('7267.T',    '本田技研',  'Honda Motor',       'JP', 'honda.co.jp',         'JP'),
    ('7269.T',    '铃木汽车',  'Suzuki Motor',      'JP', 'suzuki.co.jp',        'JP'),
    ('6902.T',    '电装',      'Denso',             'JP', 'denso.com',           'JP'),
    ('9983.T',    '迅销集团',  'Fast Retailing',    'JP', 'fastretailing.com',   'JP'),
    ('4911.T',    '资生堂',    'Shiseido',          'JP', 'shiseido.com',        'JP'),
    ('8001.T',    '伊藤忠',    'Itochu',            'JP', 'itochu.co.jp',        'JP'),
    ('8058.T',    '三菱商事',  'Mitsubishi Corp',   'JP', 'mitsubishicorp.com',  'JP'),
    ('3382.T',    '七和伊',    'Seven & i',         'JP', '7andi.com',           'JP'),
    ('2914.T',    '日本烟草',  'Japan Tobacco',     'JP', 'jti.com',             'JP'),
    ('7581.T',    '萨莉亚',    'Saizeriya',         'JP', 'saizeriya.co.jp',     'JP'),
    ('4502.T',    '武田药品',  'Takeda Pharma',     'JP', 'takeda.com',          'JP'),
    ('4568.T',    '第一三共',  'Daiichi Sankyo',    'JP', 'daiichisankyo.com',   'JP'),
    ('4519.T',    '中外制药',  'Chugai Pharma',     'JP', 'chugai-pharm.co.jp',  'JP'),
    ('4503.T',    '安斯泰来',  'Astellas Pharma',   'JP', 'astellas.com',        'JP'),
    ('7741.T',    '豪雅',      'HOYA',              'JP', 'hoya.com',            'JP'),
    ('7733.T',    '奥林巴斯',  'Olympus',           'JP', 'olympus.co.jp',       'JP'),
    ('4543.T',    '泰尔茂',    'Terumo',            'JP', 'terumo.com',          'JP'),
    ('6098.T',    '瑞可利',    'Recruit Holdings',  'JP', 'recruit.co.jp',       'JP'),
    ('005930.KS', '三星电子',  'Samsung Elec',      'KR', 'samsung.com',         'KR'),
    ('000660.KS', 'SK海力士',  'SK Hynix',          'KR', 'skhynix.com',         'KR'),
    ('066570.KS', 'LG电子',    'LG Elec',           'KR', 'lge.co.kr',           'KR'),
    ('009150.KS', '三星电机',  'Samsung Elec-Mech', 'KR', 'samsem.com',          'KR'),
    ('373220.KS', 'LG新能源',  'LG Energy',         'KR', 'lgensol.com',         'KR'),
    ('006400.KS', '三星SDI',   'Samsung SDI',       'KR', 'samsungsdi.com',      'KR'),
    ('051910.KS', 'LG化学',    'LG Chem',           'KR', 'lgchem.com',          'KR'),
    ('005490.KS', '浦项控股',  'POSCO Holdings',    'KR', 'posco.com',           'KR'),
    ('005380.KS', '现代汽车',  'Hyundai Motor',     'KR', 'hyundai.com',         'KR'),
    ('000270.KS', '起亚汽车',  'Kia Corp',          'KR', 'kia.com',             'KR'),
    ('012330.KS', '现代摩比斯','Hyundai Mobis',     'KR', 'mobis.co.kr',         'KR'),
    ('329180.KS', 'HD现代重工','HD Heavy Ind',      'KR', 'hhi.co.kr',           'KR'),
    ('241560.KS', '斗山山猫',  'Doosan Bobcat',     'KR', 'doosanbobcat.com',    'KR'),
    ('207940.KS', '三星生物',  'Samsung Biologics', 'KR', 'samsungbiologics.com','KR'),
    ('068270.KS', '赛特瑞恩',  'Celltrion',         'KR', 'celltrion.com',       'KR'),
    ('035420.KS', 'NAVER',     'Naver Corp',        'KR', 'navercorp.com',       'KR'),
    ('035720.KS', 'Kakao',     'Kakao',             'KR', 'kakaocorp.com',       'KR'),
    ('090430.KS', '爱茉莉',    'Amorepacific',      'KR', 'apgroup.com',         'KR'),
    ('097950.KS', 'CJ第一制糖','CJ CheilJedang',    'KR', 'cj.net',              'KR'),
    ('352820.KS', 'HYBE',      'HYBE',              'KR', 'hybecorp.com',        'KR'),
    ('105560.KS', 'KB金融',    'KB Financial',      'KR', 'kbfg.com',            'KR'),
    ('2330.TW',   '台积电',    'TSMC',              'TW', 'tsmc.com',            'TW'),
    ('2454.TW',   '联发科',    'MediaTek',          'TW', 'mediatek.com',        'TW'),
    ('3711.TW',   '日月光',    'ASE Technology',    'TW', 'aseglobal.com',       'TW'),
    ('2303.TW',   '联电',      'UMC',               'TW', 'umc.com',             'TW'),
    ('3034.TW',   '联咏',      'Novatek',           'TW', 'novatek.com.tw',      'TW'),
    ('2317.TW',   '鸿海',      'Foxconn',           'TW', 'foxconn.com',         'TW'),
    ('2382.TW',   '广达',      'Quanta',            'TW', 'quantatw.com',        'TW'),
    ('2308.TW',   '台达电',    'Delta Electronics', 'TW', 'deltaww.com',         'TW'),
    ('3231.TW',   '纬创',      'Wistron',           'TW', 'wistron.com',         'TW'),
    ('3008.TW',   '大立光',    'Largan Precision',  'TW', 'largan.com.tw',       'TW'),
    ('2357.TW',   '华硕',      'Asus',              'TW', 'asus.com',            'TW'),
    ('2395.TW',   '研华',      'Advantech',         'TW', 'advantech.com',       'TW'),
    ('5274.TWO',  '信骅',      'Aspeed',            'TW', 'aspeedtech.com',      'TW'),
    ('1301.TW',   '台塑',      'Formosa Plastics',  'TW', 'fpc.com.tw',          'TW'),
    ('2603.TW',   '长荣海运',  'Evergreen Marine',  'TW', 'evergreen-marine.com','TW'),
]


def seed(conn):
    cur = conn.cursor()

    print("Seeding US tickers...")
    for row in US_TICKERS:
        symbol, name_cn, name_en, domain, tag_type = row
        cur.execute("""
            INSERT INTO tickers (symbol, name_cn, name_en, market, domain, tag_type)
            VALUES (%s, %s, %s, 'US', %s, %s)
            ON CONFLICT (symbol) DO UPDATE SET
                name_cn=EXCLUDED.name_cn, name_en=EXCLUDED.name_en,
                domain=EXCLUDED.domain, tag_type=EXCLUDED.tag_type
        """, (symbol, name_cn, name_en, domain, tag_type))

    print("Seeding HK tickers...")
    for row in HK_TICKERS:
        symbol, name_cn, name_en, domain, tag_type = row
        cur.execute("""
            INSERT INTO tickers (symbol, name_cn, name_en, market, domain, tag_type)
            VALUES (%s, %s, %s, 'HK', %s, %s)
            ON CONFLICT (symbol) DO UPDATE SET
                name_cn=EXCLUDED.name_cn, name_en=EXCLUDED.name_en,
                domain=EXCLUDED.domain, tag_type=EXCLUDED.tag_type
        """, (symbol, name_cn, name_en, domain, tag_type))

    print("Seeding Asia tickers...")
    for row in ASIA_TICKERS:
        symbol, name_cn, name_en, market, domain, tag_type = row
        cur.execute("""
            INSERT INTO tickers (symbol, name_cn, name_en, market, domain, tag_type)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (symbol) DO UPDATE SET
                name_cn=EXCLUDED.name_cn, name_en=EXCLUDED.name_en,
                domain=EXCLUDED.domain, tag_type=EXCLUDED.tag_type
        """, (symbol, name_cn, name_en, market, domain, tag_type))

    print("Seeding US annual benchmarks (2024, 2025)...")
    for symbol, price in YTD_BASE_PRICES_2024.items():
        cur.execute("""
            INSERT INTO annual_benchmarks (symbol, year, price) VALUES (%s, 2024, %s)
            ON CONFLICT (symbol, year) DO UPDATE SET price=EXCLUDED.price
        """, (symbol, price))
    for symbol, price in TARGET_2025_PRICES.items():
        cur.execute("""
            INSERT INTO annual_benchmarks (symbol, year, price) VALUES (%s, 2025, %s)
            ON CONFLICT (symbol, year) DO UPDATE SET price=EXCLUDED.price
        """, (symbol, price))

    print("Seeding HK annual benchmarks (2024, 2025)...")
    for symbol, price in HK_PRICES_2024.items():
        cur.execute("""
            INSERT INTO annual_benchmarks (symbol, year, price) VALUES (%s, 2024, %s)
            ON CONFLICT (symbol, year) DO UPDATE SET price=EXCLUDED.price
        """, (symbol, price))
    for symbol, price in HK_PRICES_2025.items():
        cur.execute("""
            INSERT INTO annual_benchmarks (symbol, year, price) VALUES (%s, 2025, %s)
            ON CONFLICT (symbol, year) DO UPDATE SET price=EXCLUDED.price
        """, (symbol, price))

    print("Seeding Asia annual benchmarks (2024, 2025)...")
    for symbol, price in ASIA_PRICES_2024.items():
        cur.execute("""
            INSERT INTO annual_benchmarks (symbol, year, price) VALUES (%s, 2024, %s)
            ON CONFLICT (symbol, year) DO UPDATE SET price=EXCLUDED.price
        """, (symbol, price))
    for symbol, price in ASIA_PRICES_2025.items():
        cur.execute("""
            INSERT INTO annual_benchmarks (symbol, year, price) VALUES (%s, 2025, %s)
            ON CONFLICT (symbol, year) DO UPDATE SET price=EXCLUDED.price
        """, (symbol, price))

    conn.commit()
    cur.close()
    print("Seed complete.")


if __name__ == "__main__":
    conn = psycopg.connect(DATABASE_URL)
    try:
        seed(conn)
    finally:
        conn.close()
