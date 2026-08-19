# 05 · 文件夹结构与三语机制

## 一、文件夹结构（多页静态站参考）

```
site/
├── index.html            首页（三语合一，内嵌字典）
├── works.html            全部作品索引页
├── colophon.html         网站制作说明（可选但推荐——把设计规范公开化）
├── 404.html              通用失败页（覆盖全部 4XX）
├── robots.txt / sitemap.xml / _headers
├── works/                每个重点作品一个详情页
│   ├── case-a.html
│   └── case-b.html
├── archive/              外链文章的本地存档（内地 fallback）
│   ├── article-a.html
│   └── article-a.assets/
└── assets/
    ├── css/   site.css / detail.css / cjk.css（分片字体清单）
    ├── js/    site.js（首页）/ detail.js（子页共享引擎）/ 组件 js
    ├── fonts/ 自托管 woff2（+ split/ 中文分片目录）
    ├── audio/ 本地 MP3
    ├── works/ 作品海报 webp（多尺寸按需）
    └── og/    og-cover.jpg（1200×630）
```

**拆分原则**：
- 首页与子页 JS 分开：`site.js` 只管首页组件；`detail.js` 是子页共享引擎（语言切换 + 灯箱 + 视差等），每页只写**页面专属字典 + 页面专属逻辑**；
- 每个详情页 = 同一套骨架（topbar / case-hero / 章节 / case-aside / footer）换内容，天然一致；
- 工具脚本（字体子集、快照清理等）放 `tools/`，不进部署产物。

## 二、三语机制（单页内嵌字典）

### 核心模型
```html
<!-- 文本节点 -->
<span data-i18n="t2">TV — Winter Fire Garden</span>
<!-- aria 属性 -->
<button data-i18n-aria="apPlay" aria-label="Play">
<!-- 整块区域化内容（含媒体源切换） -->
<div class="block" data-langs="en tw">…海外视频…</div>
<div class="block" data-langs="zh">…内地 iframe…</div>
```

```js
// 每页内嵌字典（页面专属 key，en/zh/tw 三份）
window.CASE_T = {
  en:{ docTitle:"…", t2:"TV — Winter Fire Garden", cats:{ALL:"All",FILM:"Film"}, … },
  zh:{ docTitle:"…", t2:"电视 — 冬季火焰花园",     cats:{ALL:"全部",FILM:"影像"}, … },
  tw:{ docTitle:"…", t2:"電視 — 冬季火焰花園",     cats:{ALL:"全部",FILM:"影像"}, … }
};
```

### setLang 要做的事（缺一不可）
1. `localStorage.setItem('site-lang', lang)` 持久化（key 全站统一，与 `templates/trilingual.html` 一致）；
2. `document.documentElement.lang` 按语言设 `en` / `zh-Hans-CN` / `zh-Hant-HK`（同时驱动 CSS 字体栈切换）——`zh-Hant-HK` 是作者站点地域偏好（用例非规范），繁中受众以台湾为主时改用 `zh-Hant-TW`；
3. `document.title = T.docTitle`；meta description / og:title / og:description 同步；
4. 遍历 `[data-i18n]` 换 innerHTML（标题类可选锁宽解码动画，正文瞬时）；
5. 遍历 `[data-langs]` 按当前语言显隐整块（display none/block）；
6. 遍历 `[data-href-en]/[data-href-zh]` 等区域化链接换 href；
7. 语言按钮 active 态 + `aria-current`；
8. 派发自定义事件 `site:lang`（全站统一事件名，与全部 templates 一致），页面级组件（筛选条、播放器、跨案例列表）监听后重建；
9. `history.replaceState` 把 `?lang=zh` 写进 URL（可直链、可分享、SEO 友好）。

### 属性级 i18n 全集（引擎各有一张表）

| 属性 | 标记 | 典型场景 |
|---|---|---|
| `aria-label` | `data-i18n-aria` | 图标按钮（播放/下载/菜单） |
| 图片 `alt` | `data-i18n-alt` | 海报/作品图的可读描述 |
| `iframe title` | `data-i18n-title` | 嵌入内容（名片/deck）的播报名 |
| `href`（字典键） | `data-i18n-href` | **一处多语言链接首选**：CV、名片、公司官网——链接地址直接进字典（`cvHref` 等），比属性对干净 |
| 解码目标 | `data-scramble-i18n` | 切语言时更新 `data-scramble`，触发标题重解码 |
| 光标标签 | `data-cursor-i18n` | 自定义光标的 hover 文案 |
| 区域化链接（属性对） | `data-href-en` / `data-href-zh` | 索引页批量卡片的批量写法，与字典键二选一 |

### 字典约定：元信息键与 href 键

- **下划线开头 = 元信息键**：`_htmlLang` / `_title` / `_desc` / `_ogTitle` / `_ogDesc` / `_cursorText`——引擎特殊处理，不绑 DOM；
- **`xxxHref` 结尾 = 链接键**：值是 URL，供 `data-i18n-href` 取用；
- 两类键让「文档级」与「链接级」的语言切换都收敛在字典里，**单文件自查完备**。

