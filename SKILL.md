---
name: portfolio-site-kit
description: Builds trilingual portfolio / works-showcase static sites with dual-region (global + mainland China) media compatibility, self-hosted fonts, and iterative polish. Invoke when creating, restructuring, or iterating a personal portfolio, works showcase, or media-rich static site.
---

# portfolio-site-kit · 个人作品集网站构建方法论

本 skill 从一个已上线的三语（EN / 简中 / 繁中）个人作品集网站提炼而来：纯手写 HTML/CSS/JS + Cloudflare Pages，零框架零构建，含大量音视频与图文作品，同时保障国际与中国内地双平台可达。

**它不是一套固定模板，而是一套方法论**：设计规范、组件规范、跨地域媒体策略、部署策略、迭代节奏与避坑清单。把「具体实现」抽象成「可迁移的原则 + 可复用的代码片段」。

---

## 何时使用

- 用户要建个人作品集 / 作品展示站 / 简历型静态站（含音视频、图文集、iframe 嵌入）
- 用户已有作品集，要改版、加语言、解决「内地打不开」「媒体播不了」等问题
- 用户要做「国际 + 内地」双平台可达的任何展示类静态站
- 用户在为展示站选部署方案（托管、域名、字体、媒体存储）

## 何时不适用

- 重后端业务系统、需要登录态的应用 → 不走纯静态路线
- 单语、纯国内受众、无大媒体 → 可跳过双链路章节，其余仍适用

---

## 核心原则（速览）

1. **静态优先**：纯 HTML/CSS/JS 直传托管平台，零构建命令。能不用框架就不用。
2. **双平台可达**：所有资源（字体/音频/关键图片）自托管；境外服务（网盘/在线设计平台/云文档）必须为内地准备替代链路（境内平台镜像或本地存档）。
3. **单文件上限意识**：托管平台单文件大小上限（Cloudflare Pages 为 25 MiB）——大媒体一律放对象存储，页面层只留轻资源。
4. **缓存版本号纪律**：托管平台对 CSS/JS 常发 `immutable + 1y max-age`，**每次改 CSS/JS 内容必须同步 bump `?v=YYYYMMDD` 查询参数**，否则浏览器永久用旧资源，出现「新 HTML + 旧 CSS」混合态。
5. **内容优先的版式**：作品详情页里 iframe / 视频 / 链接先于长文本；版式留呼吸感。
6. **单一强调色**：一个高饱和色只做「行动信号」（链接、焦点、进度、动线），不做装饰；占比 ≤5%。
7. **动效克制**：所有过渡 ≤250ms、ease-out；语言切换等高频操作不做花哨全页动效；全站尊重 `prefers-reduced-motion`。
8. **触屏与鼠标分治**：hover 特效只在 `(hover:hover) and (pointer:fine)` 生效；触屏默认可见完整状态。
9. **多语言单页机制**：每页内嵌字典 + `data-i18n` 就地切换，`?lang=` URL + localStorage 持久化，首访浏览器语言检测但不固化。
10. **书面迭代**：每轮改动先写成「用户原话 → 根因 → 方案 → 状态」的改进文档，锁定后再动代码，一轮一次执行完。

---

## 文件地图

```
portfolio-site-kit/
├── SKILL.md                      ← 本文件
├── references/                   ← 分主题深度文档
│   ├── 01-design-and-style.md    设计规范与「找风格」方法论
│   ├── 02-components.md          组件规范（顶栏/卡片/筛选/播放器/磁贴场/滚动条…）
│   ├── 03-media-compat.md        ★ 音视频与图文的跨地域兼容（专节）
│   ├── 04-deploy-and-domain.md   部署、缓存、域名策略、内地可达
│   ├── 05-structure-i18n.md      文件夹结构 + 三语机制
│   ├── 06-iteration.md           迭代节奏与改进文档写法
│   └── 07-pitfalls.md            ★ 避坑清单（现象→原因→怎么避免）
└── templates/                    ← 可直接复制的组件模板
    ├── trilingual.html           三语切换机制骨架（字典+setLang+data-langs）
    ├── audio-player.html         内嵌音频播放器（播放/seek/时间/下载）
    ├── bgm.html                  背景音乐单例按钮
    ├── tile-field.html           参数化 Metro 磁贴背景场
    ├── marquee.html              无限滚动条（克隆×2+回卷+拖拽+联动暂停）
    └── regional-links.html       区域化链接 / 视频双链路 / iframe 内嵌模式
```

★ = 使用本 skill 时最常被查阅的两篇。

---

## 推荐工作流（新站从 0 到 1）

1. **定性风格**（→ `01-design-and-style.md`）
   - 让作者给几张喜欢的参考截图；
   - 把截图交给任意可用图片 + 联网的 Agent，结合作者专业方向与内容气质，产出一版属于他自己的风格 Demo（配色、字体、母题、版式）；
   - 以该 Demo 为风格锚点，**不要预设任何单一审美，更不要照抄某个现有网站**。
2. **定结构**（→ `05-structure-i18n.md`）：页面清单、assets 拆分、语言机制先定型——后期改结构成本最高。
3. **铺组件**（→ `02-components.md` + `templates/`）：从 templates 复制骨架，套入风格 Demo 的 token。
4. **接媒体**（→ `03-media-compat.md`）：视频双链路、音频自托管、外链文章本地存档，一次配对配全。
5. **部署上线**（→ `04-deploy-and-domain.md`）：直传托管、`_headers`、robots/sitemap/og:image。
6. **迭代打磨**（→ `06-iteration.md` + `07-pitfalls.md`）：书面迭代一轮一轮来，改动后跑一遍坑清单自查。

## 硬约束速查

| 项 | 约束 |
|---|---|
| 托管单文件上限 | Cloudflare Pages 25 MiB（大媒体放对象存储） |
| CSS/JS 缓存 | 改内容必 bump `?v=`，否则旧缓存不刷新 |
| 字体 | 全部自托管 woff2，禁外部字体 CDN（内地不稳） |
| 大媒体直链 | 网盘直链需 `raw=1`（流式）而非 `dl=0`（下载页）；需服务端支持 Range |
| 可内嵌页面 | iframe 必须 `?embed` 参数，否则被 X-Frame-Options/CSP 拦截 |
| 音频 | 本地 MP3 自托管；`preload="metadata"` 控制预载 |
| 语言切换 | 动画克制（标题类锁宽解码即可），正文瞬时切换，不引重排 |

## 隐私与可复用性声明

本 skill 中所有链接、域名、品牌均为占位示例。落地时替换为用户自己的资源；提炼经验时沿用「平台类别」（境外网盘 / 国内设计平台 / 对象存储等）而非具体品牌绑死。
