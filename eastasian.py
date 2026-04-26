import yfinance as yf
import pandas as pd
import time
import os
import requests
import random
import string
from datetime import datetime

# ==========================================
# 0. Yahoo Finance URL 映射
# ==========================================
TICKER_URL_MAP = {
    # 日本股票
    '9984.T': 'https://finance.yahoo.com/quote/9984.T/',
    '6758.T': 'https://finance.yahoo.com/quote/6758.T/',
    '6501.T': 'https://finance.yahoo.com/quote/6501.T/',
    '6752.T': 'https://finance.yahoo.com/quote/6752.T/',
    '6702.T': 'https://finance.yahoo.com/quote/6702.T/',
    '7974.T': 'https://finance.yahoo.com/quote/7974.T/',
    '8035.T': 'https://finance.yahoo.com/quote/8035.T/',
    '6857.T': 'https://finance.yahoo.com/quote/6857.T/',
    '4063.T': 'https://finance.yahoo.com/quote/4063.T/',
    '6920.T': 'https://finance.yahoo.com/quote/6920.T/',
    '6723.T': 'https://finance.yahoo.com/quote/6723.T/',
    '6971.T': 'https://finance.yahoo.com/quote/6971.T/',
    '6981.T': 'https://finance.yahoo.com/quote/6981.T/',
    '6301.T': 'https://finance.yahoo.com/quote/6301.T/',
    '6594.T': 'https://finance.yahoo.com/quote/6594.T/',
    '6954.T': 'https://finance.yahoo.com/quote/6954.T/',
    '6367.T': 'https://finance.yahoo.com/quote/6367.T/',
    '6273.T': 'https://finance.yahoo.com/quote/6273.T/',
    '7203.T': 'https://finance.yahoo.com/quote/7203.T/',
    '7267.T': 'https://finance.yahoo.com/quote/7267.T/',
    '7269.T': 'https://finance.yahoo.com/quote/7269.T/',
    '6902.T': 'https://finance.yahoo.com/quote/6902.T/',
    '9983.T': 'https://finance.yahoo.com/quote/9983.T/',
    '4911.T': 'https://finance.yahoo.com/quote/4911.T/',
    '8001.T': 'https://finance.yahoo.com/quote/8001.T/',
    '8058.T': 'https://finance.yahoo.com/quote/8058.T/',
    '3382.T': 'https://finance.yahoo.com/quote/3382.T/',
    '2914.T': 'https://finance.yahoo.com/quote/2914.T/',
    '7581.T': 'https://finance.yahoo.com/quote/7581.T/',
    '4502.T': 'https://finance.yahoo.com/quote/4502.T/',
    '4568.T': 'https://finance.yahoo.com/quote/4568.T/',
    '4519.T': 'https://finance.yahoo.com/quote/4519.T/',
    '4503.T': 'https://finance.yahoo.com/quote/4503.T/',
    '7741.T': 'https://finance.yahoo.com/quote/7741.T/',
    '7733.T': 'https://finance.yahoo.com/quote/7733.T/',
    '4543.T': 'https://finance.yahoo.com/quote/4543.T/',
    '6098.T': 'https://finance.yahoo.com/quote/6098.T/',
    # 韩国股票
    '005930.KS': 'https://finance.yahoo.com/quote/005930.KS/',
    '000660.KS': 'https://finance.yahoo.com/quote/000660.KS/',
    '066570.KS': 'https://finance.yahoo.com/quote/066570.KS/',
    '009150.KS': 'https://finance.yahoo.com/quote/009150.KS/',
    '373220.KS': 'https://finance.yahoo.com/quote/373220.KS/',
    '006400.KS': 'https://finance.yahoo.com/quote/006400.KS/',
    '051910.KS': 'https://finance.yahoo.com/quote/051910.KS/',
    '005490.KS': 'https://finance.yahoo.com/quote/005490.KS/',
    '005380.KS': 'https://finance.yahoo.com/quote/005380.KS/',
    '000270.KS': 'https://finance.yahoo.com/quote/000270.KS/',
    '012330.KS': 'https://finance.yahoo.com/quote/012330.KS/',
    '329180.KS': 'https://finance.yahoo.com/quote/329180.KS/',
    '241560.KS': 'https://finance.yahoo.com/quote/241560.KS/',
    '207940.KS': 'https://finance.yahoo.com/quote/207940.KS/',
    '068270.KS': 'https://finance.yahoo.com/quote/068270.KS/',
    '035420.KS': 'https://finance.yahoo.com/quote/035420.KS/',
    '035720.KS': 'https://finance.yahoo.com/quote/035720.KS/',
    '090430.KS': 'https://finance.yahoo.com/quote/090430.KS/',
    '097950.KS': 'https://finance.yahoo.com/quote/097950.KS/',
    '352820.KS': 'https://finance.yahoo.com/quote/352820.KS/',
    '105560.KS': 'https://finance.yahoo.com/quote/105560.KS/',
    # 台湾股票
    '2330.TW': 'https://finance.yahoo.com/quote/2330.TW/',
    '2454.TW': 'https://finance.yahoo.com/quote/2454.TW/',
    '3711.TW': 'https://finance.yahoo.com/quote/3711.TW/',
    '2303.TW': 'https://finance.yahoo.com/quote/2303.TW/',
    '3034.TW': 'https://finance.yahoo.com/quote/3034.TW/',
    '2317.TW': 'https://finance.yahoo.com/quote/2317.TW/',
    '2382.TW': 'https://finance.yahoo.com/quote/2382.TW/',
    '2308.TW': 'https://finance.yahoo.com/quote/2308.TW/',
    '3231.TW': 'https://finance.yahoo.com/quote/3231.TW/',
    '3008.TW': 'https://finance.yahoo.com/quote/3008.TW/',
    '2357.TW': 'https://finance.yahoo.com/quote/2357.TW/',
    '2395.TW': 'https://finance.yahoo.com/quote/2395.TW/',
    '5274.TW': 'https://finance.yahoo.com/quote/5274.TW/',
    '1301.TW': 'https://finance.yahoo.com/quote/1301.TW/',
    '2603.TW': 'https://finance.yahoo.com/quote/2603.TW/',
}

