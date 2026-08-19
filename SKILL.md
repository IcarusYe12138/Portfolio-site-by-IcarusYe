---
name: portfolio-site-kit
description: Builds trilingual portfolio / works-showcase static sites with dual-region (global + mainland China) media compatibility, self-hosted fonts, and iterative polish. Invoke when creating, restructuring, or iterating a personal portfolio, works showcase, or media-rich static site.
---

# portfolio-site-kit · 个人作品集网站构建方法论

本 skill 提炼自构建 [icarusye.site](https://icarusye.site/) 的实战经验——一个已上线的三语（EN / 简中 / 繁中）个人作品集网站：纯手写 HTML/CSS/JS + Cloudflare Pages，零框架零构建，含大量音视频与图文作品，同时保障国际与中国内地双平台可达。该站点既是这套方法论的活示例，也可作为阅读本文档时的参照。

**它不是一套固定模板，而是一套方法论**：设计规范、组件规范、跨地域媒体策略、部署策略、迭代节奏与避坑清单。把「具体实现」抽象成「可迁移的原则 + 可复用的代码片段」。

---

## 何时使用

- 用户要建个人作品集 / 作品展示站 / 简历型静态站（含音视频、图文集、iframe 嵌入）——**首次调用先走 `references/00-onboarding.md` 的接洽问卷**
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
├── CHANGELOG.md                  版本日志（本 skill 自身的迭代记录）
├── references/                   ← 分主题深度文档
│   ├── 00-onboarding.md          ★ 首次接洽：问卷、素材载体、工具链与隐私红线
│   ├── 01-design-and-style.md    设计规范与「找风格」方法论（含书面 Style Spec、文案纪律）
│   ├── 02-components.md          组件规范（顶栏/卡片/筛选/播放器/磁贴场/详情页/预载器/Contact/嵌入名片/Colophon…）
│   ├── 03-media-compat.md        ★ 音视频与图文的跨地域兼容（含区域差异四层清单）
│   ├── 04-deploy-and-domain.md   部署、缓存、域名购买指南、SEO 基础、隐私友好统计与合规、内地可达
│   ├── 05-structure-i18n.md      文件夹结构 + 三语机制（属性级 i18n 全集 + 首页架构）
│   ├── 06-iteration.md           三层迭代文档体系（总规/轮次日志/站根活档）
│   ├── 07-pitfalls.md            ★ 避坑清单（现象→原因→怎么避免）
│   ├── 08-accessibility-motion.md WCAG 2.2 基线与测试工具 + 无障碍模式 + reduced-motion 策略 + 光敏保护
│   ├── 09-performance.md         性能：字体子集分片管线、懒加载、IO 模式、Resource Hints 与图片格式
│   └── 10-content-ops.md         内容运维：作品增删改同步清单、计数自动化、周期性内容审计
│   └── 11-preship-checklist.md   ★ 上线前总检单（硬约束 + 全 checklist 一页汇总）
├── templates/                    ← 可直接复制的组件模板
│   ├── trilingual.html           三语引擎（完整属性集：i18n/alt/title/href/scramble/cursor）
│   ├── works-index.html          全部作品索引页骨架（计数自动化 + 筛选 + HIGHLIGHT）
│   ├── case-page.html            案例详情页骨架（互链列表 + 双链路 Links 区）
│   ├── 404.html                  通用失败页（4XX 语义化 + 三语 + 语言回链）
│   ├── audio-player.html         内嵌音频播放器（播放/seek/时间/下载）
│   ├── bgm.html                  背景音乐单例按钮
│   ├── tile-field.html           参数化 Metro 磁贴背景场
│   ├── marquee.html              无限滚动条（克隆×2+回卷+拖拽+联动暂停）
│   └── regional-links.html       区域化链接 / 视频双链路 / iframe 内嵌模式
├── tools/                        ← 构建与审计脚本（用法见 tools/README.md）
│   ├── collect_chars.py          收集站内 CJK 用字 → cjk-set.txt
│   ├── subset_fonts.py           按字符集子集化原字体（TTF/OTF → 中间 OTF）
│   ├── split_cjk.js              cn-font-split 分片 → unicode-range woff2 + cjk.css
│   ├── audit.sh                  一致性审计（计数/版本号/徽标/sitemap/体量 六项）
│   └── README.md                 管线用法、依赖、三坑备忘、图片处理速查
└── examples/
    └── minimal.html              活体测试页：四组件最小组装（双击即跑）
```

★ = 使用本 skill 时最先翻的四篇。

---

## 推荐工作流（新站从 0 到 1）

0. **接洽问答**（→ `00-onboarding.md`）★ 必须第一步
   - 问风格参考：代码参考 / 网站截图 / HTML 文件 / 图片或 Figma，有没有？
   - 问内容底子：简历、作品集、外链（海外+内地）齐不齐？不齐就先做风格 Demo、内容后补；
   - 引导作品清单进结构化载体（飞书 / Markdown / Excel）；
   - 告知工具链：构建推荐 TRAE（多设备实时预览，https://www.trae.cn/ ），设计原型推荐 Kimi K3（审美在线，https://www.kimi.ai/blog/kimi-k3 ）——不强制；可选 MCP（github / cloudflare / AnySearch）、多模态理解（Qwen-MM-Plugins）、网页版 logo 生成器见 `00-onboarding.md`；
   - **询问伴侣 skill**：审美与无障碍兜底建议装 frontend-design（Anthropic 官方）+ web-design-guidelines（Vercel）——先问用户是否已有同类，推荐分层表与话术见 `00-onboarding.md`；
   - **绝不擅自安装任何 MCP 或 skill**——只推荐、给命令与理由，安装须用户明确许可；
   - **信息缺失就反问，不擅自代答**。
1. **定性风格**（→ `01-design-and-style.md`）
   - 参考素材 + 作者专业方向 → 交给任意可用图片的 Agent（Kimi K3 推荐）产出一版属于作者自己的 Demo（配色、字体、母题、版式）；
   - Demo 锁定后固化为**书面 Style Spec** 再动代码——不要预设任何单一审美，更不要照抄某个现有网站。
2. **定结构**（→ `05-structure-i18n.md`）：页面清单、首页架构（单页锚点+索引页）、assets 拆分、语言机制先定型——后期改结构成本最高。
3. **铺组件**（→ `02-components.md` + `templates/`）：从 templates 复制骨架，套入 Style Spec 的 token；`examples/minimal.html` 是最小组装参考；索引页与详情页用 `works-index.html` / `case-page.html` 骨架。
4. **接媒体**（→ `03-media-compat.md`）：视频双链路、音频自托管、外链文章本地存档，一次配对配全。
5. **部署上线**（→ `04-deploy-and-domain.md`）：直传托管、`_headers`、robots/sitemap/og:image、JSON-LD 结构化数据、域名选购、（可选）隐私友好统计；部署后用 ITDOG（https://www.itdog.cn/http/ ）多地抽测海外+内地可达性，再真机过一遍。
6. **迭代打磨**（→ `06-iteration.md` + `07-pitfalls.md`）：三层文档体系 + 书面迭代一轮一轮来，改动后跑一遍坑清单自查。
7. **内容增删**（→ `10-content-ops.md`）：任何作品增删改，照同步清单执行 + `tools/audit.sh` 计数审计。
8. **上线收尾**（→ `11-preship-checklist.md`）：跑 audit.sh + 过一页总检单，全部打勾再发布。

## 隐私与可复用性声明

本 skill 中所有链接、域名、品牌均为占位示例。落地时替换为用户自己的资源；提炼经验时沿用「平台类别」（境外网盘 / 国内设计平台 / 对象存储等）而非具体品牌绑死。
