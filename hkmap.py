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
    '00001.HK': 'https://finance.yahoo.com/quote/0001.HK/',
    '00005.HK': 'https://finance.yahoo.com/quote/0005.HK/',
    '00006.HK': 'https://finance.yahoo.com/quote/0006.HK/',
    '00016.HK': 'https://finance.yahoo.com/quote/0016.HK/',
    '00020.HK': 'https://finance.yahoo.com/quote/0020.HK/',
    '00066.HK': 'https://finance.yahoo.com/quote/0066.HK/',
    '00101.HK': 'https://finance.yahoo.com/quote/0101.HK/',
    '00135.HK': 'https://finance.yahoo.com/quote/0135.HK/',
    '00175.HK': 'https://finance.yahoo.com/quote/0175.HK/',
    '00179.HK': 'https://finance.yahoo.com/quote/0179.HK/',
    '00189.HK': 'https://finance.yahoo.com/quote/0189.HK/',
    '00241.HK': 'https://finance.yahoo.com/quote/0241.HK/',
    '00257.HK': 'https://finance.yahoo.com/quote/0257.HK/',
    '00267.HK': 'https://finance.yahoo.com/quote/0267.HK/',
    '00285.HK': 'https://finance.yahoo.com/quote/0285.HK/',
    '00291.HK': 'https://finance.yahoo.com/quote/0291.HK/',
    '00371.HK': 'https://finance.yahoo.com/quote/0371.HK/',
    '00388.HK': 'https://finance.yahoo.com/quote/0388.HK/',
    '00425.HK': 'https://finance.yahoo.com/quote/0425.HK/',
    '00522.HK': 'https://finance.yahoo.com/quote/0522.HK/',
    '00551.HK': 'https://finance.yahoo.com/quote/0551.HK/',
    '00669.HK': 'https://finance.yahoo.com/quote/0669.HK/',
    '00688.HK': 'https://finance.yahoo.com/quote/0688.HK/',
    '00700.HK': 'https://finance.yahoo.com/quote/0700.HK/',
    '00728.HK': 'https://finance.yahoo.com/quote/0728.HK/',
    '00762.HK': 'https://finance.yahoo.com/quote/0762.HK/',
    '00772.HK': 'https://finance.yahoo.com/quote/0772.HK/',
    '00788.HK': 'https://finance.yahoo.com/quote/0788.HK/',
    '00836.HK': 'https://finance.yahoo.com/quote/0836.HK/',
    '00883.HK': 'https://finance.yahoo.com/quote/0883.HK/',
    '00939.HK': 'https://finance.yahoo.com/quote/0939.HK/',
    '00941.HK': 'https://finance.yahoo.com/quote/0941.HK/',
    '00960.HK': 'https://finance.yahoo.com/quote/0960.HK/',
    '00968.HK': 'https://finance.yahoo.com/quote/0968.HK/',
    '00981.HK': 'https://finance.yahoo.com/quote/0981.HK/',
    '00992.HK': 'https://finance.yahoo.com/quote/0992.HK/',
    '01024.HK': 'https://finance.yahoo.com/quote/1024.HK/',
    '01093.HK': 'https://finance.yahoo.com/quote/1093.HK/',
    '01109.HK': 'https://finance.yahoo.com/quote/1109.HK/',
    '01171.HK': 'https://finance.yahoo.com/quote/1171.HK/',
    '01177.HK': 'https://finance.yahoo.com/quote/1177.HK/',
    '01208.HK': 'https://finance.yahoo.com/quote/1208.HK/',
    '01209.HK': 'https://finance.yahoo.com/quote/1209.HK/',
    '01211.HK': 'https://finance.yahoo.com/quote/1211.HK/',
    '01299.HK': 'https://finance.yahoo.com/quote/1299.HK/',
    '01308.HK': 'https://finance.yahoo.com/quote/1308.HK/',
    '01347.HK': 'https://finance.yahoo.com/quote/1347.HK/',
    '01357.HK': 'https://finance.yahoo.com/quote/1357.HK/',
    '01378.HK': 'https://finance.yahoo.com/quote/1378.HK/',
    '01398.HK': 'https://finance.yahoo.com/quote/1398.HK/',
    '01519.HK': 'https://finance.yahoo.com/quote/1519.HK/',
    '01530.HK': 'https://finance.yahoo.com/quote/1530.HK/',
    '01548.HK': 'https://finance.yahoo.com/quote/1548.HK/',
    '01585.HK': 'https://finance.yahoo.com/quote/1585.HK/',
    '01788.HK': 'https://finance.yahoo.com/quote/1788.HK/',
    '01801.HK': 'https://finance.yahoo.com/quote/1801.HK/',
    '01810.HK': 'https://finance.yahoo.com/quote/1810.HK/',
    '01816.HK': 'https://finance.yahoo.com/quote/1816.HK/',
    '01818.HK': 'https://finance.yahoo.com/quote/1818.HK/',
    '01888.HK': 'https://finance.yahoo.com/quote/1888.HK/',
    '01918.HK': 'https://finance.yahoo.com/quote/1918.HK/',
    '01951.HK': 'https://finance.yahoo.com/quote/1951.HK/',
    '02007.HK': 'https://finance.yahoo.com/quote/2007.HK/',
    '02018.HK': 'https://finance.yahoo.com/quote/2018.HK/',
    '02020.HK': 'https://finance.yahoo.com/quote/2020.HK/',
    '02057.HK': 'https://finance.yahoo.com/quote/2057.HK/',
    '02097.HK': 'https://finance.yahoo.com/quote/2097.HK/',
    '02228.HK': 'https://finance.yahoo.com/quote/2228.HK/',
    '02269.HK': 'https://finance.yahoo.com/quote/2269.HK/',
    '02313.HK': 'https://finance.yahoo.com/quote/2313.HK/',
    '02318.HK': 'https://finance.yahoo.com/quote/2318.HK/',
    '02319.HK': 'https://finance.yahoo.com/quote/2319.HK/',
    '02328.HK': 'https://finance.yahoo.com/quote/2328.HK/',
    '02331.HK': 'https://finance.yahoo.com/quote/2331.HK/',
    '02367.HK': 'https://finance.yahoo.com/quote/2367.HK/',
    '02382.HK': 'https://finance.yahoo.com/quote/2382.HK/',
    '02400.HK': 'https://finance.yahoo.com/quote/2400.HK/',
    '02498.HK': 'https://finance.yahoo.com/quote/2498.HK/',
    '02577.HK': 'https://finance.yahoo.com/quote/2577.HK/',
    '02588.HK': 'https://finance.yahoo.com/quote/2588.HK/',
    '02602.HK': 'https://finance.yahoo.com/quote/2602.HK/',
    '02618.HK': 'https://finance.yahoo.com/quote/2618.HK/',
    '02628.HK': 'https://finance.yahoo.com/quote/2628.HK/',
    '06082.HK': 'https://finance.yahoo.com/quote/6082.HK/',
    '02688.HK': 'https://finance.yahoo.com/quote/2688.HK/',
    '02899.HK': 'https://finance.yahoo.com/quote/2899.HK/',
    '03360.HK': 'https://finance.yahoo.com/quote/3360.HK/',
    '03690.HK': 'https://finance.yahoo.com/quote/3690.HK/',
    '03692.HK': 'https://finance.yahoo.com/quote/3692.HK/',
    '03887.HK': 'https://finance.yahoo.com/quote/3887.HK/',
    '00100.HK': 'https://finance.yahoo.com/quote/0100.HK/',
    '03931.HK': 'https://finance.yahoo.com/quote/3931.HK/',
    '06181.HK': 'https://finance.yahoo.com/quote/6181.HK/',
    '06618.HK': 'https://finance.yahoo.com/quote/6618.HK/',
    '06862.HK': 'https://finance.yahoo.com/quote/6862.HK/',
    '06969.HK': 'https://finance.yahoo.com/quote/6969.HK/',
    '09626.HK': 'https://finance.yahoo.com/quote/9626.HK/',
    '09633.HK': 'https://finance.yahoo.com/quote/9633.HK/',
    '09660.HK': 'https://finance.yahoo.com/quote/9660.HK/',
    '09863.HK': 'https://finance.yahoo.com/quote/9863.HK/',
    '09926.HK': 'https://finance.yahoo.com/quote/9926.HK/',
    '09956.HK': 'https://finance.yahoo.com/quote/9956.HK/',
    '09979.HK': 'https://finance.yahoo.com/quote/9979.HK/',
    '09985.HK': 'https://finance.yahoo.com/quote/9985.HK/',
    '09987.HK': 'https://finance.yahoo.com/quote/9987.HK/',
    '09988.HK': 'https://finance.yahoo.com/quote/9988.HK/',
    '09992.HK': 'https://finance.yahoo.com/quote/9992.HK/',
    '09995.HK': 'https://finance.yahoo.com/quote/9995.HK/',
}