# ==========================================
# 1. 代理配置 (隧道代理 + 动态轮换)
# ==========================================
# 原始信息: blurpath.net:15132:pdd6wxr7bg-zone-resi-region-HK,JP,TW,US-st--city--session-zPDM-sessionTime-0:NerxBq
PROXY_CONFIG_STR = "blurpath.net:15132:pdd6wxr7bg-zone-resi-region-HK,JP,TW,US-st--city--session-zPDM-sessionTime-0:NerxBq"

def get_proxy():
    """
    解析静态代理配置并生成新的 Session ID (如果支持动态 session)
    注意：对于某些隧道代理，改变 session ID 字符串通常会触发 IP 切换。
    """
    # 生成一个随机的 8 位字符串作为 session ID，以确保每次获取的 IP 不同
    random_session = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    
    print(f"  🔄 正在配置代理 (Session: {random_session})...", end="")
    try:
        # 解析提供的字符串: host:port:username:password
        parts = PROXY_CONFIG_STR.split(':')
        if len(parts) == 4:
            host = parts[0]
            port = parts[1]
            # 原始 username 通常包含 session-xxx 部分，我们需要替换它来实现切换
            raw_username = parts[2]
            password = parts[3]
            
            # 尝试动态替换 session ID 以强制切换 IP
            if "session-" in raw_username:
                # 使用正则或字符串替换将 session-zPDM 替换为 session-{random}
                import re
                # 替换 session- 后面的字母数字直到下一个破折号或结尾
                new_username = re.sub(r'session-[a-zA-Z0-9]+', f'session-{random_session}', raw_username)
                username = new_username
            else:
                username = raw_username

            # 构建带认证的代理字符串 http://user:pass@host:port
            proxy_str = f"http://{username}:{password}@{host}:{port}"
            print(f" 配置成功")
            return proxy_str
        else:
            print(f" 代理配置格式错误: {PROXY_CONFIG_STR}")
    except Exception as e:
        print(f" 配置代理异常: {e}")
    return None

CURRENT_PROXY = None

