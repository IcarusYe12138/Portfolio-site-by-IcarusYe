# Changelog

本 skill 自身的迭代记录（践行 `references/06-iteration.md` 的方法论）。格式参考 Keep a Changelog；版本号语义化。

## [0.4.1] — 2026-08-19

### Added
- **三语 README 新增「设计阶段资源 / Resources for the design phase」**（README.md / zh-CN / zh-HK 同步）：
  - **图标库推荐**：simple-icons（★首选，CC0，CDN 直链）、NViconsLib Silhouette（内地专属平台补充）、thesvg（对话式 MCP 调用）、icons8-mcp（品牌色还原，SVG 需 API Key）；含中文社媒覆盖说明与许可警示；
  - **设计与原型工具**：Google Stitch（Gemini UI 生成器）、Design Skills Hub（社区设计技能注册中心）；
  - **前端 skill 作者评估**：Design Tokens（★推荐，OKLCH 与本 kit token 纪律互补）、identity-skill（可选，依赖生图模型）、Motion Skill（本栈不推荐，Framer Motion/React 与本 kit 静态优先冲突）、vercel-domain（仅当用户选 Vercel）、前端三件套已在 ★ 伴侣表。
  - 延续「充分知情权」纪律：所有推荐标注 Agent 调用方式、许可、覆盖范围与作者主观评估，绝不自作主张安装。