# ==========================================
# 1. 代理配置 (隧道代理)
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
            # 原始: ...-session-zPDM-sessionTime-0
            # 逻辑: 如果 username 中包含 'session-', 尝试替换后面的 ID
            raw_username = parts[2]
            password = parts[3]
            
            # 尝试动态替换 session ID 以强制切换 IP
            if "session-" in raw_username:
                # 简单的字符串替换，或者重新构建 username
                # 这里假设原始字符串格式固定，直接替换 session-zPDM 为 session-{random}
                # 如果您的代理商不支持自定义 session ID，请恢复使用原始 raw_username
                
                # 方法 A: 直接追加/替换 (更稳健的方法是根据代理商文档)
                # 这里为了保险，我们先使用原始配置，但在请求失败时，
                # 实际上隧道代理通常会自动轮换，或者我们需要在 username 里改 session ID
                # 假设您的代理支持通过修改 session-xxx 来切换 IP：
                import re
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
# 0.1 数据源配置 (已更新为包含25年收盘价的数据)
# ==========================================
RAW_STOCK_DATA = """
00001.HK 长和 39.5578 52.8000 CKH HOLDINGS
00005.HK 汇丰控股 71.7606 122.2000 HSBC HOLDINGS
00006.HK 电能实业 51.2827 55.2500 POWER ASSETS
00016.HK 新鸿基地产 71.6159 94.3500 SHK PPT
00020.HK 商汤-W 1.4900 2.2000 SENSETIME-W
00066.HK 港铁公司 25.8285 29.7200 MTR CORPORATION
00101.HK 恒隆地产 5.7574 8.5800 HANG LUNG PPT
00135.HK 昆仑能源 8.0243 7.3800 KUNLUN ENERGY
00175.HK 吉利汽车 14.5409 17.9400 GEELY AUTO
00179.HK 德昌电机控股 10.6501 29.7400 JOHNSON ELEC H
00189.HK 东岳集团 8.0326 10.8400 DONGYUE GROUP
00241.HK 阿里健康 3.3200 5.0600 ALI HEALTH
00257.HK 光大环境 3.6600 4.8200 EB ENVIRONMENT
00267.HK 中信股份 8.7331 12.0600 CITIC
00285.HK 比亚迪电子 41.2527 33.6400 BYD ELECTRONIC
00291.HK 华润啤酒 24.3977 26.2200 CHINA RES BEER
00371.HK 北控水务集团 2.3567 2.4600 BJ ENT WATER
00388.HK 香港交易所 286.8313 407.8000 HKEX
00425.HK 敏实集团 14.8061 31.7200 MINTH GROUP
00522.HK ASMPT 74.1891 77.7000 ASMPT
00551.HK 裕元集团 15.5794 15.9600 YUE YUEN IND
00669.HK 创科实业 99.9402 89.9500 TECHTRONIC IND
00688.HK 中国海外发展 11.9340 12.2500 CHINA OVERSEAS
00700.HK 腾讯控股 413.3913 599.0000 TENCENT
00728.HK 中国电信 4.6337 5.4000 CHINA TELECOM
00762.HK 中国联通 7.0259 7.7600 CHINA UNICOM
00772.HK 阅文集团 25.2000 32.9000 CHINA LIT
00788.HK 中国铁塔 10.1192 11.5600 CHINA TOWER
00836.HK 华润电力 17.9231 17.2600 CHINA RES POWER
00883.HK 中国海洋石油 17.7841 21.2800 CNOOC
00939.HK 建设银行 5.9098 7.6700 CCB
00941.HK 中国移动 72.1725 81.7000 CHINA MOBILE
00960.HK 龙湖集团 9.6647 8.5400 LONGFOR GROUP
00968.HK 信义光能 3.0995 2.9700 XINYI SOLAR
00981.HK 中芯国际 31.8000 71.3500 SMIC
00992.HK 联想集团 9.7029 9.2600 LENOVO GROUP
01024.HK 快手-W 41.0798 63.7500 KUAISHOU-W
01093.HK 石药集团 4.6477 8.4400 CSPC PHARMA
01109.HK 华润置地 21.3822 27.2000 CHINA RES LAND
01171.HK 兖矿能源 8.2137 9.6000 YANKUANG ENERGY
01177.HK 中国生物制药 3.1563 6.1800 SINO BIOPHARM
01208.HK 五矿资源 2.5600 8.8100 MMG
01209.HK 华润万象生活 27.2512 42.9800 CHINA RES MIXC
01211.HK 比亚迪股份 87.8953 95.1000 BYD COMPANY
01299.HK 友邦保险 54.7934 80.1000 AIA
01308.HK 海丰国际 18.5210 27.9000 SITC
01347.HK 华虹半导体 21.6500 74.1000 HUA HONG SEMI
01357.HK 美图公司 2.8637 6.9700 MEITU
01378.HK 中国宏桥 10.9760 32.5400 CHINAHONGQIAO
01398.HK 工商银行 4.7902 6.2400 ICBC
01519.HK 极兔速递-W 6.1300 10.4700 J&T EXPRESS-W
01530.HK 三生制药 6.0315 24.2600 3SBIO
01548.HK 金斯瑞生物科技 9.8400 12.3900 GENSCRIPT BIO
01585.HK 雅迪控股 12.4786 11.3200 YADEA
01788.HK 国泰君安国际 1.0899 2.5400 GUOTAI JUNAN I
01801.HK 信达生物 36.6000 76.2500 INNOVENT BIO
01810.HK 小米集团-W 34.5000 39.2000 XIAOMI-W
01816.HK 中广核电力 2.7375 2.9300 CGN POWER
01818.HK 招金矿业 10.9313 30.6600 ZHAOJIN MINING
01888.HK 建滔积层板 6.7637 13.1800 KB LAMINATES
01918.HK 融创中国 2.3200 1.3100 SUNAC
01951.HK 锦欣生殖 2.6900 2.3800 JXR
02007.HK 碧桂园 0.4850 0.4150 COUNTRY GARDEN
02018.HK 瑞声科技 37.2632 39.0800 AAC TECH
02020.HK 安踏体育 75.7687 80.3000 ANTA SPORTS
02057.HK 中通快递-W 145.9905 162.2000 ZTO EXPRESS-W
02097.HK 蜜雪集团 202.5000 410.8000 MIXUE GROUP
02228.HK 晶泰控股 5.9800 9.4600 XTALPI
02269.HK 药明生物 17.5600 31.4400 WUXI BIO
02313.HK 申洲国际 59.2075 60.9500 SHENZHOU INTL
02318.HK 中国平安 43.6123 65.3000 PING AN
02319.HK 蒙牛乳业 17.0034 14.8600 MENGNIU DAIRY
02328.HK 中国财险 11.8021 16.3200 PICC P&C
02331.HK 李宁 15.8962 18.6600 LI NING
02367.HK 巨子生物 48.7764 33.1400 GIANT BIOGENE
02382.HK 舜宇光学科技 68.2446 65.5500 SUNNY OPTICAL
02400.HK 心动公司 24.8832 65.2500 XD INC
02498.HK 速腾聚创 30.7000 36.6000 ROBOSENSE
02577.HK 英诺赛科 31.2500 78.3000 INNOSCIENCE
02588.HK 中银航空租赁 57.4167 72.6500 BOC AVIATION
02602.HK 万物云 18.7612 18.4100 ONEWO
02618.HK 京东物流 12.8000 11.4200 JD LOGISTICS
02628.HK 中国人寿 14.1252 27.4400 China Life
06082.HK 壁仞科技 0.0000 0.0000 Biren
02688.HK 新奥能源 53.2811 68.9000 ENN ENERGY
02899.HK 紫金矿业 13.7791 35.6600 ZIJIN MINING
03360.HK 远东宏信 5.2159 8.0400 FE HORIZON
03690.HK 美团-W 151.7000 102.8000 MEITUAN-W
03692.HK 翰森制药 17.0889 36.0800 HANSOH PHARMA
03887.HK HLDGS 0.0000 6.6600 HASHKEY HLDGS 
00100.HK MiniMax 0.0000 165.0000 MiniMax
03931.HK 中创新航 12.8600 25.1000 CALB
06181.HK 老铺黄金 235.3051 618.0000 LAOPU GOLD
06618.HK 京东健康 28.1000 55.5500 JD HEALTH
06862.HK 海底捞 15.0159 14.2000 HAIDILAO
06969.HK 思摩尔国际 13.1256 11.8500 SMOORE INTL
09626.HK 哔哩哔哩-W 142.0000 192.0000 BILIBILI-W
09633.HK 农夫山泉 33.2278 46.8400 NONGFU SPRING
09660.HK 地平线机器人-W 3.6000 8.6100 HORIZONROBOT-W
09863.HK 零跑汽车 32.5500 48.7400 LEAPMOTOR
09926.HK 康方生物 60.7000 113.1000 AKESO
09956.HK 安能物流 7.8240 11.8200 ANE
09979.HK 绿城管理控股 2.9276 2.7700 GREENTOWN MGMT
09985.HK 卫龙美味 6.9407 11.2700 WL DELICIOUS
09987.HK 百胜中国 366.4606 368.2000 YUM CHINA
09988.HK 阿里巴巴-W 81.0392 142.6000 BABA-W
09992.HK 泡泡玛特 89.2825 189.3000 POP MART
09995.HK 荣昌生物 14.4000 71.8500 REMEGEN
"""

