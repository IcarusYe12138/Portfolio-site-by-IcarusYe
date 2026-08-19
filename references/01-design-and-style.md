# 01 · 设计规范与「找风格」方法论

> 原则：**风格来自作者本人 + AI 辅助发散，绝不预设单一审美，更不照抄现有网站。**

## 一、找风格三步法（推荐流程）

每个人做作品集时气质不同：有人先锋、有人编辑向、有人极简。推荐流程：

### 第 1 步 · 作者定性
让作者提供：
- 3~5 张他**喜欢**的参考截图（别人网站、海报、品牌页、游戏设定集均可）；
- 一句话描述自己的专业方向与内容气质（如「新闻 + 传播」「建筑摄影」「数据可视化」）；
- 明确的「不要」清单（如「不要赛博朋克」「不要动态蓝线」「不要按钮带小箭头」）——负面清单往往比正面描述更有用。

### 第 2 步 · AI 生成风格 Demo
把截图 + 描述交给任意**可用图片 + 联网**的 Agent，要求产出：
- 一版属于该作者的配色（主色/强调色/中性阶/线色）；
- 字体三角色建议（display / body / mono）；
- 一个装饰母题（motif）建议（点阵、等值线、网格、半调……）；
- 版式骨架（Hero、卡片网格、时间线、页脚的排布方式）。

拿这版 Demo 与作者对齐，反复一两轮后**锁定为风格锚点**。

> 连参考截图都没有时，可先用网页版 logo 生成器（见 `00-onboarding.md` 工具链一节）快速探索字标/配色方向——生成物只是发散输入，最终仍要收敛回书面 Style Spec。

### 第 3 步 · 组件落地
回到 `02-components.md` 的组件规范与 `templates/` 的代码骨架，把 Demo 里的 token（色、字、间距、母题）替换进去。组件结构是通用的，皮肤是作者自己的。

## 二、设计系统模板（可迁移的原则）

以下从一套「白底 + 单一强调色」的克制体系提炼，参数可整体替换为作者 Demo 的值。

### 1. 色彩：地层模型 + 单一矿脉
> **⚠ 示例值，非规范**——下面这些 hex 是作者本人站点的实测值（来自 icarusye.site），用作「长什么样」的示范，不是「必须用这个」。落地时 100% 换成作者自己的 Demo 结论（见第 2 步）。
```
--bg        #FAFAFA   页面基底（画布）
--bg2       #F5F6F7   次级条带（数据带、卡片底）
--card      #FFFFFF   卡片
--line      #E3E6EA   1px 结构分隔线（代替阴影）
--ink       #1A1A2E   文字与主笔触
--ink70/50/30          文字三级透明度
--accent    #2F2FE4   ★ 唯一强调色——只出现在「可以行动」的位置
--accent-deep #162E93 强调色 hover 深度
```
纪律：
- 强调色只做**行动信号**：链接、焦点环、进度条、动线、可交互提示；**绝不做装饰**。
- 任意视图中强调色占比 **≤5%**。
- 层级用「透明度阶梯 + 1px 发丝线」表达，不用阴影堆层级。

### 2. 字体：三角色制
| 角色 | 作用 | 建议 |
|---|---|---|
| Display | 大标题、Hero、章节题 | 几何感/工业感无衬线，300–500 字重 + 0.1–0.2em 字距 |
| Body | 正文 | 15px / 1.65 行高 / 最长 62–64ch |
| Mono | 规格、编号、日期、hex、坐标 | 编号与数据全部 `font-variant-numeric:tabular-nums` |

- 西文用**可变字体**或少量字重单文件，`font-display:swap`；
- 中文与西文字体族用 CSS 变量拼接（`--f-disp:'X',var(--f-cjk),系统中文回退`），`html[lang]` 切换 `--f-cjk` 顺序；
- 字体必须**自托管**（内地可达性，见 `04-deploy-and-domain.md`）。

### 3. 版式规则
- **零圆角**（或全站统一极小值），1px 发丝线代替阴影；
- **呼吸感**：区块间距用 `clamp(48px,7vh,84px)` 级别；`--gutter:clamp(20px,4vw,64px)`；`--maxw:1440px` 封顶；
- **内容优先**：作品详情页 iframe / 视频 / 外链按钮排在长文本之前；
- **图上文下**：16:9 大图卡用「媒体在上、标题在下」布局，避免严重裁切；
- 编号文化：卡片、章节、案例全部带 mono 编号（01/02/…），形成档案感；
- 4 档断点：Mobile `<768px` / Tablet `768–1023px` / Desktop `1024–2559px` / Ultra `≥2560px`；超宽屏**砍装饰不放大布局**（删浮动导航点等）。

### 4. 装饰母题：数据驱动，不用照片
装饰背景不用照片、不用 AI 生成图，用**代码生成的参数化图形**：
- 点阵场（`radial-gradient` 平铺）作全局底纹；
- 磁贴场 / 等值线 / 三角点阵等单一母题贯穿全站（见 `templates/tile-field.html`）；
- 好处：零图片请求、随容器自适应、密度可调、风格高度统一。

### 第 4 步 · 书面设计规范（Style Spec）
风格 Demo 锁定后、写代码之前，把 Demo 固化成**一页书面规范**——它是后续所有页面唯一的设计依据（colophon 也可引用它说明「设计遵循一份唯一的书面规范」）。必含五节：