# ==========================================
# 1. 股票原始数据配置
# ==========================================
RAW_STOCK_DATA = """
9984.T       JP    软银集团           2287.28    4400.00    SoftBank Group
6758.T       JP    索尼集团           3350.35    4024.00    Sony Group
6501.T       JP    日立制作所          3890.98    4902.00    Hitachi
6752.T       JP    松下控股           1598.54    2023.50    Panasonic
6702.T       JP    富士通            2775.23    4329.00    Fujitsu
7974.T       JP    任天堂            9162.91    10595.00   Nintendo
8035.T       JP    东京电子           23593.20   34320.00   Tokyo Electron
6857.T       JP    爱德万测试          9154.07    19635.00   Advantest
4063.T       JP    信越化学           5176.15    4873.00    Shin-Etsu Chemical
6920.T       JP    激光科技           14949.68   29645.00   Lasertec
6723.T       JP    瑞萨电子           2046.50    2140.00    Renesas Elec
6971.T       JP    京瓷             1533.99    2196.50    Kyocera
6981.T       JP    村田制作所          2501.77    3246.00    Murata Manufact
6301.T       JP    小松制作所          4172.86    5000.00    Komatsu
6594.T       JP    尼得科            2833.61    2132.00    Nidec
6954.T       JP    发那科            4078.76    6084.00    FANUC
6367.T       JP    大金工业           18327.16   20080.00   Daikin Industries
6273.T       JP    SMC            60963.11   54460.00   SMC Corp
7203.T       JP    丰田汽车           3043.56    3356.00    Toyota Motor
7267.T       JP    本田技研           1467.35    1536.00    Honda Motor
7269.T       JP    铃木汽车           1752.96    2334.50    Suzuki Motor
6902.T       JP    电装             2147.69    2158.00    Denso
9983.T       JP    迅销集团           53246.72   56940.00   Fast Retailing
4911.T       JP    资生堂            2740.83    2278.00    Shiseido
8001.T       JP    伊藤忠商事          1526.85    1975.00    Itochu
8058.T       JP    三菱商事           2518.60    3586.00    Mitsubishi Corp
3382.T       JP    七和伊控股          2434.72    2250.50    Seven & i 
2914.T       JP    日本烟草           3890.98    5640.00    Japan Tobacco
7581.T       JP    萨莉亚            5321.19    5480.00    Saizeriya
4502.T       JP    武田药品           3999.08    4835.00    Takeda Pharma
4568.T       JP    第一三共           4266.76    3348.00    Daiichi Sankyo
4519.T       JP    中外制药           6781.31    8243.00    Chugai Pharma
4503.T       JP    安斯泰来           1461.21    2093.00    Astellas Pharma
7741.T       JP    豪雅             19565.60   23685.00   HOYA
7733.T       JP    奥林巴斯           2347.01    1984.50    Olympus
4543.T       JP    泰尔茂            3029.27    2270.00    Terumo
6098.T       JP    瑞可利            11112.00   8847.00    Recruit Holdings
005930.KS    KR    三星电子           52329.90   119900.00  Samsung Elec
000660.KS    KR    SK海力士          172099.42  651000.00  SK Hynix
066570.KS    KR    LG电子           82453.71   91900.00   LG Elec
009150.KS    KR    三星电机           123800.00  255000.00  Samsung Elec-Mech
373220.KS    KR    LG新能源          348000.00  368500.00  LG Energy 
006400.KS    KR    三星SDI          247500.00  269500.00  Samsung SDI
051910.KS    KR    LG化学           249070.62  333000.00  LG Chem
005490.KS    KR    浦项控股           244582.03  305000.00  POSCO Holdings
005380.KS    KR    现代汽车           198801.50  296500.00  Hyundai Motor
000270.KS    KR    起亚汽车           94075.00   121800.00  Kia Corp
012330.KS    KR    现代摩比斯          230948.14  373000.00  Hyundai Mobis
329180.KS    KR    HD现代重工         284329.84  509000.00  HD Heavy Ind
241560.KS    KR    斗山山猫           40974.14   57700.00   Doosan Bobcat
207940.KS    KR    三星生物           1459121.62 1695000.00 Samsung Biologics
068270.KS    KR    赛特瑞恩           179537.27  181000.00  Celltrion
035420.KS    KR    NAVER          197929.12  242500.00  Naver Corp
035720.KS    KR    Kakao          38142.40   60100.00   Kakao
090430.KS    KR    爱茉莉太平洋         103695.03  119500.00  Amorepacific
097950.KS    KR    CJ第一制糖         247358.89  208000.00  CJ CheilJedang
352820.KS    KR    HYBE           193233.98  330000.00  HYBE
105560.KS    KR    KB金融集团         80082.95   124700.00  KB Financial
2330.TW      TW    台积电            1057.72    1550.00    TSMC
2454.TW      TW    联发科            1359.24    1430.00    MediaTek
3711.TW      TW    日月光投控          156.10     250.50   ASE Technology
2303.TW      TW    联电             40.44      49.25      UMC
3034.TW      TW    联咏             475.68     374.00     Novatek
2317.TW      TW    鸿海             177.55     230.50     Foxconn
2382.TW      TW    广达             273.93     272.00     Quanta
2308.TW      TW    台达电            422.98     963.00    Delta Electronics
3231.TW      TW    纬创             100.56     150.50     Wistron
3008.TW      TW    大立光            2583.84    2495.00   Largan Precision
2357.TW      TW    华硕             586.08     548.00     Asus
2395.TW      TW    研华             337.88     288.00     Advantech
5274.TWO     TW    信骅             3286.96    7260.00    Aspeed
1301.TW      TW    台塑             35.00      39.00      Formosa Plastics
2603.TW      TW    长荣海运           195.33     190.00   Evergreen Marine
"""