# ==========================================
# 0.2 域名映射表 (用于获取 Google Favicon)
# ==========================================
TICKER_DOMAIN_MAP = {
    # 互联网/科技巨头
    '00700': 'tencent.com', '09988': 'taobao.com', '01810': 'mi.com', '03690': 'meituan.com',
    '01024': 'kuaishou.com', '09626': 'bilibili.com', '00981': 'smics.com', '00020': 'sensetime.com',
    '00100': 'minimax.io', '00772': 'yuewen.com', '01357': 'meitu.com', '02400': 'xd.com',
    '09992': 'popmart.com', '00992': 'lenovo.com', '06618': 'jdhealth.com', '00241': 'alihealth.cn/',
    '02618': 'jdl.com',

    # 汽车/新能源/制造
    '01211': 'byd.com', '00175': 'geely.com', '09863': 'leapmotor.com', '02018': 'aactechnologies.com',
    '02382': 'sunnyoptical.com', '06969': 'smooreholdings.com', '00669': 'ttigroup.com',
    '01585': 'yadea.com', '00968': 'xinyisolar.com', '00425': 'minthgroup.com',

    # 消费
    '02020': 'anta.com', '02331': 'lining.com', '09633': 'nongfuspring.com', '06862': 'haidilao.com',
    '09987': 'yumchina.com', '02319': 'mengniu.com.cn', '00291': 'crbeer.com.hk', '02367': 'giantbiogene.com',

    # 金融
    '02318': 'pingan.com', '00939': 'ccb.com', '00005': 'hsbc.com', '01299': 'aia.com',
    '00388': 'hkex.com.hk', '01398': 'icbc.com.cn', '02628': 'chinalife.com.cn',
    '02328': 'picc.com.cn', '01788': 'gtja.com',

    # 生物医药
    '02269': 'wuxibiologics.com', '01801': 'innoventbio.com', '01093': 'cspc.com.hk',
    '01177': 'sinobiopharm.com', '01548': 'genscript.com', '03692': 'hansoh.cn',

    # 能源/资源
    '02899': 'zijinmining.com', '00883': 'cnoocltd.com', '01378': 'hongqiaochina.com',
    '01171': 'yankuang.com.cn', '02688': 'ennenergy.com', '00836': 'cr-power.com',

    # 地产/综合
    '01109': 'crland.com.hk', '00001': 'ckh.com.hk', '00016': 'shkp.com', '00688': 'coli.com.hk',
    '00960': 'longfor.com', '00267': 'citic.com', '01918': 'sunac.com.cn', '02007': 'bgy.com.cn',

    # 运营商/公用
    '00941': 'chinamobileltd.com', '00728': 'chinatelecom-h.com', '00762': 'chinaunicom.com.hk',
    '00788': 'chinatowercom.cn', '00066': 'mtr.com.hk', '01519': 'jtexpress.com', '02057': 'zto.com'
}

