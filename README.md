# efinmap v3 — 桌面股票热力图 | Desktop Stock Heatmap

实时追踪 **美股 / 港股 / 日韩台** 市场涨跌的桌面应用，无需浏览器，开箱即用。

Real-time stock heatmap desktop app covering **US / HK / JP-KR-TW** markets. No browser needed, run straight from the EXE.

---

## 功能特点 | Features

### 📊 热力图 | Heatmap
- 美股 US (119只) | 港股 HK (108只) | 日韩台 Asia (71只) | 自选 Watchlist
- 涨跌幅颜色方块，一目了然
- Color-coded tiles showing real-time performance

### 🔄 自动刷新 | Auto Refresh
- 定时拉取 Yahoo Finance 最新数据（默认每30分钟）
- 倒计时显示下次刷新时间
- 刷新后页面自动重载
- Automatic fetch on configurable interval (default 30 min)
- Countdown timer + auto-reload on update

### 🎨 涨跌颜色切换 | Color Scheme
- **绿涨红跌**（西方习惯 / Western default）
- **红涨绿跌**（A股/港股习惯 / Chinese/HK style）
- 设置中一键切换，保存后自动刷新
- Switch instantly in Settings — no restart needed

### 🌐 中英双语 | Bilingual UI
- 界面语言可在 English / 中文 之间切换
- 热力图股票名称自动对应语言
- Switch between English and Chinese in Settings

### 🛠 股票管理 | Stock Manager
- **添加**：输入代码自动查询，指定板块和基准价
- **调整**：修改已有股票的市场、板块、价格
- **屏蔽**：隐藏不需要的股票（非永久删除）
- **Add**: auto-lookup by ticker, assign sector and base price
- **Edit**: modify market, sector, or reference price
- **Block**: hide stocks without deleting them

### 🖥 系统集成 | System Integration
- **系统托盘**：关闭窗口自动最小化到托盘，后台持续运行
- **开机自启**：一键设置 Windows 登录后自动启动
- **Yahoo Finance 链接**：点击股票代码在浏览器打开详情页
- **System tray**: minimize on close, runs in background
- **Auto-start**: boot with Windows
- **Yahoo Finance links**: click any ticker to open in browser

---

## 截图 | Screenshots

*(Insert screenshots here)*

---

## 快速开始 | Quick Start

1. 下载 `efinmap.exe` 到任意目录（路径不要含中文字符）
2. 双击运行 — 首次启动会自动拉取数据
3. 右下角托盘图标常驻，右键可管理程序

1. Download `efinmap.exe` to any folder (avoid Chinese characters in path)
2. Double-click to launch — first run fetches data automatically
3. System tray icon stays resident; right-click for menu

> **注意**：首次启动因加载 WebEngine 可能需要几秒钟，请耐心等待。
> **Note**: First launch may take a few seconds due to WebEngine initialization.

---

## 设置说明 | Settings

点击工具栏 ⚙ 齿轮图标打开设置对话框。

Click the ⚙ icon on the toolbar to open Settings.

| 设置项 | 说明 | 默认值 |
|--------|------|--------|
| 刷新间隔 | 数据自动更新频率（1–120分钟） | 30 |
| 语言 | English / 中文 | 中文 |
| 涨跌颜色 | 绿涨红跌 / 红涨绿跌 | 绿涨红跌 |
| 开机自启 | Windows 登录时自动运行 | 关 |

---

## 数据来源 | Data Source

- **Yahoo Finance** — 实时股价、涨跌幅、市值
- 数据延迟约 15–20 分钟（Yahoo Finance 免费数据限制）
- Data is delayed ~15–20 minutes per Yahoo Finance free tier

---

## 常见问题 | FAQ

**Q: 部分股票显示 `--`？**
A: Yahoo Finance 偶尔限流，等几分钟后点击工具栏刷新按钮重试。

**Q: Some stocks show `--`?**
A: Yahoo Finance rate limit. Wait a few minutes and click the refresh button.

**Q: 如何退出程序？**
A: 右键托盘图标 → 退出；或在任务管理器结束进程。

**Q: How to quit?**
A: Right-click tray icon → Exit, or close via Task Manager.

**Q: 添加的股票没有涨跌幅？**
A: 需要在「管理股票」→「调整股票」中填入正确的年末基准价格。

**Q: Added stock shows no change %?**
A: Go to Stock Manager → Edit tab and set the correct year-end reference price.

---

## 版本信息 | Version

**v3.0** (2026-05-28)
- 首次桌面版发布
- 涨跌颜色切换 + 中英双语 + 股票管理 + 系统托盘
- Initial desktop release
- Color scheme toggle, bilingual UI, stock manager, system tray