### 双引擎分工（首页 vs 子页）

- 首页：`HOME_T` 字典 + `homeSetLang(lang, animate)`（额外更新 `body[data-lang]` 驱动 CSS 注记显隐；按钮就地处理不跳页）；
- 子页：共享 `setLang` 引擎 + 各页专属 `CASE_T`；首页/子页解码动画速度必须一致（同一把 scrambleSwap）；
- 跨页保持：子页回首页用 `CASE_MAIN = {en:'index.html', zh:'index.html?lang=zh', tw:'index.html?lang=tw'}`；站内导航统一读 localStorage；
- `sessionStorage 'skip-detect'` 守卫：手动切换过语言后跳页不再跑浏览器检测。

### 无障碍兜底：sr-only 镜像

装饰性滚动内容（marquee 数据带/词汇墙）对屏幕阅读器不可读——同区块放一个 `.sr-only`（视觉隐藏、可读性保留）的镜像列表，`data-i18n` 三语同步。同理，纯装饰背景一律 `aria-hidden="true"`。

### SEO：hreflang 互指

head 内声明三语互指 + `x-default`（配合 `?lang=` URL）：
```html
<link rel="alternate" hreflang="en" href="index.html">
<link rel="alternate" hreflang="zh-Hans-CN" href="index.html?lang=zh">
<link rel="alternate" hreflang="zh-Hant-HK" href="index.html?lang=tw">
<link rel="alternate" hreflang="x-default" href="index.html">
```

### 语言判定优先级
```
URL ?lang=  >  localStorage 已保存选择  >  首访浏览器检测（zh-Hant/HK/TW/MO→tw，其他 zh→zh，其余→en）
```
**检测结果不落 localStorage**——语言跟随浏览器，直到用户手动切换才固化。

### 动画纪律（重要）
- 语言切换是高频操作：**标题类**（h1/h2/h3/小标签）可跑「锁宽解码」——切换期间冻结元素高度 + overflow:hidden，随机字符逐位收敛到目标文本（随机字符宽度不同不再引起重排抖动）；
- **正文一律瞬时替换**，无动画；
- 不做全页扫描线、字符滚轮、遮罩层过渡——喧宾夺主且引发布局抖动，被反复推翻过的路线。

### 结构性原则
- **不维护三份 HTML**——同一 DOM + 字典切换，改结构只改一处；
- **logo 语言中立**：多语言站的 logo 用字标/缩写（如两字母字标），不做各语言本地化的文字标——logo 旁挂「各语言小字」会在切换时长短跳变、风格漂移；统一字标，全站跨越三种语言纹丝不动（统一性优先于各语言的展示欲）；
- 语言按钮顺序、样式全站统一（如 `EN → 繁 → 简`），切换时顶栏布局纹丝不动；
- 中文专有内容（如繁体副标题）经字典字段处理，不做机器转换。

## 三、首页架构模式（单页锚点 + 独立索引页）

作品集类站点的推荐首页结构（一页走完叙事，重内容外移）：

```
Hero（磁贴/点阵背景 + 姓名双行解码 + 身份编号行 + 坐标页脚）
→ 数据带（单行 marquee + 计数动画 + sr-only 镜像）——紧跟 Hero，制造动能
→ WORKS 01（sec-head 编号 + 3~5 张精选横滚轨，图上文下）
→ 纹理分隔带（装饰场低密度）
→ ABOUT 02（关键词导语 + 教育卡 + 语言表）
→ CAPABILITIES（多车道差速词汇墙）
→ EXPERIENCE（降级为 About 副标题下的时间线，不占顶级导航）
→ CONTACT 03（mailto 主 CTA + 按钮行 + 嵌入物）
→ Footer（两行结构）
```

**结构决策经验**：
- **顶级导航只留 4 项以内**（Home / Works / About / Contact）；次要板块（经历、技能）**并入相邻板块做副标**——导航越短，用户越走得完；
- 章节编号体系（sec-head 的 01/02/03 + mono meta 行）贯穿全站，档案感来自一致性而非装饰；
- **全部作品索引独立成页**（works.html），首页只放 3~5 张精选 + 「查看全部 N 件」入口——首页管叙事，索引页管完备；
- 数据带放 Hero 正下方：首屏刚结束就给出「数字证据」，比放在页底有力得多；
- 单页锚点 + 独立索引页的混合，兼顾 SEO（每页有独立 URL 与 title）与叙事（首页一镜到底）。

## 四、404 / 失败页

- 一个通用失败页覆盖全部 4XX（401/403/404…），文案不写死「404」（「信号丢失 / OFF THE ROUTE」式语义化）；
- 三语化 + 顶栏 + `RETURN` 按钮，回首页时读 localStorage 语言带 `?lang=`；
- 背景母题与主站一致（同款磁贴场/点阵）。