# ==========================================
# 1. 核心配置：分组定义
# ==========================================
GROUPS_CONFIG = [
    {
        "title": "🏆 核心资产",
        "sort_mode": "fixed",
        "tickers": ['00700', '09988', '01810', '03690', '00981', '01211', '02269', '01801', '02899', '00883', '01378',
                    '02318', '00388', '01299', '00005', '09992', '02020', '00941']
    },
    {
        "title": "🌐 互联网科技",
        "sort_mode": "market_cap",
        "tickers": ['00700', '09988', '01810', '03690', '01024', '09626', '02228', '00020', '00100', '00772', '01357',
                    '02400']
    },
    {
        "title": "💾 半导体/硬件",
        "sort_mode": "market_cap",
        "tickers": ['00981', '01347', '02577', '00992', '06969', '02382', '02018', '09660', '00285', '01888', '06082',
                    '02498']
    },
    {
        "title": "🛍️ 大消费",
        "sort_mode": "market_cap",
        "tickers": ['09992', '02020', '06181', '02331', '09633', '06862', '09987', '02319', '00291', '02097', '02367',
                    '09985']
    },
    {
        "title": "💰 金融",
        "sort_mode": "market_cap",
        "tickers": ['02318', '00939', '01299', '02628', '00388', '00005', '02328', '02588', '03360', '03887', '01398',
                    '01788']
    },
    {
        "title": "🧬 生物科技",
        "sort_mode": "market_cap",
        "tickers": ['01801', '02269', '01093', '09926', '01530', '06618', '00241', '09995', '03692', '01177', '01548',
                    '01951']
    },
    {
        "title": "🏙️ 综合与地产",
        "sort_mode": "market_cap",
        "tickers": ['01109', '00001', '00016', '00688', '00267', '01918', '00960', '02602', '09979', '00101', '02007',
                    '01209']
    },
    {
        "title": "⚡ 能源材料",
        "sort_mode": "market_cap",
        "tickers": ['02899', '00883', '01378', '01208', '01818', '01171', '02688', '00836', '01816', '00135', '00189',
                    '00006']
    },
    {
        "title": "📡 运营商及公用事业",
        "sort_mode": "market_cap",
        "tickers": ['00941', '00728', '00762', '00788', '00066', '01519', '00371', '00257', '02618', '01308', '09956',
                    '02057']
    },
    {
        "title": "🏭 制造业",
        "sort_mode": "market_cap",
        "tickers": ['01211', '00175', '09863', '00669', '02313', '00522', '00968', '00179', '03931', '01585', '00425',
                    '00551']
    }
]