### Fixed / 补全
- **为推荐的前端 skill 补齐 GitHub 链接**（应作者要求，从 GitHub 检索）：
  - Design Tokens → [XINGANLIU/design-system-generator-skill](https://github.com/XINGANLIU/design-system-generator-skill)（OKLCH+亮暗适配）+ 社区版 [Owl-Listener/designer-skills](https://github.com/Owl-Listener/designer-skills#design-token)；
  - identity-skill → [Sac-Y/identity-skill](https://github.com/Sac-Y/identity-skill)；
  - Motion Skill (Framer Motion) → 社区版 [schoepplake/framer-motion-skill](https://github.com/schoepplake/framer-motion-skill)；
  - **vercel-domain 未找到可靠独立 skill 仓库**——已在文档中明确标注，其权威来源为 Vercel 官方域名文档（非社区 skill），并提示用户。

## [0.4.0] — 2026-08-19

### Added
- **港式粤语 README**（`README.zh-HK.md`）：第三份面向文；三份 README 顶部互链改为双向三选一。英文仍为英式英语，简体为白话，繁中采用港式粤语口吻。

## [0.3.0] — 2026-08-19

### Added
- **五个主题章节补全**（市场对标调研确认的空白，来源含 AnySearch 2026-08 检索验证）：
  - `04` 新增「九、SEO 基础」：Core Web Vitals 阈值表（LCP ≤2.5s / INP ≤200ms / CLS ≤0.1，CrUX 75% 判据）+ JSON-LD 结构化数据（Person / CreativeWork / SoftwareApplication 示例与 Rich Results Test 验证）+ canonical 指裸 URL + 存档页 noindex；
  - `08` 新增「一、基线：WCAG 2.2 一致性级别与测试工具」（原一~七顺延为二~八）：86 条三级构成、本 skill 基线定为 AA、4.1.1 已移除说明；NVDA / VoiceOver / 键盘 / 200% 缩放测试栈；landmarks 语义要求；**富媒体无障碍**（视频字幕、音频 transcript——作品集站最常见硬伤）；
  - `09` 新增「六、Resource Hints 与图片格式」（原六顺延为七）：preload / prefetch / preconnect / dns-prefetch 决策表与「fetchpriority 优先于 preload」要点；AVIF + picture 三级回落；Critical CSS 明确不做及理由；CWV 实验室 vs 字段数据对照；
  - `10` 新增「八、周期性内容审计」：link rot 工具表（lychee / muffet / broken-link-checker / Dead Link Checker）+ 月/季/发布前审计节奏 + 签名 URL TTL 监控方案（07 坑 #9 的对策）；
  - `04` 统计节扩展「隐私合规要点（GDPR / PIPL）」：cookieless 免横幅判据、IP 匿名化、数据留存 ≤14 个月、SaaS 路线补 Plausible / Umami 链接。
- **新工具推荐**（均落位 00 工具链 + README 双语推荐表）：
  - [ITDOG HTTP 检测](https://www.itdog.cn/http/)——部署后海外+内地多省份节点可达性批量验证（04 五/十、SKILL.md 工作流第 5 步、10 月度审计、11 E 段、README 双语）；
  - 网页版 Logo 生成器（[明日方舟：终末地风格](https://ark.ncreeper.top/) / [图叙 TuxuAI](https://www.tuxuai.com/share/inspiration?shareId=880)，标注「仅作分享，不做保证」）——风格探索期发散用（00 工具链 + 01 三步法旁注）；
  - [Qwen-MM-Plugins](https://github.com/QwenLM/Qwen-MM-Plugins)——让不具备视觉能力的 agent 理解视频/音频/图片，需自接千问 API（00 新小节 + README）；
  - [AnySearch](https://www.anysearch.com/home) MCP——对话内全网检索（00 MCP 小节 + README）。
- **安装纪律（硬规则）**：绝不未经用户明确许可安装任何 MCP / skill——只推荐、给命令与理由，由用户执行或明确授权（00 通用纪律节 + 伴侣 skill 纪律 + SKILL.md 工作流第 0 步 + 开工判据 + README 双语）。

### Changed
- `08` 全文章节重编号（一~七 → 二~八）；`09` 六→七；`04` 八/九→九/十（SEO 插入）；
- `11` 总检单补 7 项：landmarks / 字幕 transcript / 屏幕阅读器抽测 / preconnect+fetchpriority / CWV 报告 / JSON-LD+canonical / ITDOG 抽样；
- 英文 README 贯彻英式拼写（Licence 等；已有 colour / personalised / honours 全数保留）。

## [0.2.0] — 2026-08-19

### Added
- **伴侣 skill 推荐机制**（`00-onboarding.md` 新节 + `SKILL.md` 工作流第 0 步 + 双语 README）：
  - 分层推荐表（★ 必装 frontend-design / web-design-guidelines；推荐 ui-ux-pro-max / impeccable；可选 high-end-visual-design / webapp-testing），各附安装命令与「补什么位」说明；
  - 接洽话术模板 + 开工判据新增「伴侣 skill 已询问（装了/已有同类/拒绝 三态记录）」；
  - 三条纪律：先问再推（防重复安装）、skill 预算 ≤ 20–30（Anthropic 官方建议，过多致触发判定下降）、冲突时以本 skill「静态优先」为准。
  - 背景调研结论：当前生态热门 skill 集中于审美判断（frontend-design 27 万+）与工程规则（web-design-guidelines 39 万+）两条横向赛道，无作品集垂直生命周期同类；本 skill 定位为垂直方法论 + 伴侣 skill 横向补位。
- 安装方式补充 `npx skills add <本仓库>`（vercel-labs skills CLI 兼容任意 GitHub 仓库）。

## [0.1.1] — 2026-08-19

### Added
- **04-deploy-and-domain.md 新增「四、自定义域名绑定实操」**（后续章节顺延重编号）：
  - 路线 A（保留注册商 DNS + CNAME，约 10 分钟）/ 路线 B（NS 迁移 Cloudflare，上生态）完整步骤与对比表；
  - 绑定后必做：Always Use HTTPS + www/非 www 规范域重定向；
  - 排障实录三连（真实部署）：「名称服务器无效」（NS 删净 / DNSSEC 先关 / 手动 Check）、Error 1016（绑定未完成触发自动记录 / 橙云代理 / flattening）、「初始化 48h」的真实耗时预期；
  - 附：交给浏览器 Agent 执行 NS 切换的任务 Prompt 模板（含安全护栏）；
  - 内容整理自一次真实配置咨询（Perplexity 问答），已泛化所有域名 / NS / 账号信息。
- **推荐服务链接落位**：03 对象存储选型表（COS / OSS / R2 + 选择逻辑）、02 名片平台（Popl / muse link）、04 托管基线与存储行内链、00 飞书载体链接 + 可选 MCP 小节（github-mcp-server / mcp-server-cloudflare）；
- 双语 README 新增「推荐服务 / Recommended services」汇总表。

## [0.1.0] — 2026-08-19

首个打标版本。自 Initial commit 起的全部变更：

### Added
- **SKILL.md**：入口——触发条件、十条核心原则、九步工作流、文件地图、隐私声明
- **references/（12 篇）**：
  - `00-onboarding.md` 接洽问卷（风格四问 / 内容三问 / 载体推荐 / 工具链 / 隐私红线 / 开工判据）
  - `01-design-and-style.md` 找风格三步法 + 书面 Style Spec 模板 + 文案纪律
  - `02-components.md` 14 组组件规范（顶栏/卡片/筛选/播放器/BGM/磁贴场/marquee/扫转轨/详情页/预载器/Contact/嵌入名片/Colophon/速查表）
  - `03-media-compat.md` 跨地域媒体专节：视频双链路、音频自托管、本地存档 A/B 型、区域差异四层清单、限制表、落地清单
  - `04-deploy-and-domain.md` 托管、`?v=` 缓存纪律、域名三方案、域名购买指南、部署补充坑、隐私友好统计、上线总检
  - `05-structure-i18n.md` 目录结构、三语机制（setLang 九步 / 属性级 i18n 全集 / 双引擎分工 / hreflang / sr-only 镜像 / logo 语言中立）、首页架构模式
  - `06-iteration.md` 三层迭代文档体系（改版总规 / 轮次日志 / 站根活档）+ 0→9 轮节奏
  - `07-pitfalls.md` 23 条真实坑（现象→根因→怎么避免）
  - `08-accessibility-motion.md` 键盘可达、ARIA 模式表、RM 分支表、光敏保护（700ms/1000ms 节流）、语言切换动效否决史
  - `09-performance.md` 载荷分层、先子集再分片管线（含 tools 指针与实测基准）、懒加载矩阵、IO 三模式、滚动/动画纪律
  - `10-content-ops.md` 作品增删改同步清单、计数自动化、grep 审计
  - `11-preship-checklist.md` 上线前总检单（硬约束表 + B–F 六段 checklist 一页汇总）
- **templates/（9 份）**：trilingual（完整属性集引擎）、works-index（计数自动化索引页）、case-page（详情页骨架 + 互链列表）、404（4XX 语义化失败页）、audio-player、bgm、tile-field、marquee、regional-links
- **tools/**：collect_chars.py / subset_fonts.py / split_cjk.js（字体管线通用版，含三坑备忘）、audit.sh（六项一致性审计）、README.md（用法 + 图片处理速查）
- **examples/minimal.html**：四组件最小组装活体测试页
- **双语 README**（英式英语 / 简体中文）：问题表、工具链推荐、结构、原则、安装方式

### Changed
- localStorage key 与语言事件统一为 `site-lang` / `site:lang`（文档与模板一致）
- SKILL.md 瘦身：硬约束表外移至 `11-preship-checklist.md`

### 来源声明
方法论提炼自构建 [icarusye.site](https://icarusye.site/) 的实战经验；该站点为活示例与参照。
