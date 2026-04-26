/**
 * heatmap.js — shared rendering logic for all three market pages.
 * Replicates the Python color/layout logic from the original scripts.
 */

// ── Color helpers ──────────────────────────────────────────────────────────
function lerp(a, b, t) { return Math.round(a + (b - a) * t); }

function interpolateRGB(val, minVal, maxVal, start, end) {
  val = Math.max(minVal, Math.min(maxVal, val));
  const t = (val - minVal) / (maxVal - minVal);
  return `rgb(${lerp(start[0], end[0], t)},${lerp(start[1], end[1], t)},${lerp(start[2], end[2], t)})`;
}

function getColorStyle(change) {
  const THRESHOLD = 5.0;
  const WHITE      = [255, 255, 255];
  const DEEP_GREEN = [22,  163,  74];
  const DEEP_RED   = [220,  38,  38];
  const abs = Math.abs(change);

  let bgColor, textColor, pillBg;

  if (change >= 0) {
    bgColor   = abs < 0.5 ? 'rgb(255,255,255)' : interpolateRGB(abs, 0, THRESHOLD, WHITE, DEEP_GREEN);
    textColor = abs > 2.5 ? '#ffffff' : '#14532d';
    pillBg    = abs > 2.5 ? 'rgba(255,255,255,0.25)' : 'rgba(255,255,255,0.6)';
  } else {
    bgColor   = abs < 0.5 ? 'rgb(255,255,255)' : interpolateRGB(abs, 0, THRESHOLD, WHITE, DEEP_RED);
    textColor = abs > 2.5 ? '#ffffff' : '#7f1d1d';
    pillBg    = abs > 2.5 ? 'rgba(255,255,255,0.25)' : 'rgba(255,255,255,0.6)';
  }

  return { bgColor, textColor, pillBg };
}

// ── Formatters ──────────────────────────────────────────────────────────────
const INDEX_SYMBOLS = new Set(['SPX', 'IXIC', 'DJI', 'RUT']);

function fmtPrice(symbol, price) {
  if (INDEX_SYMBOLS.has(symbol)) return price.toFixed(1);
  if (price < 10)      return '$' + price.toFixed(2);
  if (price > 20000)   return '$' + (price / 1000).toFixed(0) + 'k';
  return '$' + price.toFixed(1);
}

function fmtCap(cap) {
  if (!cap || cap === 0) return '';
  const T = cap / 1e12, B = cap / 1e9;
  if (T >= 1) return T.toFixed(1) + 'T';
  if (B >= 1) return B.toFixed(1) + 'B';
  return (cap / 1e6).toFixed(0) + 'M';
}

function fmtCapHKD(cap) {
  // cap is in HKD hundred-millions (亿)
  if (!cap || cap === 0) return '';
  return cap.toFixed(0) + '亿';
}

function sign(v) { return v >= 0 ? '+' : ''; }

// ── Card renderer ───────────────────────────────────────────────────────────
/**
 * @param {object} s  - stock data object from API
 * @param {string} priceStr - pre-formatted price (caller handles HKD/USD/local)
 * @param {string} capStr   - pre-formatted market cap
 */
function renderCard(s, priceStr, capStr) {
  const { bgColor, textColor, pillBg } = getColorStyle(s.daily_chg);
  const ytdColor  = textColor === '#ffffff' ? '#ffffff' : (s.ytd_chg    >= 0 ? '#15803d' : '#b91c1c');
  const yoyColor  = textColor === '#ffffff' ? '#ffffff' : (s.yoy_25_chg >= 0 ? '#15803d' : '#b91c1c');

  const logo = s.domain
    ? `<img class="logo-img" src="https://www.google.com/s2/favicons?domain=${s.domain}&sz=128" onerror="this.style.display='none'">`
    : '';
  const peStr = s.pe_ratio && s.pe_ratio > 0 ? `PE ${Math.round(s.pe_ratio)}` : 'PE --';

  const yahooBase = 'https://finance.yahoo.com/quote/';
  const url = yahooBase + encodeURIComponent(s.symbol) + '/';

  return `
<a href="${url}" target="_blank" style="text-decoration:none;color:inherit;">
  <div class="asset-card" style="background-color:${bgColor};color:${textColor};">
    <div class="market-cap-badge">${capStr}</div>
    <div class="type-badge" style="color:${textColor}">${s.tag || ''}</div>
    <div class="card-header">
      <div class="logo-wrapper">${logo}</div>
      <div class="ticker-symbol">${s.symbol}</div>
      <div class="ticker-name">${s.name_cn}</div>
    </div>
    <div class="data-pills-container">
      <div class="data-pill" style="background:${pillBg};color:${textColor};opacity:0.9">${priceStr}</div>
      <div class="data-pill" style="background:${pillBg};color:${textColor}">${sign(s.daily_chg)}${s.daily_chg.toFixed(2)}%</div>
      <div class="data-pill" style="background:${pillBg};color:${ytdColor};font-size:9px">
        <span class="pill-label">YTD</span>${sign(s.ytd_chg)}${s.ytd_chg.toFixed(1)}%
      </div>
      <div class="data-pill" style="background:${pillBg};color:${yoyColor};font-size:9px">
        <span class="pill-label">25 YoY</span>${sign(s.yoy_25_chg)}${s.yoy_25_chg.toFixed(1)}%
      </div>
    </div>
    <div class="card-footer-pe" style="border-color:${textColor}20">${peStr}</div>
  </div>
</a>`;
}