# ==========================================
# 2. 数据处理逻辑
# ==========================================
def parse_static_data(raw_text):
    """解析用户提供的静态文本数据"""
    static_map = {}
    lines = raw_text.strip().split('\n')
    for line in lines:
        if not line.strip(): continue
        # 使用 split() 默认分割空格，处理不定长空格
        parts = line.split()
        
        # 格式: 代码 中文简称 24年收盘 25年收盘 英文简称
        # 注意：英文简称可能包含空格，需要特殊处理
        if len(parts) >= 5:
            full_ticker = parts[0].strip()
            # 提取数字部分用于匹配
            ticker_code = full_ticker.split('.')[0]
            
            name_cn = parts[1].strip()
            
            try:
                price_24 = float(parts[2])
                price_25 = float(parts[3])
            except:
                price_24 = 0.0
                price_25 = 0.0
            
            # 剩下的部分重组为英文名
            name_en = " ".join(parts[4:]).strip()
            
            static_map[ticker_code] = {
                'name_en': name_en,
                'name_cn': name_cn,
                'price_24': price_24,
                'price_25': price_25
            }
    return static_map

def get_yahoo_data(ticker_code):
    """从 Yahoo Finance 获取数据 (带自动重试和代理轮换机制)"""
    global CURRENT_PROXY
    
    # 格式化股票代码
    try:
        clean_code = f"{int(ticker_code):04d}"
        symbol = f"{clean_code}.HK"
    except:
        symbol = f"{ticker_code}.HK"
    
    data = {
        'current_price': 0.0,
        'daily_change': 0.0,
        'market_cap': 0.0,
        'pe_ttm': 0.0
    }
    
    # 最大重试次数
    max_retries = 3
    
    for attempt in range(max_retries):
        # 1. 确保有代理
        if not CURRENT_PROXY:
            CURRENT_PROXY = get_proxy()
            if CURRENT_PROXY:
                os.environ['HTTP_PROXY'] = CURRENT_PROXY
                os.environ['HTTPS_PROXY'] = CURRENT_PROXY

        try:
            # 2. 初始化 Ticker
            ticker = yf.Ticker(symbol)
            
            # 3. 获取数据 (yfinance 内部使用 requests)
            # 访问 .info 属性会触发网络请求
            info = ticker.info
            
            # --- 如果成功获取 info，提取数据并跳出循环 ---
            
            # 价格
            price = info.get('currentPrice') or info.get('regularMarketPrice') or info.get('previousClose')
            if price:
                data['current_price'] = float(price)
            
            # 涨跌幅
            prev_close = info.get('previousClose')
            if data['current_price'] and prev_close:
                change_pct = ((data['current_price'] - prev_close) / prev_close) * 100
                data['daily_change'] = change_pct
            
            # 市值
            mcap = info.get('marketCap')
            if mcap:
                data['market_cap'] = float(mcap) / 100000000.0
            
            # PE
            pe = info.get('trailingPE')
            if pe:
                data['pe_ttm'] = float(pe)
            else:
                data['pe_ttm'] = -1.0
                
            # 成功获取，退出重试循环
            break

        except Exception as e:
            print(f"  ⚠️ 获取 {symbol} 失败 (第 {attempt + 1} 次): {e}")
            
            # 关键修改：如果失败（包括超时），强制刷新代理 IP
            print("  🔄 正在切换新代理 IP 并重试...")
            CURRENT_PROXY = get_proxy() # 获取新的 Session ID
            if CURRENT_PROXY:
                os.environ['HTTP_PROXY'] = CURRENT_PROXY
                os.environ['HTTPS_PROXY'] = CURRENT_PROXY
            
            # 稍微等待一下再重试，避免请求过于密集
            time.sleep(2)
            
            # 如果是最后一次尝试依然失败，则保持默认值 0.0
            if attempt == max_retries - 1:
                print(f"  ❌ {symbol} 最终获取失败，跳过。")

    return data