1. **Token 表**：色彩（含使用场景与占比上限）、字体三角色、间距/圆角/层级规则；
2. **版式范式**：Hero / 卡片网格 / 时间线 / 页脚等区块的排布方式（可附 Demo 截图编号引用）；
3. **交互规范**：动效时长上限、曲线、触发方式、hover 态样式；
4. **警戒线（Guardrails）**：明确「禁止事项」——如强调色不得作装饰、禁弹跳动效、按钮不带箭头图标；
5. **Checklist**：新页面完成后的设计自查项。

规范一经定稿，任何偏离都要先改规范再改代码——否则风格会在迭代中漂移。

## 三、文案纪律（通用规则）

- **选定一种英语变体并全站贯彻**（英式/美式自选，但只能有一种：colour/color、optimise/optimize、honours/honors 不得混用；中文站同理：简繁不得混排）；
- **数据分隔符统一**：数据行/元信息里的分隔符全站只用一种（推荐 `·`），不混用 `|`、`—`、`/`；
- **正文禁用 em-dash（——/—）**：英文正文用逗号或括号替代，避免排版突兀；
- 编号体系统一（mono 字体 + `tabular-nums`，01/02… 前导零补齐）；
- 数字/年份/单位格式全站一致（如 `2026.08`、`×N`、`8:53`）。

## 四、反面示范（常见翻车）

| 反面 | 为什么翻车 |
|---|---|
| 强调色当装饰大面积铺 | 稀释信号功能，用户找不到「哪里能点」 |
| 阴影 + 圆角 + 渐变全上 | 层级混乱，廉价感；发丝线体系更高级 |
| 按钮/链接带小箭头图标 | 视觉碎；用 hover 变色 + 位移即可表达可点 |
| 语言切换做全页扫描线/字符滚轮 | 高频操作动效喧宾夺主、引发布局抖动（详见 07 坑 #14） |
| 直接复刻某个知名网站 | 一是版权/气质错配，二是作者自己的内容撑不起来 |
| 灰度 hover 滤镜无媒体查询 | 触屏设备无 hover，图片永远灰色（详见 07 坑 #13） |

## 五、设计阶段资源（按需主动推荐）

> 本节是**推荐速查表**：当用户在实际建站中表现出对应需求（找图标、要原型、做图表、纠结装不装设计类 skill），**主动开口介绍下表相关项、问要不要用/装**——经许可才行动，绝不擅自安装（安装纪律见 `00-onboarding.md`）。评级是作者主观评估，不强制。

### 图标库（用户说「要放社交媒体/品牌图标」时）

| 库 | 风格 | Agent 调用 | 覆盖 | 许可/注意 |
|---|---|---|---|---|
| [simple-icons](https://github.com/simple-icons/simple-icons) ★ 首选 | 单色极简剪影，3300+ 品牌 | CDN 按 slug 直链 | QQ/微博/B 站/小红书 + 几乎全海外 | **CC0 免署名**，行业标准 |
| [NViconsLib Silhouette](https://github.com/nullice/NViconsLib_Silhouette) | 纯剪影，专为内地+全球社媒 | GitHub Raw 直链 | 微信/QQ 空间/微博 + 海外 | 上游缺内地平台的补充 |
| [thesvg](https://github.com/glincker/thesvg) | 极简品牌 SVG，6000+ | `@thesvg/mcp-server` 对话式 | 含微博，持续更新 | 按名字调工具，不用手写 URL |
| [icons8-mcp](https://github.com/icons8/icons8-mcp) | 116 风格、36 万+ | 官方 MCP，自然语言搜 | 按名可命中，需人工核实 | 免费只出 PNG，SVG 要 Key |

### 设计与原型工具（用户没参考素材 / 想快速出多屏原型时）

| 工具 | 作用 |
|---|---|
| [Google Stitch](https://stitch.withgoogle.com/) | Gemini AI UI 生成：文字/草图/截图 → 多屏原型 + 代码；可提取现有网站设计系统 |
| [Design Skills Hub](https://designskills.xyz/skills)（官网 [vaporaviator.com/works/design-skills-hub](https://vaporaviator.com/works/design-skills-hub)） | 社区设计技能注册中心：审美 + 工程两种 skill；可把 Figma 导出成复用 skill |

两者互补：Stitch **生成** UI，Design Skills Hub **编码设计判断**。同类替代见 `00-onboarding.md` 的「工具是会过期的时点选择」原则。

### 图表 / 数据可视化（用户说「想放数据图表」时）

| Skill | 作用 |
|---|---|
| [lieflat-charts](https://github.com/larashero3-dotcom/lieflat-charts) ★ | 面向 agent 的数据可视化：数据 → 精致可交互 HTML 图表（指标/时间线/分布），无需重型图表库，自带 SKILL.md |

### 前端设计 skill（用户问「要不要装 XX 设计 skill」时）

| Skill | 结论 |
|---|---|
| **Design Tokens**（OKLCH）— [XINGANLIU/design-system-generator-skill](https://github.com/XINGANLIU/design-system-generator-skill) ★ | 改一个 `hue` 全站换色，契合静态优先 + 单一强调色 |
| **identity-skill** — [Sac-Y/identity-skill](https://github.com/Sac-Y/identity-skill) | 可选：先出参考图确认再 1:1 还原，依赖生图模型 |
| **Motion Skill**（Framer Motion）— [schoepplake/framer-motion-skill](https://github.com/schoepplake/framer-motion-skill) | **本栈不推荐**：面向 React，与静态优先冲突 |

一句话：在意色彩科学装 **Design Tokens**；做 React 才考虑 **Motion Skill**（超本 kit 范围）；其余按需。
