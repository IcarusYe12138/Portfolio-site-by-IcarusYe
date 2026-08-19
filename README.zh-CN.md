# Portfolio Site Kit（个人作品集网站构建方法论）

一套精简、省 token 的方法论，帮（就算零代码基础的）你搭一个**三语**（英文 / 简体中文 / 繁体中文）个人作品集 / 作品展示**静态站**，兼顾国际与内地双平台可达。纯手写 HTML/CSS/JS，零框架、零构建。

[English version](README.md) · [繁體中文（港式粵語）](README.zh-HK.md)

---

## 这是一套方法论，不是一个模板

你不用先看完任何作品集、也不必读完这份 README 才能动手——**从「快速开始」就能启动**。读得越深，越少走弯路：

1. **什么资料都没看？** → 直接看 [快速开始](#快速开始)，5 步起步。
2. **有旧站想改 / 已有内容？** → 看 [skill 怎么读你的网站](#skill-怎么读你的网站)，它按需分批读，不会一股脑吞掉你全部文件。
3. **想一次搞懂判断标准？** → 看 [核心原则](#核心原则) 与 [参考文档地图](#参考文档地图)。
4. **习惯自己翻？** → 用 [目录](#目录) 慢慢逛。

这套方法论提炼自一个真实项目（[icarusye.site](https://icarusye.site/)），但**你不必参考它**也能用——它只是一份来源，不是门槛。

### 快速开始

最快的路径，0 前置文档，照着说就行：

1. **把要用到的东西给我**：贴 1–3 张你喜欢的网站/海报截图，或用一句话形容想要的感觉；没有就先跳过，之后补。
2. **列一下作品**：每件作品一个条目（标题 + 类型 + 年份 + 一个链接，海外/内地各一条更好）。
3. **说一个目标**：例如「先做个能看的单页版」「要中英双语」「作品需要内地能打开」。
4. 我会按 [references/00-onboarding.md](references/00-onboarding.md) 的接洽清单逐项问你——**我会追问你没给的信息，不会替你瞎猜**。
5. 你确定风格方向后，我再动代码，一轮只做一件事。

> 省 token 的接洽原则：**先问清、再动手；信息缺失就问，不擅自代答。** 一次只问你一份问题，答完再进下一步——不会一次性把整册书倒给你。

---

## 目录

- [它解决什么问题](#它解决什么问题)
- [这适合你吗](#这适合你吗)
- [核心原则](#核心原则)
- [skill 怎么读你的网站](#skill-怎么读你的网站)（按需分批，省 token）
- [参考文档地图](#参考文档地图)（什么时候翻哪篇）
- [仓库结构](#仓库结构)
- [安装](#安装)
- [推荐工具链](#推荐工具链)
- [推荐服务](#推荐服务)
- [设计阶段资源](#设计阶段资源)（图标 / 原型 / 图表 / 前端 skill）
- [伴侣 skill](#伴侣-skill)（接洽时问你是否装）
- [本 kit 有意不做的事](#本-kit-有意不做的事)
- [许可](#许可) · [链接时效](#链接时效)

---

## 它解决什么问题

| 问题 | 本 kit 的答案 |
|---|---|
| 无从下手——风格不明、内容不齐 | 先走接洽问卷定风格方向；风格 Demo 先行，内容文件后补 |
| 境外 CDN、字体、云盘链接在内地打不开 | 全面自托管纪律 + 双链路策略（海外直链 + 内地镜像） |
| 视频在海外能播、内地播不了 | 海外用 `<video>` 流式直链（`raw=1`），内地用可内嵌平台 iframe（`?embed`），按语言整块切换 |
| 外链文章内地无法访问 | 本地 HTML 存档：CMS 页的 CSS / 字体 / 图片全部落本地 |
| 中文字体动辄数兆载荷 | 先按站内实际字符集子集化，再按 unicode-range 分片 |
| 部署后 CSS/JS 不更新 | 缓存版本纪律：每次改内容 bump `?v=YYYYMMDD` |
| 多语言站慢慢长成几套分叉代码 | 单 DOM 三语引擎：内嵌字典 + 属性级 i18n + `?lang=` URL + 浏览器检测 |
| 迭代混乱、改着改着就散了 | 三层文档：改版总规 → 轮次决策日志 → 站根活档 |
| 作品增删后计数四处对不上 | 内容运维清单 + 从 DOM 自动计数 |

## 这适合你吗

**适合**：个人作品集 / 作品展示 / 简历型静态站；含音视频、图文集、iframe 嵌入；要国际 + 内地双平台可达；公开、无登录态、无后端。

**不适合 / 可跳过**：重后端业务系统（不走纯静态）；单语纯国内、无大媒体（可跳过双链路章节，其余仍适用）。

## 核心原则

1. **静态优先。** 纯 HTML/CSS/JS 直传，无构建命令。
2. **双地域可达。** 字体、音频、关键图片自托管；每条境外链接配内地替代。
3. **单文件上限意识。** 大媒体放对象存储，页面层保持轻量。
4. **缓存版本纪律。** 每次改 CSS/JS 必 bump `?v=`，否则浏览器用旧资源。
5. **内容优先版式。** 案例页 iframe/视频/链接排在长文本前。
6. **单一强调色。** 一个高饱和色只做行动信号，占比 ≤5%。
7. **动效克制。** 过渡 ≤250ms、ease-out；全站尊重 `prefers-reduced-motion`。
8. **触屏与鼠标分治。** hover 特效门控在 `(hover:hover) and (pointer:fine)`。
9. **一个 DOM、三种语言。** 内嵌字典就地切换；`?lang=` URL 直链；首访浏览器检测不固化。
10. **书面迭代。** 每轮把决策锁进日志再动代码，一轮一次执行完。

## skill 怎么读你的网站

**核心：按需分批、逐层推进，绝不一次性读光你的全部文件。** 既省 token，也避免噪音盖过真正重要的事。

读取顺序（每步用结论判断是否继续，需要才读下一步）：

1. **入口层**：先看索引/主页（`index.html`、`works`、目录结构、`_headers` / `robots.txt` / `sitemap.xml`）——用最小样本判断「这是什么站、什么语言、大致结构」。
2. **样式层**：看 CSS 变量 / 设计 token（配色、字体、间距）——判断风格与是否成体系。
3. **脚本层**：看交互脚本（语言切换、筛选、播放器）——判断三语机制与组件复用。
4. **媒体层**：遇到视频/音频/外链时才读对应媒体文档与链接——确认跨地域可达性。
5. **只深读你需要的参考文献**，不碰无关章节。

选文件参考 [参考文档地图](#参考文档地图)：哪一类任务就开哪一篇，不整包加载。

## 参考文档地图

`references/` 是按主题拆开的深度文档。**对应你的任务选一篇开**，不要一次全读完，省 token 也更好懂：

| 你的处境 | 开哪篇 |
|---|---|
| 新站必须第一步 | [00-onboarding](references/00-onboarding.md) — 接洽问卷、素材载体、工具链、隐私红线 |
| 要定风格方向 | [01-design-and-style](references/01-design-and-style.md) — 找风格三步法 + Style Spec + 文案纪律 |
| 要搭组件骨架 | [02-components](references/02-components.md) — 各组件何时用/要点/反面 |
| 作品要跨地域能看 | [03-media-compat](references/03-media-compat.md) — 视频/音频/图文双链路 |
| 要部署/买域名/缓存 | [04-deploy-and-domain](references/04-deploy-and-domain.md) — 托管、缓存、域名、SEO、合规 |
| 要理清文件夹与三语机制 | [05-structure-i18n](references/05-structure-i18n.md) — 目录结构 + 三语引擎 |
| 要迭代打磨节奏 | [06-iteration](references/06-iteration.md) — 三层文档体系 + 轮次节奏 |
| 每次大改前后自查 | [07-pitfalls](references/07-pitfalls.md) — 23 条真实坑 |
| 要做无障碍/动效安全 | [08-accessibility-motion](references/08-accessibility-motion.md) — WCAG 2.2、reduced-motion、光敏 |
| 要优化性能/字体 | [09-performance](references/09-performance.md) — 字体管线、懒加载、Resource Hints |
| 要增删作品 | [10-content-ops](references/10-content-ops.md) — 增删同步清单 + 计数自动化 |
| 上线前总检 | [11-preship-checklist](references/11-preship-checklist.md) — 一页总检单 |
| 想直接抄组件 / 看效果 | `templates/`（零依赖骨架）· `examples/minimal.html`（四组件双击即跑） |

## 仓库结构

```
portfolio-site-kit/
├── SKILL.md                入口：触发、核心原则、分批工作流、文件地图
├── CHANGELOG.md            skill 自身版本日志
├── references/             分主题深度文档（按任务选开，见上表）
├── templates/              可直接复制的组件骨架（0 依赖、自带注释）
│   ├── trilingual.html     三语引擎（文本/alt/title/href/解码/光标）
│   ├── works-index.html    作品索引页（计数自动化 + 筛选 + HIGHLIGHT）
│   ├── case-page.html      案例详情页（互链 + 双链路 Links）
│   ├── 404.html            通用失败页
│   ├── audio-player.html   内嵌音频播放器
│   ├── bgm.html            背景音乐单例按钮
│   ├── tile-field.html     参数化 Metro 磁贴背景场
│   ├── marquee.html        无限滚动条
│   └── regional-links.html 双链路 / 视频 / iframe
├── tools/                  构建与审计脚本（见 tools/README.md）
└── examples/
    └── minimal.html        四组件最小组装（双击即跑）
```

## 安装

最快——npm（无需 git，GitHub 慢的地区也能顺畅装）：

```bash
npx @icaruye/portfolio-site-kit@latest
```

安装器会自动探测你的 agent skills 目录（TRAE / Claude Code / Codex / Cursor / OpenCode）；加 `--dir <路径>` 手动指定，`--force` 覆盖已有安装。

其他方式：

```bash
git clone https://github.com/IcarusYe12138/Portfolio-site-by-IcarusYe.git \
  ~/.trae-cn/skills/portfolio-site-kit
# 或用 vercel-labs 的 skills CLI：
npx skills add https://github.com/IcarusYe12138/Portfolio-site-by-IcarusYe
```

（也可直接把仓库文件夹复制进你的 skills 目录。）之后你说「建作品集 / 改版 / 加语言 / 解决国内打不开」，agent 会自动调用。`tools/` 与 `examples/` 随包分发。

## 推荐工具链

- **构建用 [TRAE](https://www.trae.cn/)**：本地实时预览手机/平板/桌面视口，多设备响应式直观；主流模型可选。方法论与工具无关，其他也行。
- **设计原型用 [Kimi K3](https://www.kimi.ai/blog/kimi-k3)**：审美好；把参考截图喂给它可以拿回你自己的风格 Demo。
- 分工口诀：**Kimi 出审美，TRAE 出工程。**

（具名推荐是「作者验证过的优先项」，工具是会过期的时点选择——失效就按同类能力替换，见 [链接时效](#链接时效)。）

## 推荐服务

| 用途 | 服务 | 说明 |
|---|---|---|
| 静态托管 | [Cloudflare Pages](https://pages.cloudflare.com/) | 直传零构建，单文件 25 MiB 上限 |
| 对象存储（内地） | [腾讯云 COS](https://cloud.tencent.com/product/cos) · [阿里云 OSS](https://cn.aliyun.com/product/oss) | 大媒体外置，内地直连稳 |
| 对象存储（海外） | [Cloudflare R2](https://www.cloudflare.com/products/r2/) | 零出流量，同 CF 账号 |
| 可达性检测 | [ITDOG HTTP](https://www.itdog.cn/http/) | 全国多省 + 海外节点测线上 URL |
| 电子名片（海外/内地） | [Popl](https://popl.co/) / [muse link](https://muselink.cc/) | 可内嵌名片 iframe |
| 作品清单载体 | [飞书](https://www.feishu.cn/) | 多维表格：一行一作品、链接分列 |
| Logo 生成器（网页，风格探索） | [明日方舟：终末地](https://ark.ncreeper.top/) · [图叙](https://www.tuxuai.com/share/inspiration?shareId=880) | 仅作分享，商用前确认版权 |
| MCP（可选） | [github-mcp-server](https://github.com/github/github-mcp-server) · [mcp-server-cloudflare](https://github.com/cloudflare/mcp-server-cloudflare) · [AnySearch](https://www.anysearch.com/home) | 让 agent 直接操作 GitHub/CF，或对话内搜全网 |
| 多模态（可选） | [Qwen-MM-Plugins](https://github.com/QwenLM/Qwen-MM-Plugins) | 让无视觉 agent 理解音视频/图片，需自己的 Qwen API key |

## 设计阶段资源

设计阶段常被问的问题：图标用哪个、原型怎么做、要不要装某些前端 skill。以下是答案速查（评级是作者主观评估，不强制）：

### 图标库
| 库 | 风格 | Agent 调用 | 覆盖 | 许可/注意 |
|---|---|---|---|---|
| [simple-icons](https://github.com/simple-icons/simple-icons) ★ 首选 | 单色极简剪影，3300+ 品牌 | CDN 按 slug 直链 | QQ/微博/B 站/小红书 + 几乎全海外 | **CC0 免署名**，行业标准 |
| [NViconsLib Silhouette](https://github.com/nullice/NViconsLib_Silhouette) | 纯剪影，专为内地+全球社媒 | GitHub Raw 直链 | 微信/QQ 空间/微博 + 海外 | 上游缺内地平台的补充 |
| [thesvg](https://github.com/glincker/thesvg) | 极简品牌 SVG，6000+ | `@thesvg/mcp-server` 对话式 | 含微博，持续更新 | 按名字调工具，不用手写 URL |
| [icons8-mcp](https://github.com/icons8/icons8-mcp) | 116 风格、36 万+ | 官方 MCP，自然语言搜 | 按名可命中，需人工核实 | 免费只出 PNG，SVG 要 Key |

### 设计与原型工具
| 工具 | 作用 |
|---|---|
| [Google Stitch](https://stitch.withgoogle.com/) | Gemini AI UI 生成：文字/草图/截图 → 多屏原型 + 代码；可提取现有网站设计系统 |
| [Design Skills Hub](https://designskills.xyz/skills) ·（官网 [vaporaviator.com/works/design-skills-hub](https://vaporaviator.com/works/design-skills-hub)） | 社区设计技能注册中心：审美 + 工程两种 skill；可把 Figma 导出成复用 skill |

两者互补：Stitch **生成** UI，Design Skills Hub **编码设计判断**。

### 图表 / 数据可视化
| Skill | 作用 |
|---|---|
| [lieflat-charts](https://github.com/larashero3-dotcom/lieflat-charts) ★ | 面向 agent 的数据可视化：数据 → 精致可交互 HTML 图表（指标/时间线/分布），无需重型图表库 |

### 前端设计 skill（作者评估）
| Skill | 结论 |
|---|---|
| **Design Tokens**（OKLCH）— [XINGANLIU/design-system-generator-skill](https://github.com/XINGANLIU/design-system-generator-skill) ★ | 改一个 `hue` 全站换色，契合静态优先 + 单一强调色 |
| **identity-skill**（Sac-Y）— [Sac-Y/identity-skill](https://github.com/Sac-Y/identity-skill) | 可选：先出参考图确认再 1:1 还原，依赖生图模型 |
| **Motion Skill**（Framer Motion）— [schoepplake/framer-motion-skill](https://github.com/schoepplake/framer-motion-skill) | **本栈不推荐**：面向 React，与静态优先冲突 |

一句话：在意色彩科学装 **Design Tokens**；做 React 才考虑 **Motion Skill**（超本 kit 范围）；其余按需。

## 伴侣 skill

本 kit 管作品集的**垂直生命周期**（结构 / 双地域媒体 / 三语 / 运维 / 部署）；横向的审美与合规由伴侣 skill 补位。**接洽时会问你是否装**——绝不擅自装：

| 层 | Skill | 补什么位 |
|---|---|---|
| ★ 必装 | [frontend-design](https://github.com/anthropics/claude-code/tree/main/plugins/frontend-design)（Anthropic 官方） | 写码前锁定美学方向，反 AI slop |
| ★ 必装 | [web-design-guidelines](https://github.com/vercel-labs/agent-skills)（Vercel） | 100+ 条 WCAG 2.2 / UX 自动审计 |
| 推荐 | [ui-ux-pro-max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | 240+ 风格 / 127 字体配对——无参考时发散 |
| 推荐 | [impeccable](https://impeccable.style/) | brand 模式精修命令 |

纪律：先问再推（用户可能已有同类）；skill 总量 ≤20–30；伴侣 skill 若推 React 组件库，以本 kit「静态优先」为准。

**安装纪律（硬规则，适用一切 MCP 与 skill）：绝不未经明确许可安装任何东西。** agent 只推荐、给命令与理由，由你执行或明确授权后代理。上面所有可选工具都是「不装不碍事」。

## 本 kit 有意不做的事

- 不捆绑框架、构建器或运行时——没有会过期的东西。
- 不预设审美、只讲纪律——视觉身份来自你，不是本 kit。
- 不含具体品牌链接——文档 URL 都是通用占位符。

## 许可

[MIT](LICENSE) · Copyright (c) 2026 IcarusYe12138

方法论与代码骨架可自由复用；其提炼来源的作品集仍归作者本人所有。

## 链接时效

文档中外部链接（产品页、GitHub 仓库、社区 skill）在撰写时（2026-08）已验证可达，但可能变动或下架。若链接失效或工具停更，请按**同类能力**而非**具体品牌**替换——方法论依然成立。发现失效链接欢迎提 PR 或 issue。