def get_all_stocks_data(groups_config, static_data):
    # 初始化代理环境
    global CURRENT_PROXY
    CURRENT_PROXY = get_proxy()
    if CURRENT_PROXY:
        os.environ['HTTP_PROXY'] = CURRENT_PROXY
        os.environ['HTTPS_PROXY'] = CURRENT_PROXY
        print(f"✅ 初始代理环境已设置")
    else:
        print("⚠️ 警告: 未能获取代理，将尝试直连...")
    
    all_tickers = list(set([t for group in groups_config for t in group['tickers']]))
    print(f"📊 正在初始化数据获取 (Yahoo Finance)，共 {len(all_tickers)} 只股票...")
    
    stocks_data = {}
    count = 0
    total = len(all_tickers)
    
    for symbol in all_tickers:
        count += 1
        # 在控制台显示转换后的 Yahoo 代码，方便调试
        try:
            display_symbol = f"{int(symbol):04d}.HK"
        except:
            display_symbol = symbol
        
        print(f"  处理进度: {count}/{total} ({display_symbol}) ...", end="\r")
        
        # 1. 获取静态信息
        static_info = static_data.get(symbol, {})
        name_cn = static_info.get('name_cn', symbol)
        name_en = static_info.get('name_en', symbol)
        price_24 = static_info.get('price_24', 0.0)
        price_25 = static_info.get('price_25', 0.0)
        
        # 2. 获取动态信息 (Yahoo) - 现在包含自动重试机制
        yf_data = get_yahoo_data(symbol)
        
        current_price = yf_data['current_price']
        
        # 3. 计算 YTD
        ytd_change = 0.0
        yoy_25_change = 0.0
        
        # 特殊处理：06082 壁仞科技 (2026上市，基准为IPO价格 19.60)
        is_biren = '06082' in symbol
        
        if is_biren:
            ipo_price = 19.6000
            if current_price > 0:
                ytd_change = ((current_price - ipo_price) / ipo_price) * 100
            yoy_25_change = None  # 标记为 N/A
        else:
            # 常规逻辑
            # 如果当前价格为0（获取失败），暂时用25年收盘价代替
            if current_price == 0 and price_25 > 0:
                current_price = price_25
            
            if price_25 > 0 and current_price > 0:
                ytd_change = ((current_price - price_25) / price_25) * 100
            
            # 4. 计算 25 YoY (25年收盘价 vs 24年收盘价)
            if price_24 > 0 and price_25 > 0:
                yoy_25_change = ((price_25 - price_24) / price_24) * 100
        
        # 5. 组装数据
        stocks_data[symbol] = {
            'symbol': display_symbol,  # 使用转换后的代码显示 (如 0700.HK)
            'ticker_code': symbol,    # 原始代码 (如 00700)，用于查找 URL
            'name': name_cn,
            'name_en': name_en,
            'domain': TICKER_DOMAIN_MAP.get(symbol, None),
            'current_price': current_price,
            'daily_change': yf_data['daily_change'],
            'ytd_change': ytd_change,
            'yoy_25_change': yoy_25_change,
            'market_cap': yf_data['market_cap'],
            'pe_ttm': yf_data['pe_ttm']
        }
        
        # 稍微的延时，避免过于频繁
        time.sleep(0.5)
        
    print("\n✅ 数据获取完成")
    return stocks_data

