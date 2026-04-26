"""
Group definitions for all three markets.
Used by the API to structure the response.
"""

US_GROUPS = [
    {
        "id": "global",
        "title": "1. Global Markets (ETF) • 全球市场核心",
        "sort_rule": "manual",
        "symbols": ['SPX', 'IXIC', 'DJI', 'RUT', 'MAGS', 'IBIT', 'GLD', 'USO',
                    'CPER', 'TLT', 'DXY', 'USDJPY'],
    },
    {
        "id": "tech",
        "title": "2. US Tech Giants • 美股科技巨头",
        "sort_rule": "market_cap",
        "symbols": ['AAPL', 'NVDA', 'META', 'GOOGL', 'MSFT', 'AMZN', 'AVGO', 'TSM',
                    'TSLA', 'ORCL', 'NFLX', 'PLTR', 'AMD', 'MU', 'INTC'],
    },
    {
        "id": "crypto",
        "title": "3. Crypto & Blockchain • 加密货币核心",
        "sort_rule": "market_cap",
        "symbols": ['IBIT', 'ETHA', 'HOOD', 'COIN', 'MSTR', 'CRCL', 'RIOT', 'MARA', 'CLSK'],
    },
    {
        "id": "china",
        "title": "4. China Core Assets • 中概股核心资产",
        "sort_rule": "market_cap",
        "symbols": ['BABA', 'PDD', 'NTES', 'JD', 'TCOM', 'LI', 'TME', 'BIDU',
                    'BEKE', 'FUTU', 'XPEV', 'YMM'],
    },
    {
        "id": "healthcare",
        "title": "5. Health Care • 医疗健康",
        "sort_rule": "market_cap",
        "symbols": ['LLY', 'JNJ', 'ABBV', 'NVO', 'UNH', 'TMO', 'ISRG', 'BSX',
                    'REGN', 'HIMS', 'TWST', 'CRSP'],
    },
    {
        "id": "consumer",
        "title": "6. Global Consumer • 零售/餐饮/旅游",
        "sort_rule": "market_cap",
        "symbols": ['WMT', 'COST', 'HD', 'MCD', 'BKNG', 'TJX', 'LOW', 'SBUX',
                    'DASH', 'ABNB', 'CMG', 'AZO'],
    },
    {
        "id": "staples",
        "title": "7. Staples & Discretionary • 必需/可选消费",
        "sort_rule": "market_cap",
        "symbols": ['PG', 'KO', 'PM', 'PEP', 'BUD', 'NKE', 'MDLZ', 'MNST',
                    'KHC', 'HSY', 'EL', 'LULU'],
    },
    {
        "id": "industrials",
        "title": "8. Industrials & Materials • 工业/材料",
        "sort_rule": "market_cap",
        "symbols": ['GE', 'LIN', 'RTX', 'CAT', 'BA', 'HON', 'ETN', 'DHR',
                    'LMT', 'MMM', 'SHW', 'EMR'],
    },
    {
        "id": "energy",
        "title": "9. Energy, Telecom & Transport • 能源/电信/运输",
        "sort_rule": "market_cap",
        "symbols": ['XOM', 'CVX', 'TMUS', 'SHEL', 'T', 'UBER', 'VZ', 'NEE',
                    'UNP', 'SO', 'WM', 'UPS'],
    },
    {
        "id": "finance",
        "title": "10. Banks & Finance • 银行/支付/投资",
        "sort_rule": "market_cap",
        "symbols": ['BRK.A', 'JPM', 'V', 'MA', 'BAC', 'WFC', 'MS', 'GS',
                    'AXP', 'SCHW', 'BLK', 'IBKR'],
    },
]