# ==========================================
# 2. 域名映射 (用于获取 Favicon)
# ==========================================
TICKER_DOMAIN_MAP = {
    # Japan
    '9984.T': 'group.softbank', '6758.T': 'sony.com', '6501.T': 'hitachi.com', '6752.T': 'holdings.panasonic',
    '7974.T': 'nintendo.co.jp', '7203.T': 'toyota.com', '7267.T': 'honda.co.jp', '9983.T': 'fastretailing.com',
    '6954.T': 'fanuc.co.jp', '8035.T': 'tel.com', '6857.T': 'advantest.com', '4063.T': 'shinetsu.co.jp',
    '6723.T': 'renesas.com', '6971.T': 'kyocera.co.jp', '6981.T': 'murata.com', '6594.T': 'nidec.com',
    '6367.T': 'daikin.com', '6273.T': 'smcworld.com', '4911.T': 'shiseido.com', '2914.T': 'jti.com',
    '4502.T': 'takeda.com', '4568.T': 'daiichisankyo.com', '7733.T': 'olympus.co.jp', '6098.T': 'recruit.co.jp',
    '8001.T': 'itochu.co.jp', '8058.T': 'mitsubishicorp.com', '3382.T': '7andi.com',
    
    # Korea
    '005930.KS': 'samsung.com', '000660.KS': 'skhynix.com', '066570.KS': 'lge.co.kr', '005380.KS': 'hyundai.com',
    '000270.KS': 'kia.com', '035420.KS': 'navercorp.com', '035720.KS': 'kakaocorp.com', '373220.KS': 'lgensol.com',
    '051910.KS': 'lgchem.com', '005490.KS': 'posco.com', '207940.KS': 'samsungbiologics.com', '068270.KS': 'celltrion.com',
    '352820.KS': 'hybecorp.com', '105560.KS': 'kbfg.com', '090430.KS': 'apgroup.com',

    # Taiwan
    '2330.TW': 'tsmc.com', '2454.TW': 'mediatek.com', '2317.TW': 'foxconn.com', '2308.TW': 'deltaww.com',
    '2382.TW': 'quantatw.com', '2303.TW': 'umc.com', '3711.TW': 'aseglobal.com', '2357.TW': 'asus.com',
    '2603.TW': 'evergreen-marine.com', '1301.TW': 'fpc.com.tw', '3008.TW': 'largan.com.tw', '3231.TW': 'wistron.com',
    '5274.TWO': 'aspeedtech.com', '3034.TW': 'novatek.com.tw', '2395.TW': 'advantech.com'
}

# ==========================================
# 3. 数据处理逻辑
# ==========================================

def parse_static_data(raw_text):
    """解析用户提供的静态文本数据"""
    stock_list = []
    lines = raw_text.strip().split('\n')
    for line in lines:
        if not line.strip(): continue
        parts = line.split()
        if len(parts) >= 6:
            ticker = parts[0].strip()
            region = parts[1].strip()
            name_cn = parts[2].strip()
            try:
                price_24 = float(parts[3])
                price_25 = float(parts[4])
            except:
                price_24 = 0.0
                price_25 = 0.0
            name_en = " ".join(parts[5:]).strip()
            stock_list.append({
                'ticker': ticker,
                'region': region,
                'name_cn': name_cn,
                'name_en': name_en,
                'price_24': price_24,
                'price_25': price_25
            })
    return stock_list

