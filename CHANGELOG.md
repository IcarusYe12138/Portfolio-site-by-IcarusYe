# Changelog

本 skill 自身的迭代记录（践行 `references/06-iteration.md` 的方法论）。格式参考 Keep a Changelog；版本号语义化。

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
