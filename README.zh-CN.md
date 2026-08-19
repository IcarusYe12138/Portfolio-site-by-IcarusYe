# Portfolio Site Kit（个人作品集网站构建方法论）

一套经过真实项目检验的 Skill：构建同时面向国际与中国内地用户的三语（英文 / 简体中文 / 繁体中文）作品集与展示类静态网站。

本 kit 提炼自构建 [icarusye.site](https://icarusye.site/) 的实战经验——一个已上线的作品集：纯手写 HTML/CSS/JS + Cloudflare Pages，零框架、零构建，大量使用音频、视频、在线嵌入文档与长图文，全部内容在防火墙两侧均可正常访问。该站点既是这套方法论的活示例，也可作为阅读本文档时的参照。

**这不是一套拿来即抄的模板，而是一套方法论**：接洽问卷、设计规范、组件规格、双地域媒体策略、部署纪律、三层文档体系，以及一份 23 条真实翻车记录的避坑清单，每条都按「现象 → 根因 → 怎么避免」格式沉淀。

[English version](README.md) · [繁體中文（港式粵語）](README.zh-HK.md)

---

## 它解决什么问题

| 问题 | 本 kit 的答案 |
|---|---|
| 无从下手——风格不明、内容不齐 | 先走接洽问卷：风格参考（代码 / 截图 / HTML / Figma）、简历与作品清单、链接核对；风格 Demo 先行，内容文件后补 |
| 境外 CDN、字体、云盘链接在内地打不开 | 全面自托管纪律 + 双链路策略（海外直链 + 内地镜像） |
| 视频在海外能播、内地播不了 | 海外用 `<video>` 流式直链（`raw=1`），内地用可内嵌平台 iframe（`?embed`），按语言整块切换 |
| 外链文章内地无法访问 | 本地 HTML 存档模式：CMS 页面 CSS / 字体 / 图片全部落本地；JS 驱动的滚动叙事页只落素材 |
| 中文字体动辄数兆载荷 | 先按「站内实际字符集」子集化，再按 unicode-range 分片 |
| 部署后 CSS/JS 不更新 | 缓存版本纪律：每次改内容必须 bump `?v=YYYYMMDD` |
| 多语言站慢慢长成几套分叉代码 | 单 DOM 三语引擎：内嵌字典 + 属性级 i18n 全集 + `?lang=` URL + 浏览器检测 |
| 迭代混乱、改着改着就散了 | 三层文档体系：改版总规 → 轮次决策日志 → 站根活档 |
| 作品增删后计数四处对不上 | 内容运维清单：同步点逐项枚举，计数从 DOM 自动计算 |

## 推荐工具链

- **构建用 [TRAE](https://www.trae.cn/)**：本地实时预览手机 / 平板 / 桌面多设备视口，做多模态响应式适配直观高效；主流模型可选。当然不限制其他工具——本方法论与工具无关。
- **设计原型用 [Kimi K3](https://www.kimi.ai/blog/kimi-k3)**：当前可用于网页设计的模型里审美足够好；把参考截图喂给它，产出属于你自己的风格 Demo。Demo 定稿后再进工程。
- 分工口诀：**Kimi 出审美，TRAE 出工程。**

## 推荐服务

| 用途 | 服务 | 说明 |
|---|---|---|
| 静态托管 | [Cloudflare Pages](https://pages.cloudflare.com/) | 直传零构建；单文件 25 MiB 上限 |
| 对象存储（内地向） | [腾讯云 COS](https://cloud.tencent.com/product/cos) · [阿里云 OSS](https://cn.aliyun.com/product/oss) | 大媒体外置，内地直连稳定 |
| 对象存储（海外向） | [Cloudflare R2](https://www.cloudflare.com/products/r2/) | 零出口流量费；与 Pages 同账号 |
| 两地可达性检测 | [ITDOG HTTP 检测](https://www.itdog.cn/http/) | 全国多省份 + 海外节点并发测线上 URL；每次部署后跑一遍 |
| 电子名片（海外） | [Popl](https://popl.co/) | 可嵌入名片 iframe |
| 电子名片（内地） | [muse link](https://muselink.cc/) | 内地可达的名片 iframe |
| 作品清单载体 | [飞书](https://www.feishu.cn/) | 多维表格：一行一作品、链接分列 |
| Logo 生成器（网页，风格探索用） | [明日方舟：终末地风格](https://ark.ncreeper.top/) · [图叙 TuxuAI](https://www.tuxuai.com/share/inspiration?shareId=880) | 仅作分享、不做保证——商用前自行确认版权 |
| MCP（可选） | [github-mcp-server](https://github.com/github/github-mcp-server) · [mcp-server-cloudflare](https://github.com/cloudflare/mcp-server-cloudflare) · [AnySearch](https://www.anysearch.com/home) | 让 agent 直接操作 GitHub / Cloudflare，或在对话内搜索全网 |
| 多模态（可选） | [Qwen-MM-Plugins](https://github.com/QwenLM/Qwen-MM-Plugins) | 让不具备视觉能力的 agent 也能理解视频 / 音频 / 图片；需自接千问 API key |

## 仓库结构

```
├── SKILL.md                  Skill 主入口：触发条件、核心原则、工作流、文件地图
├── CHANGELOG.md              本 skill 自身的版本日志
├── references/
│   ├── 00-onboarding.md          接洽问卷、内容载体、工具链与隐私红线
│   ├── 01-design-and-style.md    设计 token + 「找风格」方法论 + 文案纪律
│   ├── 02-components.md          组件规格：顶栏、卡片、筛选、播放器、详情页、预载器、Contact、嵌入名片、Colophon
│   ├── 03-media-compat.md        跨地域媒体兼容（视频 / 音频 / 网页存档 / 区域差异四层清单）
│   ├── 04-deploy-and-domain.md   托管、缓存纪律、自定义域名绑定实操（双路线+排障）、域名购买指南、SEO 基础、隐私友好统计与合规、内地可达性
│   ├── 05-structure-i18n.md      文件夹结构 + 三语引擎 + 首页架构
│   ├── 06-iteration.md           三层文档体系（总规 / 轮次日志 / 站根活档）
│   ├── 07-pitfalls.md            23 条坑，每条按「现象 → 根因 → 怎么避免」
│   ├── 08-accessibility-motion.md WCAG 2.2 基线与测试工具 + 无障碍模式 + reduced-motion 策略 + 光敏保护
│   ├── 09-performance.md         性能：字体子集分片管线、懒加载、IO 模式、Resource Hints 与图片格式
│   ├── 10-content-ops.md         内容运维：作品增删同步清单、计数自动化、周期性内容审计
│   └── 11-preship-checklist.md   上线前总检单（硬约束 + 全部 checklist 一页汇总）
├── templates/                    可直接复制的组件骨架
│   ├── trilingual.html           三语引擎（完整属性集：文本/alt/title/href/解码/光标）
│   ├── works-index.html          全部作品索引页骨架（计数自动化 + 筛选 + HIGHLIGHT）
│   ├── case-page.html            案例详情页骨架（互链列表 + 双链路 Links 区）
│   ├── 404.html                  通用失败页（4XX 语义化 + 三语 + 语言回链）
│   ├── audio-player.html         内嵌音频播放器（播放 / seek / 时间 / 下载，单实例）
│   ├── bgm.html                  背景音乐单例按钮
│   ├── tile-field.html           参数化 Metro 磁贴背景场
│   ├── marquee.html              无限滚动条（克隆×2 + 回卷 + 拖拽 + 联动暂停）
│   └── regional-links.html       双链路模式（raw=1 / ?embed / data-href-* / 点击加载）
├── tools/                        构建与审计脚本（用法见 tools/README.md）
│   ├── collect_chars.py          收集站内 CJK 用字 → 字符集清单
│   ├── subset_fonts.py           按字符集子集化原字体（产中间 OTF）
│   ├── split_cjk.js              cn-font-split 分片 → unicode-range woff2 + cjk.css
│   ├── audit.sh                  一致性审计六项（计数 / ?v= / 徽标 / sitemap / 体量）
│   └── README.md                 管线用法、依赖、三坑备忘、图片处理速查
└── examples/
    └── minimal.html              活体测试页：四组件最小组装（双击即跑）
```

## 核心原则

1. **静态优先。** 纯 HTML/CSS/JS 直传，无构建命令。
2. **双地域可达。** 字体、音频、关键图片自托管；每条境外服务链接都配内地替代。
3. **单文件上限意识。** 大媒体放对象存储（静态托管常有 25 MiB 单文件限制），页面层保持轻量。
4. **缓存版本纪律。** 每次改 CSS/JS 内容必须 bump `?v=`，否则浏览器永久使用不可变旧副本。
5. **内容优先版式。** 案例页里 iframe、视频、链接排在长文本之前。
6. **单一强调色。** 唯一的高饱和色只做行动信号（链接、焦点、进度），绝不做装饰，任意视图占比 ≤5%。
7. **动效克制。** 过渡 ≤250ms、ease-out；语言切换正文瞬时替换；全站尊重 `prefers-reduced-motion`。
8. **触屏与鼠标分治。** hover 特效只在 `(hover:hover) and (pointer:fine)` 下生效；触屏默认看到完整状态。
9. **一个 DOM，三种语言。** 每页内嵌字典就地切换；`?lang=` URL 支持直链；首访浏览器检测但不固化。
10. **书面迭代。** 每轮把决策锁进日志（用户原话 → 根因 → 方案 → 状态）再动代码，然后一次执行完。

## 使用方式

### 安装（TRAE 或任何支持 skill 的 agent）

```bash
git clone https://github.com/IcarusYe12138/Portfolio-site-by-IcarusYe.git \
  ~/.trae-cn/skills/portfolio-site-kit
# 或用 vercel-labs 的 skills CLI：
npx skills add https://github.com/IcarusYe12138/Portfolio-site-by-IcarusYe
```

（或把仓库文件夹复制进你的 skills 目录。）之后当你要求创建、重构或迭代作品集、作品展示站、富媒体静态站时，agent 会自动调用。`tools/` 与 `examples/` 随仓库分发——字体管线与一致性审计用法见 `tools/README.md`。

### 伴侣 skill（接洽时会询问是否安装）

本 skill 管作品集的**垂直生命周期**（结构 / 双地域媒体 / 三语 / 内容运维 / 部署）；横向的审美与合规由伴侣 skill 补位，接洽时按分层表询问：

| 层 | Skill | 补什么位 |
|---|---|---|
| ★ 必装 | [frontend-design](https://github.com/anthropics/claude-code/tree/main/plugins/frontend-design)（Anthropic 官方） | 写码前锁定美学方向、反 AI slop |
| ★ 必装 | [web-design-guidelines](https://github.com/vercel-labs/agent-skills)（Vercel） | 100+ 条 WCAG 2.2 / UX 自动审计 |
| 推荐 | [ui-ux-pro-max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | 240+ 风格库 / 127 字体配对——无参考素材时的发散器 |
| 推荐 | [impeccable](https://impeccable.style/) | brand 模式精修命令（typeset / colorize / bolder / quieter） |

纪律：先问再推（用户可能已有同类）；skill 总量控制在 20–30 个内；伴侣 skill 若推 React 组件库，以本 skill 的「静态优先」原则为准。

**安装纪律（硬规则，适用于一切 MCP 与 skill）：绝不未经用户明确许可就安装任何东西。** agent 只负责推荐——给出命令、理由与影响，由用户自己执行，或明确授权后代为执行。上表所有可选工具都是「不装不碍事」：没有任何流程环节依赖它们。

### 当作纯参考文档

`references/` 目录本身就是一本独立手册。建议入口：

- 项目启动前 → 先读 `references/00-onboarding.md`（接洽问卷与隐私红线）；
- 关心跨地域媒体 → 从 `references/03-media-compat.md` 读起；
- 每次大改前后 → 把 `references/07-pitfalls.md` 当 checklist 过一遍；
- 上线之前 → 用 `references/09-performance.md` 过字体管线与懒加载矩阵；
- 作品增删时 → 照 `references/10-content-ops.md` 的同步清单执行；
- 每次发布前 → `references/11-preship-checklist.md` 一页总检单收尾；
- 需要组件骨架 → 直接抄 `templates/`，全部零依赖、自带注释；
- `examples/minimal.html` → 双击浏览器打开，看四组件的最小拼装。

## 新站建议工作流

1. **接洽问答**（`references/00-onboarding.md`）：风格参考（代码 / 截图 / HTML / Figma）、简历与作品清单、海外+内地链接核对。文件不齐？先做风格 Demo、内容后补；作品清单进结构化载体（飞书 / Markdown / 表格）。
2. **定风格**：把参考截图交给支持图片的 agent（推荐 Kimi K3），产出属于作者自己的风格 Demo（配色、字体、母题、版式），锁定为书面设计规范。绝不照抄现有网站。
3. **定结构**：页面清单、首页架构、assets 布局、语言机制——结构越晚改越贵。
4. **铺组件**：从 `templates/` 复制骨架（详情页用 `case-page.html`），套入设计规范的 token。
5. **接媒体**：视频双链路、音频自托管、文章本地存档，一次配全。
6. **上线**：直传托管、`_headers`、robots、sitemap、og:image、域名选购。
7. **书面迭代**（总规 → 轮次日志 → 站根活档），每轮结束过一遍避坑清单。
8. **内容增长**：作品增删一律走内容运维清单，计数不漂移。

## 本 kit 有意不做的事

- 不捆绑任何框架、构建器或运行时：没有会过期的东西。
- 不预设审美，只讲纪律：视觉身份来自作者本人，而不是本 kit。
- 不含任何具体品牌链接：文档中的 URL 全部为通用占位符（`overseas.example`、`mainland.example`）。

## 许可

[MIT](LICENSE) · Copyright (c) 2026 IcarusYe12138

方法论与代码骨架可自由复用；其提炼来源的作品集仍归作者本人所有。
