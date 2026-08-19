# Portfolio Site Kit（個人作品集網站建構方法論）

一套經過真實項目驗證嘅 Skill：用嚟起同時面向國際同埋中國內地用戶嘅三語（英文 / 简体中文 / 繁體中文）作品集同埋展示類靜態網站。

本 kit 提煉自起 [icarusye.site](https://icarusye.site/) 嘅實戰經驗——一個已經上咗線嘅作品集：純手寫 HTML/CSS/JS + Cloudflare Pages，零框架、零建構，大量用足音頻、視頻、在線嵌入文檔同長圖文，全部內容喺防火牆兩邊都正常訪問到。呢個網站係呢套方法論嘅活例子，亦都可以喺睇文檔嗰陣做參考。

**呢個唔係一套「照抄就掂」嘅模板，而係一套方法論**：接洽問卷、設計規範、組件規格、雙地域媒體策略、部署紀律、三層文檔體系，同埋一份收錄咗 23 條真實瀨嘢記錄嘅避坑清單，每一條都按「現象 → 根因 → 點樣避免」嘅格式寫低。

[English version](README.md) · [简体中文版](README.zh-CN.md)

---

## 佢解決咗啲咩問題

| 問題 | 本 kit 嘅答案 |
|---|---|
| 無從入手——風格唔明、內容唔齊 | 先走接洽問卷：風格參考（代碼 / 截圖 / HTML / Figma）、履歷同埋作品清單、連結核對；風格 Demo 先行，內容檔案後補 |
| 境外 CDN、字體、雲端連結喺內地開唔到 | 全面自托管紀律 + 雙連結策略（海外直連 + 內地鏡像） |
| 影片喺海外播到、內地播唔到 | 海外用 `<video>` 串流直連（`raw=1`），內地用可內嵌平台 iframe（`?embed`），按語言成塊切換 |
| 外連文章內地開唔到 | 本地 HTML 存檔模式：CMS 頁面 CSS / 字體 / 圖片全部落本地；JS 驅動嘅捲動敘事頁只落素材 |
| 中文字體成日數兆載荷 | 先按「站內實際字符集」子集化，再按 unicode-range 分片 |
| 部署之後 CSS/JS 唔更新 | 緩存版本紀律：每次改內容一定要 bump `?v=YYYYMMDD` |
| 多語言站慢慢變咗幾套分叉代碼 | 單 DOM 三語引擎：內嵌字典 + 屬性級 i18n 全集 + `?lang=` URL + 瀏覽器偵測 |
| 迭代亂晒、改下改下就散咗 | 三層文檔體系：改版總規劃 → 輪次決策日誌 → 站根活檔 |
| 作品加減之後計數四圍對唔上 | 內容運維清單：同步點逐項列晒，計數由 DOM 自動計 |

## 推薦工具鏈

- **建構用 [TRAE](https://www.trae.cn/)**：本地即時預覽手機 / 平板 / 桌面多設備視口，做多模態響應式適配直接又高效；主流模型任揀。當然唔限制其他工具——呢套方法論同工具無關。
- **設計原型用 [Kimi K3](https://www.kimi.ai/blog/kimi-k3)**：喺而家用得嚟做網頁設計嘅模型入面，佢嘅審美算係夠好；將參考截圖餵畀佢，會出返一套屬於你自己嘅風格 Demo。Demo 定稿之後先入工程。
- 分工口訣：**Kimi 出審美，TRAE 出工程。**

## 推薦服務

| 用途 | 服務 | 說明 |
|---|---|---|
| 靜態托管 | [Cloudflare Pages](https://pages.cloudflare.com/) | 直傳零建構；單檔 25 MiB 上限 |
| 對象存儲（內地向） | [騰訊雲 COS](https://cloud.tencent.com/product/cos) · [阿里雲 OSS](https://cn.aliyun.com/product/oss) | 大媒體外置，內地直連穩定 |
| 對象存儲（海外向） | [Cloudflare R2](https://www.cloudflare.com/products/r2/) | 零出流量費；同 Pages 同帳戶 |
| 兩地可達性檢測 | [ITDOG HTTP 檢測](https://www.itdog.cn/http/) | 全國多省 + 海外節點並發測線上 URL；每次部署後跑一遍 |
| 電子名片（海外） | [Popl](https://popl.co/) | 可內嵌名片 iframe |
| 電子名片（內地） | [muse link](https://muselink.cc/) | 內地可達嘅名片 iframe |
| 作品清單載體 | [飛書](https://www.feishu.cn/) | 多維表格：一行一件作品、連結分欄 |
| Logo 生成器（網頁、風格探索用） | [明日方舟：終末地風格](https://ark.ncreeper.top/) · [圖敘 TuxuAI](https://www.tuxuai.com/share/inspiration?shareId=880) | 只係分享、唔作保證——商用前自己確認版權 |
| MCP（可選） | [github-mcp-server](https://github.com/github/github-mcp-server) · [mcp-server-cloudflare](https://github.com/cloudflare/mcp-server-cloudflare) · [AnySearch](https://www.anysearch.com/home) | 畀 agent 直接操作 GitHub / Cloudflare，或者喺對話入面搜全網 |
| 多模態（可選） | [Qwen-MM-Plugins](https://github.com/QwenLM/Qwen-MM-Plugins) | 令冇視覺能力嘅 agent 都理解到視頻 / 音頻 / 圖片；要自己接千問 API key |

## 儲存庫結構

```
├── SKILL.md                  Skill 主入口：觸發條件、核心原則、工作流、檔案地圖
├── CHANGELOG.md             本 skill 自己嘅版本日誌
├── references/
│   ├── 00-onboarding.md         接洽問卷、內容載體、工具鏈與隱私紅線
│   ├── 01-design-and-style.md   設計 token + 「搵風格」方法論 + 文案紀律
│   ├── 02-components.md         組件規格：頂欄、卡片、篩選、播放器、詳情頁、預載器、Contact、內嵌名片、Colophon
│   ├── 03-media-compat.md       跨地域媒體兼容（視頻 / 音頻 / 網頁存檔 / 區域差異四層清單）
│   ├── 04-deploy-and-domain.md  托管、緩存紀律、自訂域名綁定實操（雙路線+排障）、域名購買指南、SEO 基礎、隱私友好統計與合規、內地可達
│   ├── 05-structure-i18n.md     資料夾結構 + 三語引擎 + 首頁架構
│   ├── 06-iteration.md          三層迭代文檔體系（總規劃 / 輪次日誌 / 站根活檔）
│   ├── 07-pitfalls.md           23 條瀨嘢記錄，逐條按「現象 → 根因 → 點樣避免」
│   ├── 08-accessibility-motion.md WCAG 2.2 基線與測試工具 + 無障礙模式 + reduced-motion 策略 + 光敏保護
│   ├── 09-performance.md        性能：字體子集分片管線、懶加載、IO 模式、Resource Hints 與圖片格式
│   ├── 10-content-ops.md        內容運維：作品加減同步清單、計數自動化、週期性內容審計
│   └── 11-preship-checklist.md  上線前總檢單（硬約束 + 全部 checklist 一頁匯總）
├── templates/                   可以直接複製嘅組件骨架
│   ├── trilingual.html          三語引擎（完整屬性集：文本/alt/title/href/解碼/游標）
│   ├── works-index.html         全部作品索引頁骨架（計數自動化 + 篩選 + HIGHLIGHT）
│   ├── case-page.html           案例詳情頁骨架（互連列表 + 雙連結 Links 區）
│   ├── 404.html                 通用失敗頁（4XX 語義化 + 三語 + 語言回連）
│   ├── audio-player.html        內嵌音頻播放器（播放 / seek / 時間 / 下載，單實例）
│   ├── bgm.html                 背景音樂單例按鈕
│   ├── tile-field.html          參數化 Metro 磁貼背景場
│   ├── marquee.html             無限走馬燈（複製×2 + 回捲 + 拖動 + 聯動暫停）
│   └── regional-links.html      雙連結模式（raw=1 / ?embed / data-href-* / 點擊加載）
├── tools/                       建構與審計腳本（用法見 tools/README.md）
│   ├── collect_chars.py         收集站內 CJK 用字 → 字符集清單
│   ├── subset_fonts.py          按字符集子集化原字體（產中間 OTF）
│   ├── split_cjk.js             cn-font-split 分片 → unicode-range woff2 + cjk.css
│   ├── audit.sh                 一致性審計六項（計數 / ?v= / 徽標 / sitemap / 體量）
│   └── README.md                管線用法、依賴、三瀨嘢備忘、圖片處理速查
└── examples/
    └── minimal.html             活體測試頁：四組件最細組裝（雙擊即跑）
```

## 核心原則

1. **靜態優先。** 純 HTML/CSS/JS 直傳，無建構指令。
2. **雙地域可達。** 字體、音頻、關鍵圖片自托管；每一條境外服務連結都配內地替代。
3. **單檔上限意識。** 大媒體放對象存儲（靜態托管成日有 25 MiB 單檔限制），頁面層保持輕量。
4. **緩存版本紀律。** 每次改 CSS/JS 內容一定要 bump `?v=`，否則瀏覽器永遠用不可變舊副本。
5. **內容優先版式。** 案例頁裡面 iframe、視頻、連結排喺長文本之前。
6. **單一強調色。** 唯一嘅高飽和色只做行動訊號（連結、焦點、進度），絕唔做裝飾，任何視圖佔比 ≤5%。
7. **動效克制。** 過渡 ≤250ms、ease-out；語言切換正文即時替換；全站尊重 `prefers-reduced-motion`。
8. **觸屏與鼠標分治。** hover 特效只喺 `(hover:hover) and (pointer:fine)` 下生效；觸屏默認睇到完整狀態。
9. **一個 DOM，三種語言。** 每頁內嵌字典就地切換；`?lang=` URL 支援直連；首訪瀏覽器偵測但唔固化。
10. **書面迭代。** 每輪將決策鎖入日誌（用戶原話 → 根因 → 方案 → 狀態）先至郁代碼，然後一次執行完。

## 使用方式

### 安裝（TRAE 或任何支援 skill 嘅 agent）

```bash
git clone https://github.com/IcarusYe12138/Portfolio-site-by-IcarusYe.git \
  ~/.trae-cn/skills/portfolio-site-kit
# 或者用 vercel-labs 嘅 skills CLI：
npx skills add https://github.com/IcarusYe12138/Portfolio-site-by-IcarusYe
```

（或者直接將倉庫資料夾複製入你嘅 skills 目錄。）之後當你要求建立、重構或迭代作品集、作品展示站、富媒體靜態站時，agent 會自動調用。`tools/` 同埋 `examples/` 隨倉庫派發——字體管線與一致性審計用法見 `tools/README.md`。

### 伴侶 skill（接洽時會問你裝唔裝）

本 skill 管作品集嘅**垂直生命週期**（結構 / 雙地域媒體 / 三語 / 內容運維 / 部署）；橫向嘅審美與合規由伴侶 skill 補位，接洽時按分層表問：

| 層 | Skill | 補咩位 |
|---|---|---|
| ★ 必裝 | [frontend-design](https://github.com/anthropics/claude-code/tree/main/plugins/frontend-design)（Anthropic 官方） | 寫碼前鎖定美學方向、反 AI slop |
| ★ 必裝 | [web-design-guidelines](https://github.com/vercel-labs/agent-skills)（Vercel） | 100+ 條 WCAG 2.2 / UX 自動審計 |
| 推薦 | [ui-ux-pro-max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | 240+ 風格庫 / 127 字體配對——冇參考素材時嘅發散器 |
| 推薦 | [impeccable](https://impeccable.style/) | brand 模式精修指令（typeset / colorize / bolder / quieter） |

紀律：先問再推（用戶可能已經有同類）；skill 總量控制在 20–30 個內；伴侶 skill 若推 React 組件庫，以本 skill 嘅「靜態優先」原則為準。

**安裝紀律（硬規則，適用於一切 MCP 與 skill）：冇用戶明確許可，千祈唔好擅自安裝任何嘢。** agent 只負責推薦——畀出指令、理由同影響，由用戶自己執行，或者明確授權先至代為執行。上表所有可選工具都係「唔裝都冇事」：冇任何流程環節依賴佢。

### 當做純參考文檔

`references/` 目錄本身就係一本獨立手冊。建議入口：

- 項目啟動前 → 先讀 `references/00-onboarding.md`（接洽問卷與隱私紅線）；
- 關心跨地域媒體 → 由 `references/03-media-compat.md` 讀起；
- 每次大改前後 → 將 `references/07-pitfalls.md` 當 checklist 過一遍；
- 上線之前 → 用 `references/09-performance.md` 過字體管線與懶加載矩陣；
- 作品加減時 → 照 `references/10-content-ops.md` 嘅同步清單執行；
- 每次發布前 → `references/11-preship-checklist.md` 一頁總檢單收尾；
- 需要組件骨架 → 直接抄 `templates/`，全部零依賴、自帶註釋；
- `examples/minimal.html` → 雙擊瀏覽器開，睇四組件嘅最細拼裝。

## 新站建議工作流

1. **接洽問答**（`references/00-onboarding.md`）：風格參考（代碼 / 截圖 / HTML / Figma）、履歷與作品清單、海外+內地連結核對。檔唔齊？先做風格 Demo、內容後補；作品清單入結構化載體（飛書 / Markdown / 表格）。
2. **定風格**：將參考截圖交畀支援圖片嘅 agent（推薦 Kimi K3），出返屬於作者自己嘅風格 Demo（配色、字體、母題、版式），鎖定做書面設計規範。絕唔照抄現有網站。
3. **定結構**：頁面清單、首頁架構、assets 佈局、語言機制——結構越遲改越貴。
4. **鋪組件**：由 `templates/` 複製骨架（詳情頁用 `case-page.html`），套入設計規範嘅 token。
5. **接媒體**：視頻雙連結、音頻自托管、文章本地存檔，一次配齊。
6. **上線**：直傳托管、`_headers`、robots、sitemap、og:image、JSON-LD 結構化數據、域名選購；部署後用 ITDOG（https://www.itdog.cn/http/ ）多地抽測海外+內地可達性，再真機過一遍。
7. **書面迭代**（總規劃 → 輪次日誌 → 站根活檔），每輪結束過一遍避坑清單。
8. **內容增長**：作品加減一律行內容運維清單，計數唔飄移。

## 本 kit 有意唔做嘅事

- 唔捆綁任何框架、建構器或運行時：冇會過期嘅嘢。
- 唔預設審美，只講紀律：視覺身份來自作者本人，而唔係呢個 kit。
- 唔含任何具體品牌連結：文檔入面嘅 URL 全部係通用佔位符（`overseas.example`、`mainland.example`）。

## 許可

[MIT](LICENSE) · Copyright (c) 2026 IcarusYe12138

方法論與代碼骨架可以自由重用；佢提煉來源嘅作品集仍歸作者本人所有。