HK_GROUPS = [
    {
        "id": "core",
        "title": "🏆 核心资产",
        "sort_rule": "fixed",
        "symbols": ['0700.HK', '9988.HK', '1810.HK', '3690.HK', '0981.HK', '1211.HK',
                    '2269.HK', '1801.HK', '2899.HK', '0883.HK', '1378.HK', '2318.HK',
                    '0388.HK', '1299.HK', '0005.HK', '0992.HK', '2020.HK', '0941.HK'],
    },
    {
        "id": "internet",
        "title": "🌐 互联网科技",
        "sort_rule": "market_cap",
        "symbols": ['0700.HK', '9988.HK', '1810.HK', '3690.HK', '1024.HK', '9626.HK',
                    '2228.HK', '0020.HK', '0100.HK', '0772.HK', '1357.HK', '2400.HK'],
    },
    {
        "id": "semis",
        "title": "💾 半导体/硬件",
        "sort_rule": "market_cap",
        "symbols": ['0981.HK', '1347.HK', '2577.HK', '0992.HK', '6969.HK', '2382.HK',
                    '2018.HK', '9660.HK', '0285.HK', '1888.HK', '6082.HK', '2498.HK'],
    },
    {
        "id": "consumer",
        "title": "🛍️ 大消费",
        "sort_rule": "market_cap",
        "symbols": ['9992.HK', '2020.HK', '6181.HK', '2331.HK', '9633.HK', '6862.HK',
                    '9987.HK', '2319.HK', '0291.HK', '2097.HK', '2367.HK', '9985.HK'],
    },
    {
        "id": "finance",
        "title": "💰 金融",
        "sort_rule": "market_cap",
        "symbols": ['2318.HK', '0939.HK', '1299.HK', '2628.HK', '0388.HK', '0005.HK',
                    '2328.HK', '2588.HK', '3360.HK', '3887.HK', '1398.HK', '1788.HK'],
    },
    {
        "id": "biotech",
        "title": "🧬 生物科技",
        "sort_rule": "market_cap",
        "symbols": ['1801.HK', '2269.HK', '1093.HK', '9926.HK', '1530.HK', '6618.HK',
                    '0241.HK', '9995.HK', '3692.HK', '1177.HK', '1548.HK', '1951.HK'],
    },
    {
        "id": "property",
        "title": "🏙️ 综合与地产",
        "sort_rule": "market_cap",
        "symbols": ['1109.HK', '0001.HK', '0016.HK', '0688.HK', '0267.HK', '1918.HK',
                    '0960.HK', '2602.HK', '9979.HK', '0101.HK', '2007.HK', '1209.HK'],
    },
    {
        "id": "energy",
        "title": "⚡ 能源材料",
        "sort_rule": "market_cap",
        "symbols": ['2899.HK', '0883.HK', '1378.HK', '1208.HK', '1818.HK', '1171.HK',
                    '2688.HK', '0836.HK', '1816.HK', '0135.HK', '0189.HK', '0006.HK'],
    },
    {
        "id": "telecom",
        "title": "📡 运营商及公用事业",
        "sort_rule": "market_cap",
        "symbols": ['0941.HK', '0728.HK', '0762.HK', '0788.HK', '0066.HK', '1519.HK',
                    '0371.HK', '0257.HK', '2618.HK', '1308.HK', '9956.HK', '2057.HK'],
    },
    {
        "id": "manufacturing",
        "title": "🏭 制造业",
        "sort_rule": "market_cap",
        "symbols": ['1211.HK', '0175.HK', '9863.HK', '0669.HK', '2313.HK', '0522.HK',
                    '0968.HK', '0179.HK', '3931.HK', '1585.HK', '0425.HK', '0551.HK'],
    },
]

ASIA_GROUPS = [
    {
        "id": "japan",
        "title": "🇯🇵 Japan Tech & Industrial",
        "sort_rule": "market_cap",
        "market_filter": "JP",
        "symbols": [
            '9984.T', '6758.T', '6501.T', '6752.T', '6702.T', '7974.T', '8035.T',
            '6857.T', '4063.T', '6920.T', '6723.T', '6971.T', '6981.T', '6301.T',
            '6594.T', '6954.T', '6367.T', '6273.T', '7203.T', '7267.T', '7269.T',
            '6902.T', '9983.T', '4911.T', '8001.T', '8058.T', '3382.T', '2914.T',
            '7581.T', '4502.T', '4568.T', '4519.T', '4503.T', '7741.T', '7733.T',
            '4543.T', '6098.T',
        ],
    },
    {
        "id": "korea",
        "title": "🇰🇷 Korea Tech & Industry",
        "sort_rule": "market_cap",
        "market_filter": "KR",
        "symbols": [
            '005930.KS', '000660.KS', '066570.KS', '009150.KS', '373220.KS',
            '006400.KS', '051910.KS', '005490.KS', '005380.KS', '000270.KS',
            '012330.KS', '329180.KS', '241560.KS', '207940.KS', '068270.KS',
            '035420.KS', '035720.KS', '090430.KS', '097950.KS', '352820.KS',
            '105560.KS',
        ],
    },
    {
        "id": "taiwan",
        "title": "🇹🇼 Taiwan Semi & Tech",
        "sort_rule": "market_cap",
        "market_filter": "TW",
        "symbols": [
            '2330.TW', '2454.TW', '3711.TW', '2303.TW', '3034.TW', '2317.TW',
            '2382.TW', '2308.TW', '3231.TW', '3008.TW', '2357.TW', '2395.TW',
            '5274.TWO', '1301.TW', '2603.TW',
        ],
    },
]