def get_exchange_rates():
    """获取 USD 对 JPY, KRW, TWD 的汇率"""
    print("💱 正在获取最新汇率...")
    
    # 确保使用代理获取汇率
    global CURRENT_PROXY
    if not CURRENT_PROXY:
        CURRENT_PROXY = get_proxy()
    if CURRENT_PROXY:
        os.environ['HTTP_PROXY'] = CURRENT_PROXY
        os.environ['HTTPS_PROXY'] = CURRENT_PROXY
        
    rates = {'JP': 150.0, 'KR': 1300.0, 'TW': 32.0}
    pairs = {'JP': 'JPY=X', 'KR': 'KRW=X', 'TW': 'TWD=X'}
    try:
        tickers = " ".join(pairs.values())
        data = yf.Tickers(tickers)
        for region, symbol in pairs.items():
            try:
                info = data.tickers[symbol].info
                price = info.get('regularMarketPrice') or info.get('currentPrice') or info.get('previousClose')
                if price:
                    rates[region] = float(price)
            except:
                pass
    except Exception as e:
        print(f"  ! 汇率获取失败: {e}")
    return rates

def get_stock_data(stock_list, rates):
    """获取股票数据 (带自动重试和代理轮换机制)"""
    global CURRENT_PROXY
    
    # 初始代理设置
    if not CURRENT_PROXY:
        CURRENT_PROXY = get_proxy()
    if CURRENT_PROXY:
        os.environ['HTTP_PROXY'] = CURRENT_PROXY
        os.environ['HTTPS_PROXY'] = CURRENT_PROXY

    results = {}
    total = len(stock_list)
    print(f"📊 开始获取 {total} 只股票数据...")
    
    for idx, item in enumerate(stock_list):
        ticker_symbol = item['ticker']
        print(f"  [{idx+1}/{total}] 处理 {ticker_symbol} ...", end="\r")
        
        item_data = {
            'symbol': ticker_symbol,
            'name': item['name_cn'],
            'name_en': item['name_en'],
            'region': item['region'],
            'domain': TICKER_DOMAIN_MAP.get(ticker_symbol),
            'current_price': 0.0,
            'daily_change': 0.0,
            'ytd_change': 0.0,
            'yoy_25_change': 0.0,
            'market_cap_usd': 0.0,
            'pe_ttm': 0.0
        }
        
        price_24 = item['price_24']
        price_25 = item['price_25']
        
        # 计算 25 YoY
        if price_24 > 0 and price_25 > 0:
            item_data['yoy_25_change'] = ((price_25 - price_24) / price_24) * 100
        
        # --- 核心重试循环 ---
        max_retries = 3
        for attempt in range(max_retries):
            # 确保有代理
            if not CURRENT_PROXY:
                CURRENT_PROXY = get_proxy()
                if CURRENT_PROXY:
                    os.environ['HTTP_PROXY'] = CURRENT_PROXY
                    os.environ['HTTPS_PROXY'] = CURRENT_PROXY

            try:
                ticker = yf.Ticker(ticker_symbol)
                
                # 获取 info (触发网络请求)
                info = ticker.info
                
                # --- 数据提取 (成功获取 info 后) ---
                
                # 价格
                price = info.get('currentPrice') or info.get('regularMarketPrice') or info.get('previousClose')
                if price:
                    item_data['current_price'] = float(price)
                
                # 涨跌幅
                prev_close = info.get('previousClose')
                if item_data['current_price'] and prev_close:
                    item_data['daily_change'] = ((item_data['current_price'] - prev_close) / prev_close) * 100
                    
                # 市值 (转换为 USD)
                mcap_local = info.get('marketCap')
                if mcap_local:
                    rate = rates.get(item['region'], 1.0)
                    item_data['market_cap_usd'] = float(mcap_local) / rate
                    
                # PE
                pe = info.get('trailingPE')
                item_data['pe_ttm'] = float(pe) if pe else -1.0
                
                # YTD 计算
                current_price_calc = item_data['current_price']
                if current_price_calc == 0 and price_25 > 0:
                    current_price_calc = price_25

                if price_25 > 0 and current_price_calc > 0:
                    item_data['ytd_change'] = ((current_price_calc - price_25) / price_25) * 100

                # 成功获取，跳出重试循环
                break

            except Exception as e:
                print(f"    (Error: {e})", end="")
                
                # 失败时切换代理
                print("  🔄 正在切换新代理 IP 并重试...")
                CURRENT_PROXY = get_proxy()
                if CURRENT_PROXY:
                    os.environ['HTTP_PROXY'] = CURRENT_PROXY
                    os.environ['HTTPS_PROXY'] = CURRENT_PROXY
                
                time.sleep(2) # 稍作等待
                
                if attempt == max_retries - 1:
                    print(f"  ❌ {ticker_symbol} 最终获取失败，跳过。")

        results[ticker_symbol] = item_data
        time.sleep(0.5) # 避免请求过快
        
    print("\n✅ 数据获取完成")
    return results

