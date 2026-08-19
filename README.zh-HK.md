# Portfolio Site Kit（個人作品集網站建構方法論）

一套精簡、慳 token 嘅方法論，幫（就算零代碼基礎嘅）你起一個**三語**（英文 / 简体中文 / 繁體中文）個人作品集 / 作品展示**靜態站**，照顧埋國際同內地雙平台可達。純手寫 HTML/CSS/JS，零框架、零建構。

[English version](README.md) · [简体中文版](README.zh-CN.md)

---

## 呢個係一套方法論，唔係一個模板

你唔使先睇完任何作品集、亦都唔使讀晒呢份 README 先郁到手——**由「快速開始」就起得步**。讀得越深，越少行冤枉路：

1. **咩資料都未睇？** → 直接睇 [快速開始](#快速開始)，5 步入門。
2. **有舊站想改 / 已有內容？** → 睇 [skill 點樣讀你嘅網站](#skill-點樣讀你嘅網站)，佢按需分批讀，唔會一次過吞晒你全部檔案。
3. **想一次搞掂判斷標準？** → 睇 [核心原則](#核心原則) 同 [參考文檔地圖](#參考文檔地圖)。
4. **慣咗自己睇？** → 用 [目錄](#目錄) 慢慢行。

呢套方法論提煉自一個真實項目（[icarusye.site](https://icarusye.site/)），但**你唔使參考佢**都用得——佢只係一份來源，唔係門檻。

### 快速開始

最直接嘅路徑，0 前置文檔，照講就得：

1. **將要用嘅嘢畀我**：貼 1–3 張你鍾意嘅網站/海報截圖，或者一句話形容想要嘅感覺；冇就跳過，遲啲補。
2. **列低你嘅作品**：每件作品一個條目（標題 + 類型 + 年份 + 一條連結，海外/內地各一條更好）。
3. **講一個目標**：例如「先做個睇得嘅單頁版」「要中英雙語」「作品喺內地要開到」。
4. 我會跟住 [references/00-onboarding.md](references/00-onboarding.md) 嘅接洽清單逐項問你——**我會追問你未畀嘅嘢，唔會替你自己估**。
5. 你鎖定風格方向之後，我先郁代碼，一輪只做一件事。

> 慳 token 嘅接洽原則：**先問清、再郁手；資訊缺失就問，唔擅自代答。** 一次只問你一份問題，答完先入下一步——唔會一次過倒晒成本書畀你。

---

## 目錄

- [佢解決咗啲咩問題](#佢解決咗啲咩問題)
- [啱唔啱你](#啱唔啱你)
- [核心原則](#核心原則)
- [skill 點樣讀你嘅網站](#skill-點樣讀你嘅網站)（按需分批，慳 token）
- [參考文檔地圖](#參考文檔地圖)（幾時翻邊篇）
- [儲存庫結構](#儲存庫結構)
- [安裝](#安裝)
- [推薦工具鏈](#推薦工具鏈)
- [推薦服務](#推薦服務)
- [設計階段資源](#設計階段資源)（圖標 / 原型 / 圖表 / 前端 skill）
- [伴侶 skill](#伴侶-skill)（接洽時問你裝唔裝）
- [本 kit 有意唔做嘅事](#本-kit-有意唔做嘅事)
- [許可](#許可) · [連結時效](#連結時效)

---

## 佢解決咗啲咩問題

| 問題 | 本 kit 嘅答案 |
|---|---|
| 無從入手——風格唔明、內容唔齊 | 先走接洽問卷定風格方向；風格 Demo 先行，內容檔案後補 |
| 境外 CDN、字體、雲端連結喺內地開唔到 | 全面自托管紀律 + 雙連結策略（海外直連 + 內地鏡像） |
| 影片喺海外播到、內地播唔到 | 海外用 `<video>` 串流直連（`raw=1`），內地用可內嵌平台 iframe（`?embed`），按語言成塊切換 |
| 外連文章內地開唔到 | 本地 HTML 存檔：CMS 頁嘅 CSS / 字體 / 圖片全部落本地 |
| 中文字體成日數兆載荷 | 先按站內實際字符集子集化，再按 unicode-range 分片 |
| 部署之後 CSS/JS 唔更新 | 緩存版本紀律：每次改內容 bump `?v=YYYYMMDD` |
| 多語言站慢慢變咗幾套分叉代碼 | 單 DOM 三語引擎：內嵌字典 + 屬性級 i18n + `?lang=` URL + 瀏覽器偵測 |
| 迭代亂晒、改下改下就散咗 | 三層文檔：改版總規劃 → 輪次決策日誌 → 站根活檔 |
| 作品加減之後計數四圍對唔上 | 內容運維清單 + 由 DOM 自動計數 |

## 啱唔啱你

**啱**：個人作品集 / 作品展示 / 履歷型靜態站；含音視頻、圖文集、iframe 嵌入；要國際 + 內地雙平台可達；公開、無登入態、無後端。

**唔啱 / 可以跳過**：重後端業務系統（唔行純靜態）；單語純內地、冇大媒體（可以跳過雙連結章節，其餘照用）。

## 核心原則

1. **靜態優先。** 純 HTML/CSS/JS 直傳，無建構指令。
2. **雙地域可達。** 字體、音頻、關鍵圖片自托管；每條境外連結配內地替代。
3. **單檔上限意識。** 大媒體放對象存儲，頁面層保持輕量。
4. **緩存版本紀律。** 每次改 CSS/JS 必 bump `?v=`，否則瀏覽器用舊資源。
5. **內容優先版式。** 案例頁 iframe/視頻/連結排喺長文本前。
6. **單一強調色。** 一個高飽和色只做行動訊號，佔比 ≤5%。
7. **動效克制。** 過渡 ≤250ms、ease-out；全站尊重 `prefers-reduced-motion`。
8. **觸屏與鼠標分治。** hover 特效門控喺 `(hover:hover) and (pointer:fine)`。
9. **一個 DOM、三種語言。** 內嵌字典就地切換；`?lang=` URL 直連；首訪瀏覽器偵測唔固化。
10. **書面迭代。** 每輪將決策鎖入日誌先郁代碼，一輪一次執行完。

## skill 點樣讀你嘅網站

**核心：按需分批、逐層推進，絕唔會一次過讀晒你全部檔案。** 慳 token，又避免噪音蓋過真正重要嘅嘢。

讀取順序（每步用結論判斷係咪繼續，需要先讀下一步）：

1. **入口層**：先睇索引/主頁（`index.html`、`works`、目錄結構、`_headers` / `robots.txt` / `sitemap.xml`）——用最細樣本判斷「咩站、咩語言、大致結構」。
2. **樣式層**：睇 CSS 變量 / 設計 token（配色、字體、間距）——判斷風格同係咪成體系。
3. **腳本層**：睇交互腳本（語言切換、篩選、播放器）——判斷三語機制同組件重用。
4. **媒體層**：遇到視頻/音頻/外連先至讀對應媒體文檔與連結——確認跨地域可達性。
5. **淨係深讀你需要嘅參考文檔**，唔掂無關章節。

揀檔案參考 [參考文檔地圖](#參考文檔地圖)：邊類任務就開邊篇，唔成包加載。

## 參考文檔地圖

`references/` 係按主題拆開嘅深度文檔。**對應你嘅任務揀一篇開**，唔好一次睇晒，慳 token 又易明：

| 你嘅處境 | 開邊篇 |
|---|---|
| 新站一定要第一步 | [00-onboarding](references/00-onboarding.md) — 接洽問卷、素材載體、工具鏈、隱私紅線 |
| 要定風格方向 | [01-design-and-style](references/01-design-and-style.md) — 搵風格三步法 + Style Spec + 文案紀律 |
| 要起組件骨架 | [02-components](references/02-components.md) — 各組件幾時用/要點/反面 |
| 作品要跨地域睇到 | [03-media-compat](references/03-media-compat.md) — 視頻/音頻/圖文雙連結 |
| 要部署/買域名/緩存 | [04-deploy-and-domain](references/04-deploy-and-domain.md) — 托管、緩存、域名、SEO、合規 |
| 要理清資料夾同三語機制 | [05-structure-i18n](references/05-structure-i18n.md) — 目錄結構 + 三語引擎 |
| 要迭代打磨節奏 | [06-iteration](references/06-iteration.md) — 三層文檔體系 + 輪次節奏 |
| 每次大改前後自查 | [07-pitfalls](references/07-pitfalls.md) — 23 條真實瀨嘢 |
| 要做無障礙/動效安全 | [08-accessibility-motion](references/08-accessibility-motion.md) — WCAG 2.2、reduced-motion、光敏 |
| 要優化性能/字體 | [09-performance](references/09-performance.md) — 字體管線、懶加載、Resource Hints |
| 要加減作品 | [10-content-ops](references/10-content-ops.md) — 加減同步清單 + 計數自動化 |
| 上線前總檢 | [11-preship-checklist](references/11-preship-checklist.md) — 一頁總檢單 |
| 想直接抄組件 / 睇效果 | `templates/`（零依賴骨架）· `examples/minimal.html`（四組件雙擊即跑） |

## 儲存庫結構

```
portfolio-site-kit/
├── SKILL.md                入口：觸發、核心原則、分批工作流、檔案地圖
├── CHANGELOG.md            skill 自己嘅版本日誌
├── references/             分主題深度文檔（按任務揀開，見上表）
├── templates/              可以直接複製嘅組件骨架（0 依賴、自帶註釋）
│   ├── trilingual.html     三語引擎（文本/alt/title/href/解碼/游標）
│   ├── works-index.html    作品索引頁（計數自動化 + 篩選 + HIGHLIGHT）
│   ├── case-page.html      案例詳情頁（互連 + 雙連結 Links）
│   ├── 404.html            通用失敗頁
│   ├── audio-player.html   內嵌音頻播放器
│   ├── bgm.html            背景音樂單例按鈕
│   ├── tile-field.html     參數化 Metro 磁貼背景場
│   ├── marquee.html        無限走馬燈
│   └── regional-links.html 雙連結 / 視頻 / iframe
├── tools/                  建構與審計腳本（見 tools/README.md）
└── examples/
    └── minimal.html        四組件最細組裝（雙擊即跑）
```

## 安裝

一次裝好（TRAE 或任何支援 skill 嘅 agent）：

```bash
git clone https://github.com/IcarusYe12138/Portfolio-site-by-IcarusYe.git \
  ~/.trae-cn/skills/portfolio-site-kit
# 或者用 vercel-labs 嘅 skills CLI：
npx skills add https://github.com/IcarusYe12138/Portfolio-site-by-IcarusYe
```

（或者直接將倉庫資料夾複製入你嘅 skills 目錄。）之後你講「起作品集 / 改版 / 加語言 / 解決內地開唔到」，agent 會自動調用。`tools/` 同 `examples/` 隨倉庫派發。

## 推薦工具鏈

- **建構用 [TRAE](https://www.trae.cn/)**：本地即時預覽手機/平板/桌面視口，多設備響應式直觀；主流模型任揀。方法論與工具無關，其他都得。
- **設計原型用 [Kimi K3](https://www.kimi.ai/blog/kimi-k3)**：審美好；將參考截圖餵畀佢可以攞返你自己嘅風格 Demo。
- 分工口訣：**Kimi 出審美，TRAE 出工程。**

（具名推薦係「作者驗證過嘅優先項」，工具係會過期嘅時點選擇——失效就按同類能力替換，見 [連結時效](#連結時效)。）

## 推薦服務

| 用途 | 服務 | 說明 |
|---|---|---|
| 靜態托管 | [Cloudflare Pages](https://pages.cloudflare.com/) | 直傳零建構，單檔 25 MiB 上限 |
| 對象存儲（內地） | [騰訊雲 COS](https://cloud.tencent.com/product/cos) · [阿里雲 OSS](https://cn.aliyun.com/product/oss) | 大媒體外置，內地直連穩 |
| 對象存儲（海外） | [Cloudflare R2](https://www.cloudflare.com/products/r2/) | 零出流量，同 CF 帳戶 |
| 可達性檢測 | [ITDOG HTTP](https://www.itdog.cn/http/) | 全國多省 + 海外節點測線上 URL |
| 電子名片（海外/內地） | [Popl](https://popl.co/) / [muse link](https://muselink.cc/) | 可內嵌名片 iframe |
| 作品清單載體 | [飛書](https://www.feishu.cn/) | 多維表格：一行一件、連結分欄 |
| Logo 生成器（網頁，風格探索） | [明日方舟：終末地](https://ark.ncreeper.top/) · [圖敘](https://www.tuxuai.com/share/inspiration?shareId=880) | 只係分享，商用前確認版權 |
| MCP（可選） | [github-mcp-server](https://github.com/github/github-mcp-server) · [mcp-server-cloudflare](https://github.com/cloudflare/mcp-server-cloudflare) · [AnySearch](https://www.anysearch.com/home) | 畀 agent 直接操作 GitHub/CF，或對話內搜全網 |
| 多模態（可選） | [Qwen-MM-Plugins](https://github.com/QwenLM/Qwen-MM-Plugins) | 令冇視覺 agent 理解音視頻/圖片，要自己嘅 Qwen API key |

## 設計階段資源

設計階段成日問嘅問題：圖標用邊個、原型點做、要唔要裝某啲前端 skill。以下係速查（評級係作者主觀評估，唔強制）：

### 圖標庫
| 庫 | 風格 | Agent 調用 | 覆蓋 | 許可/注意 |
|---|---|---|---|---|
| [simple-icons](https://github.com/simple-icons/simple-icons) ★ 首選 | 單色極簡剪影，3300+ 品牌 | CDN 按 slug 直連 | QQ/微博/B 站/小紅書 + 幾乎全海外 | **CC0 免署名**，行業標準 |
| [NViconsLib Silhouette](https://github.com/nullice/NViconsLib_Silhouette) | 純剪影，專為內地+全球社媒 | GitHub Raw 直連 | 微信/QQ 空間/微博 + 海外 | 上游缺內地平台嘅補充 |
| [thesvg](https://github.com/glincker/thesvg) | 極簡品牌 SVG，6000+ | `@thesvg/mcp-server` 對話式 | 含微博，持續更新 | 按名叫人個工具，唔用手寫 URL |
| [icons8-mcp](https://github.com/icons8/icons8-mcp) | 116 風格、36 萬+ | 官方 MCP，自然語言搜 | 按名可命中，需人工核實 | 免費只出 PNG，SVG 要 Key |

### 設計與原型工具
| 工具 | 作用 |
|---|---|
| [Google Stitch](https://stitch.withgoogle.com/) | Gemini AI UI 生成：文字/草圖/截圖 → 多屏原型 + 代碼；可提取現有網站設計系統 |
| [Design Skills Hub](https://designskills.xyz/skills) ·（官網 [vaporaviator.com/works/design-skills-hub](https://vaporaviator.com/works/design-skills-hub)） | 社區設計技能註冊中心：審美 + 工程兩種 skill；可將 Figma 導出成重用 skill |

兩者互補：Stitch **生成** UI，Design Skills Hub **編碼設計判斷**。

### 圖表 / 數據可視化
| Skill | 作用 |
|---|---|
| [lieflat-charts](https://github.com/larashero3-dotcom/lieflat-charts) ★ | 面向 agent 嘅數據可視化：數據 → 精緻可交互 HTML 圖表（指標/時間線/分佈），唔使重型圖表庫 |

### 前端設計 skill（作者評估）
| Skill | 結論 |
|---|---|
| **Design Tokens**（OKLCH）— [XINGANLIU/design-system-generator-skill](https://github.com/XINGANLIU/design-system-generator-skill) ★ | 改一個 `hue` 全站換色，契合靜態優先 + 單一強調色 |
| **identity-skill**（Sac-Y）— [Sac-Y/identity-skill](https://github.com/Sac-Y/identity-skill) | 可選：先出參考圖確認再 1:1 還原，依賴生圖模型 |
| **Motion Skill**（Framer Motion）— [schoepplake/framer-motion-skill](https://github.com/schoepplake/framer-motion-skill) | **本棧唔建議**：面向 React，同靜態優先衝突 |

一句講晒：在意色彩科學裝 **Design Tokens**；做 React 先考慮 **Motion Skill**（超本 kit 範圍）；其餘按需。

## 伴侶 skill

本 kit 管作品集嘅**垂直生命週期**（結構 / 雙地域媒體 / 三語 / 運維 / 部署）；橫向嘅審美同合規由伴侶 skill 補位。**接洽時會問你裝唔裝**——絕對唔擅自裝：

| 層 | Skill | 補咩位 |
|---|---|---|
| ★ 必裝 | [frontend-design](https://github.com/anthropics/claude-code/tree/main/plugins/frontend-design)（Anthropic 官方） | 寫碼前鎖定美學方向，反 AI slop |
| ★ 必裝 | [web-design-guidelines](https://github.com/vercel-labs/agent-skills)（Vercel） | 100+ 條 WCAG 2.2 / UX 自動審計 |
| 推薦 | [ui-ux-pro-max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | 240+ 風格 / 127 字體配對——冇參考時發散 |
| 推薦 | [impeccable](https://impeccable.style/) | brand 模式精修指令 |

紀律：先問再推（用戶可能已經有同類）；skill 總量 ≤20–30；伴侶 skill 若推 React 組件庫，以本 kit「靜態優先」為準。

**安裝紀律（硬規則，適用一切 MCP 與 skill）：冇明確許可，千祈唔好擅自安裝任何嘢。** agent 只推薦、畀指令同理由，由你執行或明確授權後代理。上面所有可選工具都係「唔裝都冇事」。

## 本 kit 有意唔做嘅事

- 唔捆綁框架、建構器或運行時——冇會過期嘅嘢。
- 唔預設審美、只講紀律——視覺身份來自你，唔係本 kit。
- 唔含具體品牌連結——文檔 URL 都係通用佔位符。

## 許可

[MIT](LICENSE) · Copyright (c) 2026 IcarusYe12138

方法論與代碼骨架可以自由重用；佢提煉來源嘅作品集仍歸作者本人所有。

## 連結時效

文檔入面嘅外部連結（產品頁、GitHub 倉庫、社區 skill）喺撰寫時（2026-08）已驗證可達，但可能郁動或下架。若連結失效或工具停咗，請按**同類能力**而唔係**具體品牌**替換——方法論一樣成立。發現失效連結歡迎提 PR 或 issue。