// ── Section renderer ────────────────────────────────────────────────────────
function renderSection(group, priceFmt, capFmt) {
  const st = group.stats;
  const avgColor = st.avg_chg >= 0 ? '#059669' : '#dc2626';
  const cards = group.stocks.map(s => renderCard(s, priceFmt(s), capFmt(s))).join('');

  return `
<div class="section-card">
  <div class="section-title">${group.title}</div>
  <div class="grid">${cards}</div>
  <div class="stats-footer">
    <div class="stat-item"><span class="stat-title">上涨</span><span class="stat-value">${st.up}/${st.total}</span></div>
    <div class="stat-item"><span class="stat-title">平均</span><span class="stat-value" style="color:${avgColor}">${sign(st.avg_chg)}${st.avg_chg.toFixed(2)}%</span></div>
    <div class="stat-item"><span class="stat-title">今日最佳</span><span class="stat-value" style="color:#059669;font-size:11px">${st.best_day.symbol} ${sign(st.best_day.chg)}${st.best_day.chg.toFixed(1)}%</span></div>
    <div class="stat-item"><span class="stat-title">YTD 最佳</span><span class="stat-value" style="color:#059669;font-size:11px">${st.best_ytd.symbol} ${sign(st.best_ytd.chg)}${st.best_ytd.chg.toFixed(1)}%</span></div>
  </div>
</div>`;
}

// ── Main fetch-and-render ────────────────────────────────────────────────────
/**
 * @param {string} apiUrl       - e.g. '/api/v1/market/us'
 * @param {string} containerId  - DOM id of the container div
 * @param {string} headerTitle  - page H1 text
 * @param {string} marketType   - 'US' | 'HK' | 'ASIA'
 */
async function fetchAndRender(apiUrl, containerId, headerTitle, marketType) {
  const container = document.getElementById(containerId);

  try {
    const resp = await fetch(apiUrl);
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    const data = await resp.json();

    const updatedAt = data.updated_at
      ? new Date(data.updated_at).toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai', hour12: false })
      : '--';
    const statusOpen = data.market_status === 'OPEN';
    const statusBadge = statusOpen
      ? `<span class="status-badge status-open">🟢 Market Open</span>`
      : `<span class="status-badge status-closed">🔴 Market Closed</span>`;

    // Price + cap formatters per market type
    const priceFmt = marketType === 'ASIA'
      ? s => s.price > 0 ? s.price.toFixed(s.price >= 100 ? 0 : 1) : '--'
      : s => fmtPrice(s.symbol, s.price);

    const capFmt = s => fmtCap(s.market_cap);

    const sections = data.groups.map(g => renderSection(g, priceFmt, capFmt)).join('');

    container.innerHTML = `
<div class="main-header">
  <h1>${headerTitle}</h1>
  <p>${updatedAt} (CST)</p>
  <div style="font-size:10px;color:#6b7280;margin:4px 0 8px">
    <div>Data: Yahoo Finance (15min update)</div>
    <div><a href="mailto:jasonlee325@gmail.com" style="color:inherit;text-decoration:none">jasonlee325@gmail.com</a></div>
  </div>
  ${statusBadge}
</div>
${NAV_HTML}
${sections}
${NAV_HTML}`;
  } catch (err) {
    container.innerHTML = `<div style="text-align:center;padding:40px;color:#6b7280">
      <p>数据加载失败，请刷新重试。</p><p style="font-size:12px">${err.message}</p>
    </div>`;
  }
}

// ── Shared nav ───────────────────────────────────────────────────────────────
const NAV_HTML = `
<div class="nav-bar">
  <span class="nav-icon">👉</span>
  <a href="/index.html">US</a>
  <span class="nav-sep">|</span>
  <a href="/hk.html">HK</a>
  <span class="nav-sep">|</span>
  <a href="/asia.html">JP/KR/TW</a>
  <span class="nav-sep">|</span>
  <a href="/watchlist.html">自选</a>
</div>`;

// ── Auto-refresh (10 min since last load) ────────────────────────────────────
let _lastLoad = Date.now();
document.addEventListener('visibilitychange', () => {
  if (document.visibilityState === 'visible' && Date.now() - _lastLoad > 600_000) {
    const url = location.href.split('?')[0];
    location.replace(url + '?t=' + Date.now());
  }
});