# ==========================================
# 4. 辅助函数 (UI 相关)
# ==========================================
def format_market_cap_usd(val_usd):
    if not val_usd or val_usd == 0: return ""
    if val_usd >= 1_000_000_000:
        return f"{val_usd / 1_000_000_000:.1f}B USD"
    elif val_usd >= 1_000_000:
        return f"{val_usd / 1_000_000:.0f}M USD"
    else:
        return f"{val_usd:.0f} USD"

def interpolate_color(val, min_val, max_val, start_color, end_color):
    if val < min_val: val = min_val
    if val > max_val: val = max_val
    ratio = (val - min_val) / (max_val - min_val)
    r = int(start_color[0] + ratio * (end_color[0] - start_color[0]))
    g = int(start_color[1] + ratio * (end_color[1] - start_color[1]))
    b = int(start_color[2] + ratio * (end_color[2] - start_color[2]))
    return f"rgb({r}, {g}, {b})"

def get_color_style(change):
    threshold = 4.0
    white = (255, 255, 255)
    deep_green = (22, 163, 74)
    deep_red = (220, 38, 38)
    color_up = deep_green
    color_down = deep_red
    text_color = "#1f2937"
    pill_bg = "rgba(255,255,255, 0.85)"

    if change >= 0:
        bg_color = interpolate_color(change, 0, threshold, white, color_up)
        if change > 2.0:
            text_color = "#ffffff"
            pill_bg = "rgba(255,255,255, 0.2)"
    else:
        abs_change = abs(change)
        bg_color = interpolate_color(abs_change, 0, threshold, white, color_down)
        if abs_change > 2.0:
            text_color = "#ffffff"
            pill_bg = "rgba(255,255,255, 0.2)"
    return bg_color, text_color, pill_bg

