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
1. `localStorage.setItem('yy-lang', lang)` 持久化；
2. `document.documentElement.lang` 按语言设 `en` / `zh-Hans-CN` / `zh-Hant-HK`（同时驱动 CSS 字体栈切换）；
3. `document.title = T.docTitle`；meta description / og:title / og:description 同步；
4. 遍历 `[data-i18n]` 换 innerHTML（标题类可选锁宽解码动画，正文瞬时）；
5. 遍历 `[data-langs]` 按当前语言显隐整块（display none/block）；
6. 遍历 `[data-href-en]/[data-href-zh]` 等区域化链接换 href；
7. 语言按钮 active 态 + `aria-current`；
8. 派发自定义事件（如 `case:lang`），页面级组件（筛选条、播放器、跨案例列表）监听后重建；
9. `history.replaceState` 把 `?lang=zh` 写进 URL（可直链、可分享、SEO 友好）。

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
- 语言按钮顺序、样式全站统一（如 `EN → 繁 → 简`），切换时顶栏布局纹丝不动；
- 中文专有内容（如繁体副标题）经字典字段处理，不做机器转换。

## 三、404 / 失败页

- 一个通用失败页覆盖全部 4XX（401/403/404…），文案不写死「404」（「信号丢失 / OFF THE ROUTE」式语义化）；
- 三语化 + 顶栏 + `RETURN` 按钮，回首页时读 localStorage 语言带 `?lang=`；
- 背景母题与主站一致（同款磁贴场/点阵）。
