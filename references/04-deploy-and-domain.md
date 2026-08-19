# 04 · 部署、缓存与域名策略

## 一、托管：静态直传

**推荐基线**：[Cloudflare Pages](https://pages.cloudflare.com/)（或同类静态托管）Direct Upload——拖目录上传即部署，**零构建命令、零框架依赖**。

**要点**：
- 输出目录 = 仓库根目录；HTML/CSS/JS/字体/装饰 SVG 全在页面层；
- 大媒体（PDF、长视频、长音频）放**对象存储**（[腾讯云 COS](https://cloud.tencent.com/product/cos) / [阿里云 OSS](https://cn.aliyun.com/product/oss) / [Cloudflare R2](https://www.cloudflare.com/products/r2/)，选型对比见 `03-media-compat.md`），页面层直链——绕开单文件 25 MiB 上限，也省钱流量；
- 配 `_headers` 加安全响应头：
```
/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
```
- `robots.txt`：`Allow: /`、禁抓 404 页、`Sitemap: https://<域名>/sitemap.xml`；
- `sitemap.xml` 列出全部可分享页面；
- 每页 OG 分享三件套：`og:title` / `og:description` / `og:image`（1200×630 JPG，绝对 URL）+ `twitter:card: summary_large_image`——微信/Telegram/X 卡片才会出图；
- og 标签多页站**用脚本批量挂**（枚举页面清单统一注入 og:image + 宽高声明 + twitter 卡片），不逐页手写——漏挂与不一致是事故之源；
- 内地可达性：Cloudflare Pages 的 `*.pages.dev` 域名在内地**时通时断**，绑自定义域名走 CF 解析更稳；要求高时另备境内 CDN/托管（见域名策略）。

## 二、缓存纪律（最高频翻车点）

托管平台对 CSS/JS 发 `immutable + 1y max-age` 且 URL 不变 → 浏览器**永久用旧资源**，出现「新 HTML + 旧 CSS」混合态事故。

**规则**：
- 全站所有 `assets/css|js` 引用挂版本参数：`site.css?v=20260819`；
- **每次改 CSS/JS 内容必须同步 bump `?v=` 值**（日期 + 序号，如 `20260819b`）；
- HTML 不缓存（平台默认），所以版本号写在 HTML 里即可生效；
- 字体文件内容不变时可长期缓存；换了字体重子集也要换文件名或加参数。

另：删除文件后边缘缓存仍可能短期返回 200（旧文件残影）——无引用即无害，等 TTL 过期即可，不必纠结。

## 三、域名策略

### 方案对比

| 方案 | 适用 | 取舍 |
|---|---|---|
| **单域 + Cloudflare 接入** | 海外为主、内地「能用就行」 | 最省事；内地访问 `*.pages.dev` 不稳，绑自定义域可改善；无备案则境内无 CDN 加速 |
| **单域 + 双 CDN**（境外 CF + 境内 CDN，DNS 分线路解析） | 内地体验要求高 | 境内线路需 ICP 备案；回源同一静态源站，成本翻倍 |
| **双域**（海外站 + 国内托管站，内容同步） | 内地体验最高、可接受双份维护 | 两套部署流程、两套媒体链接映射；静态站同步成本低（rsync/CI） |

**建议**：个人作品集从「单域 + CF」起步；内地反馈差再升级双 CDN（需备案）或双域。作品集内容少，双域同步其实只是「同一目录传两处 + 链接映射」。

**通用项**：
- HTTPS 全站（平台默认证书即可）；
- 主域 + `www` 301 到单一规范域；
- 备案只在「服务器/CDN 节点在境内」时才需要；纯 CF 境外节点不需要备案（代价是内地延迟与不稳）。

## 四、自定义域名绑定实操（Pages + 注册商 DNS）

> 场景：域名在注册商（腾讯云 DNSPod / 阿里云等），站点在 Cloudflare Pages。两条路线 + 三段真实排障。
> 官方文档：https://developers.cloudflare.com/pages/configuration/custom-domains/

### 路线 A：保留注册商 DNS，加 CNAME（推荐，最简单）

不动 NS，注册商继续管解析，只加一条记录指向 Pages：

1. 注册商控制台 → 域名解析（DNSPod「云解析 DNS」）→ 添加记录：
   - 绑子域（`www.` / `blog.`）：类型 `CNAME`，主机记录填子域前缀，记录值填 `your-project.pages.dev`（去掉 `https://`）；
   - 绑根域（`@`）：同样 CNAME——DNSPod 支持根域 CNAME；**部分注册商不支持**，报错就改绑子域；
2. Cloudflare Dashboard → **Workers & Pages** → 你的项目 → **Custom domains** → Set up a custom domain，输入域名；
3. CF 检测到 CNAME 即提示 Activate，确认后**自动签发免费 SSL**，全程约 10 分钟。

### 路线 B：NS 迁移到 Cloudflare（彻底，上生态）

打算用 Workers / 防护规则 / Bulk Redirects 等 CF 全家桶时选这条：

1. CF Dashboard 添加域名（Add a Site）→ CF 自动扫描复制现有 DNS 记录；
2. CF 分配两个专属 NS（形如 `xxx.ns.cloudflare.com` / `yyy.ns.cloudflare.com`）；
3. 回注册商 → 「修改 DNS 服务器」→ 选「自定义 DNS」→ **删净原 NS**（DNSPod 默认那两条），换成 CF 给的两条；
4. 等状态 Pending → Active（几分钟到 24 小时；期间建议先核对 CF 抓取的记录，尤其邮箱 MX）；
5. 之后在 Pages → Custom domains 绑定，**CNAME 由 CF 自动创建**，无需手动加。
6. 注意：只换 NS 不转注册商——域名所有权仍在注册商，不影响续费。

### 怎么选

| 对比项 | A：保留注册商 DNS | B：转 NS 到 CF |
|---|---|---|
| 复杂度 | 低（一条记录） | 中（改 NS + 等生效） |
| 生效 | 几分钟 | 数分钟–24 小时 |
| CF 生态功能（Workers 等） | 部分受限 | 完整可用 |
| 既有解析（MX 等） | 不动，零风险 | 全部迁移，需核对 |

「只想让站用自己的域名」→ A；「要深度用 CF 生态」→ B 一次到位。

### 绑定后必做（SEO 与规范域）

- SSL/TLS 设置里开 **Always Use HTTPS**；
- 设置 **www ↔ 非 www 重定向**，只保留一个规范域——否则搜索引擎收录两个版本，伤品牌一致性（对应「上线前总检」的规范域检查项）。

### 排障实录（三连，均来自真实部署）

**① 状态一直「名称服务器无效」（转 NS 后）**
- 核对 NS **逐字匹配**且旧 NS 已删净——常见错误是新旧四条并存或多打了空格；
- **DNSSEC 必须先关**：注册商侧若开着 DNSSEC，CF 永远识别不到新 NS（最隐蔽的坑）；记录列表为空才算关干净；
- 剩下就是传播时间：点「立即检查名称服务器（Check nameservers now）」手动触发；**不要反复删改 NS**，越改越乱。参考：https://developers.cloudflare.com/dns/zone-setups/troubleshooting/pending-nameservers/

**② Error 1016（Origin DNS error）**
- 含义：CF 已接管域名解析，但**没有任何记录指向源站**——多半是 Custom domain 绑定那步没在 Pages 后台真正完成（NS 在 CF 手上时，绑定动作才会触发自动建记录）；
- 检查：DNS → 记录里应有指向 `xxx.pages.dev` 的 CNAME；**代理状态必须是橙色云（已代理）**，灰色仅 DNS 不走 CDN/SSL；
- 根域绑定用 CF 的 CNAME flattening，正常无需额外配置；若之前手动加过冲突的 A 记录，删掉重试。

**③ 「正在初始化，需要长达 48 小时」**
- 官方保底上限，不是真实耗时；NS 已在 CF 上时通常**几分钟到 1 小时**转 Active；
- 卡超 1–2 小时：查 DNS 记录是否自动生成；仍无 → 删掉该自定义域重新添加一次，重新触发流程。

### 附：交给浏览器 Agent 的操作任务 Prompt（模板）

把路线 B 的 NS 切换交给浏览器 Agent（Computer Use / browser-use 类）执行时，用这类任务 Prompt——护栏比步骤更重要：

```
你是浏览器操作助手，帮我完成域名 NS 切换。每步操作前简述意图，操作后截图确认。
【背景】域名在 <注册商>，需把 NS 从 <原NS两条> 换成 Cloudflare 分配的 <新NS两条>，
站点部署在 Cloudflare Pages。
【步骤】① 登录 <注册商控制台>（遇验证码/二次验证暂停等我）→ 我的域名 → 详情页；
② 修改 DNS 服务器 → 自定义 DNS；③ 删净原两条，逐字填入新两条；④ 保存并截图。
⑤ 登录 Cloudflare → 域名概览 → 触发「检查名称服务器」，截图记录 Pending/Active 状态。
【护栏】遇双重验证/验证码/支付确认立即停下让我手动处理；除 NS 外不动任何其他设置
（DNS 记录、隐私保护、自动续费一概不碰）；完成后总结当前状态。
```

建议拆两次执行（改 NS / 等生效后再确认），避免 Agent 在传播期反复刷新卡住。

## 五、内地可达性总原则（checklist）

- [ ] 字体：全部自托管 woff2，**零外部字体 CDN**（Google Fonts 类内地不可用）
- [ ] 音频：本地 MP3
- [ ] 关键图片/海报：本地 webp
- [ ] 每条境外服务链接（网盘/在线设计/云文档）：有内地替代（境内平台镜像 / 对象存储直链 / 本地存档）
- [ ] 第三方统计/分析脚本：要么不上，要么接受内地加载失败不影响主体（`async` + 不阻塞）
- [ ] 上线后用「无梯子的内地网络 + 手机流量」实测一遍全站

**两地可达性批量验证工具**：[ITDOG HTTP 检测](https://www.itdog.cn/http/)——输入线上 URL，从全国多省份节点 + 海外节点并发测 http/https 可用性，一眼看出「哪些省份红、哪些绿」。部署完成后、以及每次大版本上线后跑一遍（内网渗透测试不必，纯可达性抽样足够）；比手工找两地朋友实测快得多，**但它不能完全替代真实设备实测**——手机流量 + 无痕窗口过一遍仍是最终判据。

## 六、域名购买指南

### 注册商怎么选

| 注册商 | 适合 | 特点 |
|---|---|---|
| **Cloudflare Registrar** | 已用 CF Pages 的首选 | 成本价（无加价）、免费 WHOIS 隐私、DNS 与托管同一家一条龙 |
| **Namecheap / Porkbun** | 海外通用 | 首年常有优惠、免费 WHOIS 隐私、界面友好 |
| **阿里云万网 / 腾讯云** | 走内地备案路线必选 | 需实名认证；ICP 备案要求域名在境内注册商处 |

### 选购纪律

- **TLD 选主流**：`.com` 最稳（全球 + 内地解析都不出幺蛾子）；`.cn` 只在走备案路线时买；**避开冷门廉价后缀**——部分在内地被整体屏蔽或 DNS 污染，邮箱信誉也差；
- **看续费价不看首年价**：首年 ¥9 续费 ¥199 的套路很常见，买前查续费价；
- **必开 WHOIS 隐私保护**（主流注册商免费），避免邮箱被爬;
- **自动续费 + 注册商锁**都打开，域名过期被抢注是最贵的事故；
- 记录好注册商账号与到期日（日历提醒），域名、托管、存储三套账号分开记档。

### 与托管的接线

- CF Pages 绑自定义域名：DNS 托管在 CF 时零配置（自动 CNAME）；DNS 在别处则手动加 CNAME（子域）或 A/ALIAS（裸域）——两条路线的完整步骤与排障见「四、自定义域名绑定实操」；
- HTTPS 用 CF 免费通用 SSL，**不要花钱买证书**；
- 内地注意：`*.pages.dev` 默认域名在内地时通时断；绑自定义域名可改善，但要内地 CDN 加速则必须 ICP 备案（域名在境内注册商 + 服务器/CDN 节点在境内才需要；纯 CF 境外节点不需要备案，代价是内地延迟与稳定性）。

## 七、部署补充坑（托管平台常见）

### `_headers` 位置
必须放在**部署产物根目录**（输出目录根），放错层级不生效也不报错。

### 直传部署 = 全量替换
Direct Upload 每次上传的是**整个站点目录快照**——这次少传一个文件，那个文件在线上就消失了。别只拖改动过的文件；部署前保证目录完整（本地保留完整站根 + git 管理可破）。

### 边缘缓存时间差
- 新增文件：部署后可能短暂 404（边缘节点传播中），几十秒到几分钟自愈；
- 删除文件：边缘可能仍短期返回 200（TTL 未到）——确认无引用即可，等过期；
- 判断「线上生效没有」以多地区/无痕窗口 + 强刷新为准，本地缓存会骗人。

### 平台配额速记（以 CF Pages 为例）
- 单文件 ≤ 25 MiB；单次部署 ≤ 20,000 个文件；单次上传压缩包有体量上限——字体分片后文件数上千时留意总数；
- 超限的不是报错就是静默失败，部署后抽查几个新文件是否 200。

### preview 与 production
- Git 集成模式每个 PR/分支有 preview URL；Direct Upload 没有——想留预览环境就多建一个项目传预览目录；
- 生产 URL 只有一个，**改 CSS/JS 必 bump `?v=`**（前文缓存纪律），preview 与 production 同理。

### 404 与 robots
- 平台默认 404 很丑：自建 `404.html` 平台会自动用作兜底（注意它也覆盖 403 等状态，文案别写死「404」）；
- `robots.txt` 里 `Disallow` 掉 404 页与不想收录的存档页，`Sitemap` 指绝对 URL。

## 八、访问统计（可选，隐私友好优先）

静态站也能有统计，三条路线按「维护成本从低到高」：

| 路线 | 代表 | 取舍 |
|---|---|---|
| **托管平台自带** | 如 Cloudflare Web Analytics | 无 cookie、免费、与 Pages 原生集成——个人站首选；数据粒度有限（够用） |
| **自托管开源** | [Umami](https://umami.is/) / GoatCounter | 数据完全自主、无 cookie 可配；需要一个常驻服务（一台小主机/容器） |
| **第三方 SaaS** | [Plausible](https://plausible.io/) / Fathom 等 | 免运维、无 cookie；订阅费；内地端点可达性需自测 |

### 隐私合规要点（GDPR / PIPL）

选型时只看功能不够，跨境个人数据处理有法定义务：

- **cookieless 优先**：上表三条路线均可无 cookie 运行——不写 cookie、不收集可识别个人身份的信息（PII），多数场景**无需 cookie 同意横幅**；一旦上 cookie 或指纹类统计（如 GA），欧盟访客需同意机制（CMP），复杂度陡增；
- **PIPL（内地）**：若明确服务内地用户，统计行为需在隐私声明中披露；数据尽量留在境内或匿名化（Cloudflare Web Analytics 不落个人数据，负担最小）；
- **GDPR（欧盟）**：IP 匿名化（`anonymize_ip` 类配置或选无 IP 收集的工具）+ 明确数据留存期限（建议 ≤ 14 个月，CrUX 窗口同量级）；
- **纪律不变**：统计脚本一律 `defer`/`async` 或无脚本 beacon，不阻塞页面；内地丢样本就丢——作品集统计只为回答「哪些作品被看」，不为精确计量。

**纪律**：
- 不上任何阻塞加载的统计脚本（`defer`/`async`，或平台的无脚本 beacon 方案）；
- 不采集 PII、不喂广告像素——作品集的统计只为回答「哪些作品被看」；
- **内地可达性自测**：境外统计端点在内地可能丢数据（请求发不出去）——要么接受样本偏差，要么自托管在两地可达的位置；
- 统计域名若被拦，不影响站点主体功能（本就异步加载，天然降级）。

## 九、SEO 基础：结构化数据、canonical 与 Core Web Vitals

静态多语言站的 SEO 三件事：让搜索引擎**读懂**（结构化数据）、**去重**（canonical）、**排名不拖后腿**（CWV）。

### 1. Core Web Vitals 阈值（Google 排名信号）

| 指标 | 含义 | Good | 需改进 | Poor |
|---|---|---|---|---|
| **LCP** | 最大内容绘制（加载速度） | ≤ 2.5s | 2.5–4.0s | > 4.0s |
| **INP** | 交互到下一帧（响应性） | ≤ 200ms | 200–500ms | > 500ms |
| **CLS** | 累积布局偏移（视觉稳定） | ≤ 0.1 | 0.1–0.25 | > 0.25 |

通过判据：CrUX 真实用户数据中至少 **75% 的访问达到 Good**。实验室数据（Lighthouse）用于开发期回归，字段数据（Search Console → Core Web Vitals 报告）才是排名依据——两者都要看，以后者为准。性能侧的落地手段（首屏图不 lazy、字体 swap、懒加载矩阵）见 `09-performance.md`。

### 2. 结构化数据（JSON-LD）

Portfolio 站三类页面各配一种 schema，帮助搜索引擎理解「这是谁 / 这是什么作品」：

```html
<!-- 首页：Person -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "Your Name",
  "url": "https://yoursite.example/",
  "jobTitle": "Your Title",
  "sameAs": ["https://github.com/you", "https://www.linkedin.com/in/you"]
}
</script>

<!-- 作品详情页：CreativeWork（datePublished / creator 指回 Person） -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "CreativeWork",
  "name": "Work Title",
  "description": "One-line description.",
  "url": "https://yoursite.example/works/slug.html",
  "creator": { "@type": "Person", "name": "Your Name" }
}
</script>
```

- 涉及软件项目可加 `SoftwareApplication`（keywords 填技术栈）；
- 验证：部署后用 Google [Rich Results Test](https://search.google.com/test/rich-results) 或 [Schema Markup Validator](https://validator.schema.org/) 过一遍；
- JSON-LD 是静态文本，随页面直出，无性能代价。

### 3. canonical 与多语言去重

`?lang=` 切换会产生同内容多 URL，需声明规范版本避免重复收录：

```html
<link rel="canonical" href="https://yoursite.example/works/slug.html">
```

- canonical 指向**不带 `?lang=` 的裸 URL**（语言变体由 hreflang 体系表达，见 `05-structure-i18n.md`）；
- `<title>` 模式统一：「页面名 — 站名」，总长 ≤ 60 字符左右；
- archive / 本地存档页**不参与收录**：`<meta name="robots" content="noindex,follow">`，并在 robots.txt 里 Disallow——存档是给访客的备胎，不是给搜索引擎的内容。

## 十、上线前总检（deploy checklist 汇总）

- [ ] `_headers` 在产物根目录；安全头生效（curl -I 验证）
- [ ] robots.txt + sitemap.xml；sitemap 内全部 URL 可达
- [ ] og:image 绝对 URL；微信/Telegram/X 实测分享卡片
- [ ] 404.html 就位且文案语义化（非 404 专属）
- [ ] 全站 CSS/JS `?v=` 一致且为最新
- [ ] 自定义域名解析 + HTTPS 正常；裸域与 www 只留一个规范域
- [ ] 大文件全在对象存储（无超限文件进部署目录）
- [ ] （如启用）统计脚本异步加载、不阻塞；内地端点可达性已知
- [ ] JSON-LD 过 Rich Results Test；canonical 指向裸 URL；存档页 noindex
- [ ] 两地可达性：ITDOG（https://www.itdog.cn/http/）多地抽样全绿 + 真机实测（海外直连 + 内地无梯子网络各过一遍全站）