# ==========================================
# 5. HTML 生成逻辑
# ==========================================
def generate_html(stock_data, parsed_stock_list):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

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

    # 增加 Cache-Control Meta 标签
    html_head = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="default">
    <meta name="apple-mobile-web-app-title" content="Asia Market">
    <!-- 禁止缓存 -->
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
    <meta http-equiv="Pragma" content="no-cache" />
    <meta http-equiv="Expires" content="0" />
    <!-- 启用点击链接 -->
    <meta name="format-detection" content="telephone=no">

    <title>East Asia Market Watch</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }}
        body {{ background-color: #f3f4f6; padding: 10px; }}
        .container {{ max-width: 1000px; margin: 0 auto; padding-bottom: 40px; }}

        .main-header {{ text-align: center; margin-bottom: 20px; padding: 20px 15px; background: white; border-radius: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); position: relative; }}
        .main-header h1 {{ font-size: 26px; color: #111827; margin-bottom: 8px; font-weight: 800; letter-spacing: -0.5px; }}
        
        .meta-info {{ color: #6b7280; font-size: 12px; line-height: 1.6; }}
        .meta-info.source {{ font-weight: 500; color: #4b5563; }}
        .meta-info.email {{ color: #9ca3af; font-size: 11px; margin-top: 2px; }}

        /* 刷新按钮样式 */
        .refresh-btn {{
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
        }}
        .refresh-btn:active {{ background-color: #e5e7eb; transform: scale(0.98); }}

        .nav-bar {{
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
        }}
        .nav-bar a {{ text-decoration: none; color: #1f2937; transition: color 0.2s; }}
        .nav-bar a:hover {{ color: #2563eb; }}
        .nav-sep {{ color: #d1d5db; font-weight: 400; }}

        .section {{ background: white; border-radius: 16px; padding: 15px 10px; margin-bottom: 20px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); }}
        .section-header {{ margin-bottom: 12px; border-bottom: 1px solid #f3f4f6; padding-bottom: 8px; }}
        .section-title {{ font-size: 18px; font-weight: 800; color: #1f2937; display: flex; align-items: center; }}

        .grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; table-layout: fixed; width: 100%; }}

        .card {{
            min-height: 180px;
            min-width: 0;
            border-radius: 10px;
            padding: 8px 4px;
            position: relative;
            display: flex;
            flex-direction: column;
            align-items: center;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
            border: 1px solid rgba(0,0,0,0.05);
            overflow: hidden;
            -webkit-tap-highlight-color: transparent;
            cursor: pointer;
        }}

        .badge-cap {{
            position: absolute; top: 4px; left: 4px; 
            background: rgba(255,255,255,0.9); padding: 1px 4px; 
            border-radius: 4px; font-size: 9px; font-weight: 700; color: #4b5563; 
            z-index: 10; box-shadow: 0 1px 1px rgba(0,0,0,0.1);
        }}
        .badge-region {{
            position: absolute; top: 4px; right: 4px;
            background: rgba(0,0,0,0.05); padding: 1px 4px;
            border-radius: 4px; font-size: 9px; font-weight: 700; color: #6b7280; z-index: 10;
        }}

        .logo-img {{ 
            width: 28px; height: 28px; border-radius: 50%; margin-bottom: 4px; margin-top: 14px; 
            object-fit: contain; background-color: white; padding: 2px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        .logo-placeholder {{
            width: 28px; height: 28px; border-radius: 50%; margin-bottom: 4px; margin-top: 14px;
            background: rgba(255,255,255,0.3); display: flex; align-items: center; justify-content: center;
            font-size: 10px; color: #555; font-weight: bold;
        }}

        .ticker {{ font-size: 14px; font-weight: 900; line-height: 1.1; }}
        .name-cn {{ 
            font-size: 11px; font-weight: 600; margin-top: 2px; margin-bottom: 1px;
            white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 100%; 
        }}
        .name-en {{
            font-size: 9px; font-weight: 500; opacity: 0.85; margin-bottom: 6px;
            white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 100%; text-transform: uppercase;
        }}

        .pill {{ 
            width: 100%; padding: 3px 0; border-radius: 6px; text-align: center; margin-bottom: 3px; 
            font-weight: 700; display: flex; align-items: center; justify-content: center; backdrop-filter: blur(4px); 
        }}
        .pill-price {{ font-size: 13px; }}
        .pill-change {{ font-size: 12px; }}
        .pill-ytd {{ font-size: 9px; padding: 2px 0; margin-top: auto; margin-bottom: 2px; }}
        .pill-yoy {{ font-size: 9px; padding: 2px 0; margin-bottom: 2px; opacity: 0.9; }}
        .pe-info {{ font-size: 9px; opacity: 0.7; margin-top: 2px; font-weight: 500; }}

        @media (min-width: 768px) {{
            .grid {{ grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 12px; }}
            .card {{ padding: 12px 6px; min-height: 200px; }}
            .ticker {{ font-size: 16px; }}
            .pill-price {{ font-size: 15px; }}
            .pill-change {{ font-size: 14px; }}
            .logo-img {{ width: 36px; height: 36px; }}
            .logo-placeholder {{ width: 36px; height: 36px; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="main-header">
            <h1>East Asia Market Watch</h1>
            <div class="meta-info">Update: {current_time}</div>
            <div class="meta-info source">Data Source: Yahoo Finance  20m delay/20m update</div>
            <div class="meta-info email">jasonlee325@gmail.com</div>
        </div>
        {nav_html}
"""

    html_body = ""
    groups = {
        "JP": {"title": "🇯🇵 Japan Tech & Auto", "items": []},
        "KR": {"title": "🇰🇷 Korea Tech & Industry", "items": []},
        "TW": {"title": "🇹🇼 Taiwan Semi & Tech", "items": []}
    }

    for item in parsed_stock_list:
        ticker_symbol = item['ticker']
        region = item['region']
        if ticker_symbol in stock_data:
            groups[region]["items"].append(stock_data[ticker_symbol])

    for region_code in ["JP", "KR", "TW"]:
        group = groups[region_code]
        if not group["items"]: continue

        html_body += f"""
        <div class="section">
            <div class="section-header">
                <div class="section-title">{group['title']}</div>
            </div>
            <div class="grid">
        """

        for item in group["items"]:
            daily_change = item['daily_change']
            ytd_change = item['ytd_change']
            yoy_25_change = item['yoy_25_change']
            pe_val = item['pe_ttm']
            domain = item['domain']

            # 修改逻辑：如果是韩国股票(KR)，不显示PE TTM
            if item['region'] == 'KR':
                pe_str = ""
            else:
                pe_str = f"PE(TTM) {pe_val:.1f}" if pe_val > 0 else ("PE(TTM) Loss" if pe_val < 0 else "PE(TTM) -")

            bg_color, text_color, pill_bg = get_color_style(daily_change)
            ytd_text_color = "#ffffff" if text_color == "#ffffff" else ('#dc2626' if ytd_change >= 0 else '#166534')
            yoy_text_color = "#ffffff" if text_color == "#ffffff" else ('#dc2626' if yoy_25_change >= 0 else '#166534')

            if domain:
                logo_html = f'<img class="logo-img" src="https://www.google.com/s2/favicons?domain={domain}&sz=64" alt="{item["name"]}" onerror="this.style.display=\'none\'" />'
            else:
                logo_html = f'<div class="logo-placeholder">{item["symbol"].split(".")[0]}</div>'

            # 获取 Yahoo Finance URL
            ticker_symbol = item['symbol']
            yahoo_url = TICKER_URL_MAP.get(ticker_symbol, '')
            card_link = f'<a href="{yahoo_url}" target="_blank" style="text-decoration: none; color: inherit;">' if yahoo_url else ''

            html_body += f"""
                {card_link}<div class="card" style="background-color: {bg_color}; color: {text_color};">
                    <div class="badge-cap">{format_market_cap_usd(item['market_cap_usd'])}</div>
                    <div class="badge-region">{item['region']}</div>
                    {logo_html}
                    <div class="ticker">{item['symbol']}</div>
                    <div class="name-cn">{item['name']}</div>
                    <div class="name-en">{item['name_en']}</div>

                    <div class="pill pill-price" style="background: {pill_bg}; color: {text_color};">
                        {item['current_price']:.0f}
                    </div>
                    <div class="pill pill-change" style="background: {pill_bg}; color: {text_color};">
                        {'+' if daily_change >= 0 else ''}{daily_change:.2f}%
                    </div>
                    <div class="pill pill-ytd" style="background: {pill_bg}; color: {ytd_text_color};">
                        YTD {ytd_change:+.1f}%
                    </div>
                    <div class="pill pill-yoy" style="background: {pill_bg}; color: {yoy_text_color};">
                        25 YoY {yoy_25_change:+.1f}%
                    </div>
                    <div class="pe-info">{pe_str}</div>
                </div>{"</a>" if yahoo_url else ""}
            """

        html_body += """
            </div>
        </div>
        """

    # 增加 JavaScript 处理刷新逻辑
    html_footer = f"""
        {nav_html}
    </div>
    <script>
        // 强制刷新函数：通过添加时间戳参数绕过缓存
        function forceReload() {{
            var url = window.location.href.split('?')[0];
            var timestamp = new Date().getTime();
            window.location.replace(url + '?t=' + timestamp);
        }}

        // 自动检测：当页面重新可见时（从后台切回），如果距离上次加载超过 10 分钟，则自动刷新
        var lastLoadTime = new Date().getTime();
        
        document.addEventListener('visibilitychange', function() {{
            if (document.visibilityState === 'visible') {{
                var currentTime = new Date().getTime();
                // 600000 ms = 10 minutes
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
    return html_head + html_body + html_footer

# ==========================================
# 6. 主程序
# ==========================================
def main():
    parsed_stock_list = parse_static_data(RAW_STOCK_DATA)
    rates = get_exchange_rates()
    data = get_stock_data(parsed_stock_list, rates)
    html_content = generate_html(data, parsed_stock_list)

    filename = "/www/wwwroot/efinmap.com/asia.html" 
    # 确保目录存在
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"\n✨ 成功生成 HTML 文件: {os.path.abspath(filename)}")

if __name__ == "__main__":
    main()