# ==========================================
# 3. 辅助函数 (UI 相关)
# ==========================================
def format_market_cap_hkd(market_cap):
    if not market_cap or market_cap == 0: return ""
    try:
        return f"{market_cap:,.0f}亿"
    except:
        return ""

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
# 4. HTML 生成逻辑
# ==========================================
def generate_html(all_data):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
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
    
    html_head = f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="default">
    <meta name="apple-mobile-web-app-title" content="HK Market">
    <!-- 禁止缓存 -->
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
    <meta http-equiv="Pragma" content="no-cache" />
    <meta http-equiv="Expires" content="0" />
    <!-- 启用点击链接 -->
    <meta name="format-detection" content="telephone=no">
    <title>HK Market Watch</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }}
        body {{ background-color: #f3f4f6; padding: 10px; }}
        .container {{ max-width: 1000px; margin: 0 auto; }}
        
        .main-header {{ text-align: center; margin-bottom: 20px; padding: 20px 15px; background: white; border-radius: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }}
        .main-header h1 {{ font-size: 26px; color: #111827; margin-bottom: 8px; font-weight: 800; letter-spacing: -0.5px; }}
        
        /* 新增元数据样式 */
        .meta-info {{ color: #6b7280; font-size: 12px; line-height: 1.6; }}
        .meta-info.source {{ font-weight: 500; color: #4b5563; }}
        .meta-info.email {{ color: #9ca3af; font-size: 11px; margin-top: 2px; }}
        
        /* 导航栏样式 */
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
        .nav-bar a {{
            text-decoration: none;
            color: #1f2937;
            transition: color 0.2s;
        }}
        .nav-bar a:hover {{
            color: #2563eb;
        }}
        .nav-icon {{
            font-size: 16px;
        }}
        .nav-sep {{
            color: #d1d5db;
            font-weight: 400;
        }}

        .section {{ background: white; border-radius: 16px; padding: 15px 10px; margin-bottom: 20px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); }}
        
        .section-header {{ margin-bottom: 12px; border-bottom: 1px solid #f3f4f6; padding-bottom: 8px; }}
        .section-title {{ font-size: 18px; font-weight: 800; color: #1f2937; display: flex; align-items: center; }}
        
        .grid {{ 
            display: grid; 
            grid-template-columns: repeat(3, 1fr); 
            gap: 6px; 
        }}
        
        .card {{
            min-height: 180px;
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
            position: absolute; 
            top: 4px; left: 4px; 
            background: rgba(255,255,255,0.9); 
            padding: 1px 4px; 
            border-radius: 4px; 
            font-size: 9px; 
            font-weight: 700; 
            color: #4b5563; 
            z-index: 10;
            box-shadow: 0 1px 1px rgba(0,0,0,0.1);
        }}
        
        .logo-img {{ 
            width: 28px; 
            height: 28px; 
            border-radius: 50%; 
            margin-bottom: 4px; 
            margin-top: 14px; 
            object-fit: contain;
            background-color: white; 
            padding: 2px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        
        .logo-placeholder {{
            width: 28px; 
            height: 28px; 
            border-radius: 50%; 
            margin-bottom: 4px; 
            margin-top: 14px;
            background: rgba(255,255,255,0.3);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 10px;
            color: #555;
            font-weight: bold;
        }}
        
        .ticker {{ font-size: 14px; font-weight: 900; line-height: 1.1; }}
        
        .name-cn {{ 
            font-size: 11px; 
            font-weight: 600; 
            margin-top: 2px; 
            margin-bottom: 1px;
            white-space: nowrap; 
            overflow: hidden; 
            text-overflow: ellipsis; 
            max-width: 100%; 
        }}
        
        .name-en {{
            font-size: 9px;
            font-weight: 500;
            opacity: 0.85;
            margin-bottom: 6px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            max-width: 100%;
            text-transform: uppercase;
        }}
        
        .pill {{ 
            width: 100%; 
            padding: 3px 0; 
            border-radius: 6px; 
            text-align: center; 
            margin-bottom: 3px; 
            font-weight: 700; 
            display: flex; 
            align-items: center; 
            justify-content: center; 
            backdrop-filter: blur(4px); 
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
            <h1>HK Market Watch</h1>
            <div class="meta-info">Update: {current_time}</div>
            <div class="meta-info source">Data Source: Yahoo Finance 15m delay/15m update</div>
            <div class="meta-info email">jasonlee325@gmail.com</div>
        </div>
        {nav_html}
    """
    
    html_body = ""
    
    for group in GROUPS_CONFIG:
        group_items = []
        for ticker in group['tickers']:
            if ticker in all_data:
                group_items.append(all_data[ticker])
        
        if group['sort_mode'] == 'market_cap':
            group_items.sort(key=lambda x: float(x['market_cap']) if x['market_cap'] else 0, reverse=True)
        
        if not group_items: continue
        
        html_body += f"""
        <div class="section">
            <div class="section-header">
                <div class="section-title">{group['title']}</div>
            </div>
            <div class="grid">
        """
        
        for item in group_items:
            daily_change = item['daily_change']
            ytd_change = item['ytd_change']
            yoy_25_change = item['yoy_25_change']
            pe_val = item['pe_ttm']
            domain = item['domain']
            
            if pe_val > 0:
                pe_str = f"{pe_val:.1f}"
            elif pe_val < 0:
                pe_str = "亏损"  # 简化显示
            else:
                pe_str = "-"
            
            bg_color, text_color, pill_bg = get_color_style(daily_change)
            ytd_text_color = "#ffffff" if text_color == "#ffffff" else ('#dc2626' if ytd_change >= 0 else '#166534')
            
            # 处理 YoY 显示逻辑
            if yoy_25_change is None:
                yoy_display_str = "N/A"
                yoy_text_color = "#9ca3af" # 灰色
            else:
                yoy_display_str = f"{yoy_25_change:+.1f}%"
                yoy_text_color = "#ffffff" if text_color == "#ffffff" else ('#dc2626' if yoy_25_change >= 0 else '#166534')
            
            # Logo 处理逻辑
            if domain:
                logo_html = f'<img class="logo-img" src="https://www.google.com/s2/favicons?domain={domain}&sz=64" alt="{item["name"]}" onerror="this.style.display=\'none\'" />'
            else:
                logo_html = f'<div class="logo-placeholder">{item["symbol"][-2:]}</div>'

            # 获取 Yahoo Finance URL - 使用 ticker_code (5位代码) 来查找
            ticker_code = item.get('ticker_code', item['symbol'])
            yahoo_url = TICKER_URL_MAP.get(f'{ticker_code}.HK', '')
            # 移动端去掉 target="_blank"，避免点击无反应
            card_link = f'<a href="{yahoo_url}" style="text-decoration: none; color: inherit;">' if yahoo_url else ''

            html_body += f"""
                {card_link}<div class="card" style="background-color: {bg_color}; color: {text_color};">
                    <div class="badge-cap">{format_market_cap_hkd(item['market_cap'])}</div>
                    {logo_html}
                    <div class="ticker">{item['symbol']}</div>
                    <div class="name-cn">{item['name']}</div>
                    <div class="name-en">{item['name_en']}</div>

                    <div class="pill pill-price" style="background: {pill_bg}; color: {text_color};">
                        ${item['current_price']:.2f}
                    </div>
                    <div class="pill pill-change" style="background: {pill_bg}; color: {text_color};">
                        {'+' if daily_change >= 0 else ''}{daily_change:.2f}%
                    </div>
                    <div class="pill pill-ytd" style="background: {pill_bg}; color: {ytd_text_color};">
                        YTD {ytd_change:+.1f}%
                    </div>
                    <div class="pill pill-yoy" style="background: {pill_bg}; color: {yoy_text_color};">
                        25 YoY {yoy_display_str}
                    </div>
                    <div class="pe-info">PE(TTM) {pe_str}</div>
                </div>{"</a>" if yahoo_url else ""}
            """
            
        html_body += """
            </div>
        </div>
        """
        
    html_footer = f"""
        {nav_html}
    </div>
    <script>
    // 为卡片添加点击事件处理
    document.addEventListener('DOMContentLoaded', function() {{
        var cards = document.querySelectorAll('.card');
        cards.forEach(function(card) {{
            card.addEventListener('click', function(e) {{
                // 查找父级的 <a> 标签
                var link = this.closest('a');
                if (link) {{
                    // 如果找到链接，直接跳转
                    window.location.href = link.href;
                }}
            }});
        }});
    }});
    </script>
    </body>
    </html>
    """

    return html_head + html_body + html_footer

# ==========================================
# 5. 主程序
# ==========================================
def main():
    # 1. 解析静态数据
    static_data = parse_static_data(RAW_STOCK_DATA)
    
    # 2. 获取动态数据 (Yahoo Finance)
    data = get_all_stocks_data(GROUPS_CONFIG, static_data)
    if not data: return
    
    # 3. 生成 HTML
    html_content = generate_html(data)
    
    filename = "/www/wwwroot/efinmap.com/hk.html"
    # 确保目录存在
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    print(f"\n✨ 成功生成 HTML 文件: {os.path.abspath(filename)}")

if __name__ == "__main__":
    main()