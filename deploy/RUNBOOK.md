# efinmap 部署 Runbook

目标服务器：Debian 12+ Linux，已绑定域名 `efinmap.com` 的 A 记录到该服务器 IP。

执行人身份：`root` 或可 `sudo` 的普通用户。下文 `sudo` 命令在 root 下可省略。

---

## 0. 前置检查（本地）

部署前确认本地以下文件已配置好：

```bash
# 在 C:\efinmap\
cat .env                    # 存在，但只是开发用的占位密码
cat .env.example            # 模板，将上传到服务器
cat collectors/proxy.py     # 已读 PROXY_CONFIG env，无硬编码凭证
grep -n "make_interval\|time(16, 0)\|allow_origins\|SERVE_STATIC" api/main.py api/routers/market.py
```

把以下信息记下来，部署中要填进 `.env`：

| 变量 | 值 |
|------|-----|
| 数据库密码 | `<生成一个 32 字节随机串>` |
| 代理 PROXY_CONFIG | `blurpath.net:15132:pdd6wxr7bg-...:NerxBq` |
| 域名 | `efinmap.com` |

生成密码示例：`openssl rand -base64 24`

---

## 1. 服务器基础环境

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y postgresql nginx python3 python3-venv python3-pip \
                    git certbot python3-certbot-nginx ufw

# 防火墙：只开 22/80/443
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw --force enable
sudo ufw status
```

验证：
```bash
systemctl is-active postgresql nginx    # 两行都应输出 active
psql --version                          # PostgreSQL 15+
python3 --version                       # 3.11+
```

---

## 2. 上传代码到 `/opt/efinmap/`

**推荐 git 路径**（先在本地 `git init && git commit`，然后推到 GitHub 私有 repo）：

```bash
sudo mkdir -p /opt/efinmap
sudo chown $USER:$USER /opt/efinmap
git clone git@github.com:你/efinmap.git /opt/efinmap
```

**或 scp 直传**（适合不进 git 的情况）：

```bash
# 在本地 Windows
scp -r C:/efinmap/* user@server:/tmp/efinmap/
# 在服务器
sudo mv /tmp/efinmap /opt/efinmap
```

无论哪种方式，**`.env` 必须不存在于服务器上**（git 已 ignore，scp 时手动剔除）。

验证：
```bash
ls /opt/efinmap/                 # 应有 api/ collectors/ frontend/ deploy/ .env.example
test ! -f /opt/efinmap/.env && echo "OK: 没有 .env"
```

---

## 3. 创建 Python venv + 安装依赖

```bash
cd /opt/efinmap
python3 -m venv venv
venv/bin/pip install --upgrade pip
venv/bin/pip install -r api/requirements.txt
```

验证：
```bash
venv/bin/python -c "import fastapi, psycopg, yfinance; print('deps OK')"
```

---

## 4. 配置 `.env`

```bash
cd /opt/efinmap
cp .env.example .env
# 用强密码替换占位符
DB_PASS=$(openssl rand -base64 24 | tr -d '/+=')
sed -i "s|CHANGE_ME_STRONG_PASSWORD|$DB_PASS|g" .env
# 把代理填进去（手动 vim/nano）
nano .env
# 文件最终应像：
#   DATABASE_URL=postgresql://efinmap_user:<32字符密码>@localhost:5432/efinmap
#   PROXY_CONFIG=blurpath.net:15132:pdd6wxr7bg-...:NerxBq

# 把同样的 DB_PASS 写进 init_db.sql
sed -i "s|CHANGE_ME_STRONG_PASSWORD|$DB_PASS|g" deploy/init_db.sql
echo "DB_PASS=$DB_PASS"  # 记下来，万一脚本失败需要手动重试
```

---

## 5. 初始化 PostgreSQL

```bash
sudo -u postgres psql -f /opt/efinmap/deploy/init_db.sql
```

应输出 `CREATE DATABASE / CREATE ROLE / GRANT` 等。

灌入种子数据（ticker 元数据 + 2024/2025 年末基准价）：

```bash
cd /opt/efinmap
venv/bin/python deploy/seed_data.py
# 应打印：Seeding US tickers... HK ... Asia ... benchmarks ... Seed complete.
```

验证：
```bash
sudo -u postgres psql -d efinmap -c "SELECT COUNT(*) FROM tickers;"
# 应 > 250

sudo -u postgres psql -d efinmap -c "SELECT COUNT(*) FROM annual_benchmarks WHERE year=2025;"
# 应 ~ 250

# 测试用户能连：
psql "postgresql://efinmap_user:$DB_PASS@localhost:5432/efinmap" -c "\dt"
```

---

## 6. 启动 FastAPI（systemd）

```bash
sudo cp /opt/efinmap/deploy/efinmap-api.service /etc/systemd/system/
sudo chown -R www-data:www-data /opt/efinmap
sudo systemctl daemon-reload
sudo systemctl enable --now efinmap-api
```

验证：
```bash
systemctl status efinmap-api          # active (running)
journalctl -u efinmap-api -n 30 --no-pager    # 看到 "Application startup complete"

# 直接打 API（数据还没采集，应回 503）：
curl -i http://127.0.0.1:8000/api/v1/market/us
# HTTP/1.1 503  → 正常，因为 price_snapshots 还是空表
```

---

## 7. nginx 反向代理（HTTP）

```bash
sudo cp /opt/efinmap/deploy/nginx.conf /etc/nginx/sites-available/efinmap
sudo ln -sf /etc/nginx/sites-available/efinmap /etc/nginx/sites-enabled/efinmap
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t              # syntax OK
sudo systemctl reload nginx
```

验证（从外网或服务器本地）：
```bash
curl -I http://efinmap.com/                # 200, 返回 index.html
curl -i http://efinmap.com/api/v1/market/us # 503 (空数据库)
```

---

## 8. 配置 cron（数据采集 + 清理）

```bash
sudo mkdir -p /var/log/efinmap
sudo chown www-data:www-data /var/log/efinmap

sudo crontab -u www-data /opt/efinmap/deploy/crontab.txt
sudo crontab -u www-data -l    # 验证已生效

# 日志轮转
sudo cp /opt/efinmap/deploy/logrotate-efinmap /etc/logrotate.d/efinmap
sudo logrotate -d /etc/logrotate.d/efinmap   # dry-run，无报错即可
```

立即手动触发一次美股采集，确认链路通：

```bash
cd /opt/efinmap/collectors
sudo -u www-data /opt/efinmap/venv/bin/python collect_us.py | head -30
# 应看到 "AAPL OK $XXX +X.XX%" 之类
```

回头查 API 应有数据：

```bash
curl -s http://efinmap.com/api/v1/market/us | head -c 500
# 应看到 {"market_status":"...","groups":[...]}
```

---

## 9. 启用 HTTPS（certbot）

```bash
sudo certbot --nginx -d efinmap.com -d www.efinmap.com \
    --non-interactive --agree-tos -m jasonlee325@gmail.com --redirect
sudo systemctl enable --now certbot.timer    # 自动续期
```

certbot 会自动改 `/etc/nginx/sites-available/efinmap`，加 `listen 443 ssl` 和 HTTP→HTTPS 301。

验证：
```bash
curl -I https://efinmap.com/                          # 200
curl -I http://efinmap.com/                           # 301 → https
sudo certbot renew --dry-run                          # 测试续期
```

---

## 10. 切换 DNS（最后一步）

确认 `https://efinmap.com` 完全正常后，把 efinmap.com 的 A 记录从旧腾讯云 IP 改到新服务器 IP。TTL 默认 600 秒，一刻钟内全网生效。

旧腾讯云保留 1-2 周作为回退，确认新服务器稳定后再下线。

---

## 烟雾测试 checklist

切换 DNS 后逐项过一遍：

- [ ] `https://efinmap.com/` 显示 US 热力图，所有股票卡片有数据
- [ ] `https://efinmap.com/hk.html` 显示港股
- [ ] `https://efinmap.com/asia.html` 显示日韩台
- [ ] `https://efinmap.com/watchlist.html` 自选页可加载
- [ ] 在自选页输入 `AAPL`，能从已有数据加载
- [ ] 在自选页输入 `0388.HK`、`9984.T`，能加载
- [ ] 在自选页输入新 ticker（如 `RBLX`），能从 Yahoo 拉取并显示
- [ ] 删除自选股，刷新页面后保持删除状态（localStorage 工作）
- [ ] 浏览器 DevTools Console 无报错
- [ ] HTTP→HTTPS redirect 工作

---

## 常见错误排查

### `journalctl -u efinmap-api` 报 `psycopg.OperationalError: connection refused`
- PostgreSQL 没起来：`systemctl status postgresql`
- `.env` 密码和 init_db.sql 不一致：重新 `sed` 改两处后 `systemctl restart efinmap-api`

### API 返回 503 "No US data available yet"
- 没跑过 collector，或 collector 全失败
- 看 `/var/log/efinmap/us.log`，找 yfinance 报错。常见：代理失效（PROXY_CONFIG 写错）、yfinance 被限流
- 临时可空 `PROXY_CONFIG=` 让 collector 直连 Yahoo（看服务器 IP 是否能访问）

### nginx 502 Bad Gateway
- FastAPI 没起来：`systemctl status efinmap-api`
- FastAPI 监听端口不是 8000：`ss -tlnp | grep 8000`

### 自选股添加新 ticker 报 503 "YFinance not available"
- venv 没装 yfinance：`venv/bin/pip list | grep yfinance`
- 或者 `efinmap-api.service` 用的 python 不是 venv 里的：检查 `ExecStart` 路径

### certbot `Detail: ... Connection refused`
- DNS 还没指向新服务器，certbot 验证失败 → 先把 DNS 切过来再跑
- 或者 ufw 没放 80：`sudo ufw status`

### 港股代码采集了但前端不显示
- 它必须先在 `tickers` 表中（由 seed_data.py 灌入），collect_hk 不会自动 upsert ticker 元数据
- 解决：在 `seed_data.py` 的 `HK_TICKERS` 和 `HK_PRICES_2024/2025` 加新条目，重跑 `venv/bin/python deploy/seed_data.py`（INSERT ... ON CONFLICT DO UPDATE，安全幂等）

---

## 日常维护

### 数据库备份（建议每天凌晨）

```bash
# /etc/cron.daily/efinmap-backup
#!/bin/bash
BACKUP_DIR=/var/backups/efinmap
mkdir -p $BACKUP_DIR
sudo -u postgres pg_dump efinmap | gzip > $BACKUP_DIR/efinmap-$(date +%F).sql.gz
find $BACKUP_DIR -name "efinmap-*.sql.gz" -mtime +14 -delete
```

`chmod +x /etc/cron.daily/efinmap-backup`

### 跨年（2026 年 12 月底要做）

1. 从 yfinance 拉取所有 ticker 的 2026 年末收盘价
2. INSERT 到 `annual_benchmarks` (year=2026)
3. 改 `api/routers/market.py` 顶部：
   ```python
   CURRENT_YEAR = 2027
   BENCHMARK_YEAR = 2026
   ```
4. `systemctl restart efinmap-api`

### 添加新股票到既有 group

1. 在 `deploy/seed_data.py` 加 ticker 元数据 + 基准价
2. 在 `api/market_config.py` 对应 group 的 `symbols` 加代码
3. 在 `collectors/collect_us.py`（或 hk/asia）加 ticker
4. 服务器同步：`git pull && venv/bin/python deploy/seed_data.py && systemctl restart efinmap-api`
   （collectors 是 cron 自动跑的，不用手动重启）

### 升级代码

```bash
cd /opt/efinmap
sudo -u www-data git pull
sudo -u www-data venv/bin/pip install -r api/requirements.txt
sudo systemctl restart efinmap-api
sudo nginx -t && sudo systemctl reload nginx
```

---

## 回滚

旧腾讯云保留期内若新版出问题：

```bash
# 把 DNS A 记录改回旧腾讯云 IP
# 新服务器停服（不删数据，方便排查）：
sudo systemctl stop efinmap-api nginx
```
