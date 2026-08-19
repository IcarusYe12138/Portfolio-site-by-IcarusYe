# 02 · 组件规范

> 每个组件按「何时用 / 关键要点 / 反面示范」组织。可复制骨架在 `../templates/`。

## 1. 顶栏 Topbar

**何时用**：全站常驻导航；多页站每页一致。

**要点**：
- 毛玻璃效果（`rgba(白,.92)` + `backdrop-filter:blur`），滚动 >24px 后才出现底色与边框——**初始背景必须是纯白**（iOS Safari 顶部会露底色边，见 07 坑 #12）；
- 内容：logo（左）+ 语言切换 + 背景音乐按钮 + 返回（右）；导航项垂直对齐（`align-items:center`）；
- 方向感知收起：连续下滑累计 >120px 隐藏顶栏/页脚，上滑或 600ms 空闲或页顶/页底立即归位；
- **移动端页脚必须在文档流内**（不 sticky），避免占视口；
- 语言切换时顶栏**纹丝不动**（高度固定，文字不跳动）。

**反面**：导航项基线不齐；hover 效果被相邻元素遮挡（注意 z-index 与层叠上下文）。

## 2. 作品卡片 .cell

**何时用**：全部作品网格、精选轨、外链型作品。

**要点**：
```html
<a class="cell" data-cat="FILM"
   data-href-en="<海外链接>" data-href-zh="<内地链接>"
   href="<海外链接>" target="_blank" rel="noopener" data-cursor="WATCH">
  <div class="cell-media">
    <span class="cell-idx">02</span>
    <span class="cell-hl" data-i18n="hlBadge">HIGHLIGHT</span>
    <img src="assets/works/xxx.webp" alt="…" loading="lazy">
  </div>
  <div class="cell-cap">
    <span class="cell-title" data-i18n="t2">标题</span>
    <span class="cell-cat" data-i18n="c2">FILM · 24</span>
  </div>
</a>
```
- 媒体区固定 `aspect-ratio:16/9`，`object-fit:cover`；**图上文下**；
- 编号角标（mono，左上）、HIGHLIGHT 徽标（强调色底白字，右上，只在精选作品出现）；
- 灰度→显色 hover **只在精确指针设备**：
```css
@media (hover:hover) and (pointer:fine){
  .cell-media img{filter:grayscale(1)}
  .cell:hover .cell-media img{filter:grayscale(0);transform:scale(1.03)}
}
```
- hover：边框变强调色 + `translateY(-3px)` + 极轻投影；
- 区域化链接：`data-href-en` / `data-href-zh`，语言切换时 JS 整体换 `href`（见 `templates/regional-links.html`）；
- 外链卡必须 `target="_blank" rel="noopener"`。

**反面**：左右图文布局裁 16:9 图；徽标与「获奖标记」混用同一套符号。

## 3. 分类筛选 Filter Bar

**何时用**：全部作品页（≥10 件作品才值得）。

**要点**：
- 按钮式 `fbtn`：`分类名<sup>计数</sup>`；当前项 `.on` 强调色描边；
- 切换动画 = **淡入 + 上移 24px + scale(.96→1)**，90ms 错落（stagger），500ms ease-out：
```js
show.forEach((c,i) => {
  c.style.display = '';
  c.classList.add('f-pre','f-run');
  c.style.transitionDelay = (i*90)+'ms';
});
requestAnimationFrame(()=>requestAnimationFrame(()=>{
  show.forEach(c => c.classList.remove('f-pre'));
}));
```
- 动画结束清 transitionDelay，避免污染后续 hover 过渡；
- 语言切换时用当前字典重建按钮文案并保持当前分类选中态。

**反面**：display 切换无过渡（生硬）；stagger 写进 CSS transition-delay 不清理（后续动画全部延迟）。

## 4. 内嵌音频播放器 .aplayer

**何时用**：作品型音频（广播、配音、播客片段）在列表/详情页内直接试听。

**要点**（完整代码见 `../templates/audio-player.html`）：
- 结构 = 播放/暂停按钮 + 可拖 seek 轨道（fill + 菱形 knob）+ 当前/总时长 + 下载按钮；
- **全站单实例**：点新播放器自动暂停旧的；
- `new Audio()` + `preload='metadata'`（只拉时长，不拉全文件）；
- seek 用 pointer capture：`pointerdown` 开始、`pointermove` 跟手、`pointerup` 结束，`touch-action:none` 防滚动冲突；
- 音频文件**本地自托管**（禁外部 CDN），三种语言可配不同 `data-src-*`；
- 时间格式 `m:ss`，`tabular-nums` 防抖动。

**反面**：`<audio controls>` 原生控件（各浏览器样式不一、无法双语 aria）；多个播放器同时响；preload='auto' 浪费首屏带宽。

## 5. 背景音乐 BGM 单例

**何时用**：全站氛围音乐，可选功能。

**要点**（见 `../templates/bgm.html`）：
- **默认不播**（浏览器自动播放策略也要求用户手势）；点击才 `new Audio()` 并 `preload='none'`；
- `loop=true`，音量 ~0.7；
- 顶栏一个小按钮（音符图标 + "Music"），`aria-pressed` 表状态；
- 不需要页面间连续播放（跨页续播体验差且复杂）。

**反面**：自动播放（被浏览器拦 + 打扰用户）；音量 100%。

## 6. Metro 磁贴场 Tile Field

**何时用**：Hero 背景、分区装饰、空区块点缀——全站统一的装饰母题。

**要点**（完整代码见 `../templates/tile-field.html`）：
- JS 生成：单一强调色两档透明度（5%/10%），1×1 为主少量 2×1/2×2，1–2 块实心强调色点睛；
- 密度公式 `p = ax^pow × .45 + .008`，`ax` 为横轴（可 `data-dir="diag"` 改对角）——左缘近乎留白、右侧渐密；
- 每场可调：`data-density`（总量）、`data-pow`（疏密指数，越大越空）、`data-cell`（格子 px）；
- ~10% 磁贴随机 7–15s 周期翻转（Win10 Live Tile 效果），负延迟错峰；
- `resize` 防抖重建；`prefers-reduced-motion` 时静态无翻转。

**反面**：三档以上透明度 + 高密度 + 高翻转率叠加 =「看起来特别花」；用图片拼贴代替代码生成（请求多且不自适应）。

## 7. 无限滚动条 Marquee

**何时用**：数据带、能力词汇墙等单行横滚信息。

**要点**（完整代码见 `../templates/marquee.html`）：
- 结构 = 隐藏滚动条的 overflow 容器（lane）+ `width:max-content` 内容行（row）；**内容克隆 ×2**，JS 保证一半宽度 ≥ 视口宽（不足则继续克隆，上限 4 轮）；
- rAF 推进 `scrollLeft`，越半宽回卷（`-half / +half`）实现无缝循环；
- **拖拽**：鼠标 pointer capture 1:1 跟手，松手 ~400ms 后恢复自动滚；触屏走原生滚动；
- **联动暂停**：hover 任一滚动带暂停**所有**滚动带（多带同屏时体验统一）；
- **关键坑**：自动滚动也会触发 scroll 事件，不能用 scroll 事件判「用户在操作」——只用真实输入（wheel/touch/pointerdown）更新 lastUser 时间戳（详见 07 坑 #11）；
- 克隆节点必须移除 `data-count` 等动画属性，防重复触发计数动画。

**反面**：CSS `animation:translateX` 无限滚（内容不定宽就断裂、无法拖拽）；hover 暂停做单带不联动。

## 8. 横向扫转轨道（精选作品轨）

**何时用**：首页 3~5 张编辑精选卡的横向滑动展示。

**要点**：
- `overflow-x` + `scroll-snap`；桌面端 hover 时**劫持滚轮**（垂直滚轮→水平滚动，到两端放行垂直滚动让页面继续走）；
- 桌面端拖拽：pointerdown 后位移 >5px 才 setPointerCapture——**阈值门控**保证纯点击仍能进链接；拖拽结束吞掉 trailing click；
- 用细进度条（scaleX）代替左右箭头按钮；移动端原生触摸滚动 + 明确的可滑动提示（双向箭头，首次拖拽后淡出）——不要用小圆点指示器。

## 9. 案例详情页（Case Page）

**何时用**：重点作品的独立页面（每站 3~8 个）；全站复用率最高的页面结构——骨架相同换内容，天然一致。

**要点**（完整骨架见 `../templates/case-page.html`）：
- 结构链：`topbar`（logo + 语言 + 返回）→ `case-hero`（海报 + 标题 + 元信息）→ `case-grid`（`case-aside` 事实侧栏 sticky + `case-art` 编号章节）→ `next-proj` → footer；
- **内容优先硬规则：Links 永远是第 01 节**——外链/iframe/视频先于长文出现（「看作品」优先于「读介绍」）；
- 章节标题带 `data-n` 编号（01/02/…），全站详情页编号语义一致；
- 事实侧栏 = k-v 行（领域/年份/角色/团队），`position:sticky` 随正文滚动；
- **案例互链列表**：JS 生成——当前案例置顶 + 强调色标记 + `aria-current="page"` 不可点，其余直链；语言切换时按字典重建；移动端（<960px）经 matchMedia 自动移到正文之后；
- 交互增强四件套：媒体淡入缩放（`.rv-s`）、链接按钮 hover、章节标题视差、图片 lightbox；
- 页面 = 页面专属字典 `CASE_T` + 共享引擎，不复制引擎代码。

**反面**：每个详情页手写一套结构（改版时要改 N 处）；Links 藏在文末；侧栏内容与正文重复。

## 10. 预加载器（Preloader）

**何时用**：品牌开场提示；与导航防抖窗口（700ms，见 08 文档）同量级。

**要点**：
```js
/* 720ms 编排式进度（ease-out cubic）——节奏提示，不是真实资源计量 */
const dur = 720, t0 = performance.now();
(function tick(t){
  const k = Math.min(1,(t-t0)/dur), e = 1-Math.pow(1-k,3);
  if(pct) pct.textContent = Math.round(e*100)+'%';
  if(bar) bar.style.transform = `scaleX(${e})`;
  if(k<1) requestAnimationFrame(tick);
  else setTimeout(() => { el.classList.add('done'); onDone(); setTimeout(() => el.remove(), 260); }, 100);
})(t0);
```
- 字标 + 细进度线 + 百分比计数；完成淡出后**自我移除**（不留 display:none 死节点）；
- `onDone()` 触发 Hero 姓名解码——预载结束 = 首屏动画开始，形成编排感；
- RM（减弱动效）时**直接 remove() 不播动画**；
- 只做一次，不进 sessionStorage 重播。

**反面**：真实资源加载进度条（静态站本来就近乎瞬时，进度条是表演）；永不清除的遮罩。

## 11. Contact 区模式

**何时用**：全站收尾的联系区块。

**要点**：
- **mailto: 邮箱为主 CTA**（大字号、hover 变强调色）——跨设备最可靠的动作，没有之一；
- 按钮行次之：CV（外链，**按语言切地址**——海外网盘 vs 内地镜像，走字典 href 键）+ LinkedIn 等社交链接；
- 第三方可嵌入物（电子名片等）用 iframe `loading="lazy"` + `title`（i18n）；
- **必须有降级路径**：`card not loading?` 外链兜底——iframe 被平台策略拦截或加载失败时，用户仍有点击出口；
- 背景可用低密度装饰场（对角疏密），保持收尾区的安静。

**反面**：只放表单（静态站无后端、垃圾提交无从过滤）；嵌入式内容无降级链接；联系方式散落在多个区块。

## 12. 嵌入名片 / 第三方卡片（iframe）

**何时用**：Contact 区嵌入电子名片、第三方卡片式页面。

**要点**：
```html
<div class="card-frame">
  <iframe id="cardIframe" src="https://overseas.example/card"
          title="Digital card" data-i18n-title="cardTitle" loading="lazy"></iframe>
</div>
<a class="cf-fallback" id="cardFallback" href="https://overseas.example/card"
   target="_blank" rel="noopener" data-i18n="cfFallback">Card not loading? Open it directly ↗</a>
```
```css
.card-frame{
  border:1px solid var(--ink);background:var(--card);
  aspect-ratio:9/16;                          /* 9:16 竖屏 = 卡片类嵌入的黄金比例 */
  width:min(100%,380px);margin-inline:auto;   /* 移动端：宽度驱动 */
  position:relative;overflow:hidden;
}
.card-frame iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
@media (min-width:1024px){
  /* 桌面端：改高度驱动——左列文案高度随语言不同，
     若宽度驱动会三语卡片高矮不齐；高度驱动保证卡片形状一致 */
  .card-frame{width:auto;height:clamp(520px,68vh,680px)}
}
```
```js
/* 源按语言切换：cardSrc / cardTitle / cardHref 三键进字典，
   setLang 时 iframe 源 + title + 兜底链接三同步 */
const iframe = document.getElementById('cardIframe');
if(iframe){ iframe.src = T.cardSrc; iframe.title = T.cardTitle; }
const fb = document.getElementById('cardFallback');
if(fb){ fb.href = T.cardHref; }
```
- **源按区域配双源**：海外/繁中 → 境外名片平台；简中 → 内地可达的名片平台（与视频双链路同理，见 `03-media-compat.md`）；
- **兜底链接常驻**：第三方嵌入随时可能被拦或挂掉，iframe 下方留一条文字出口（「名片加载不出来？直接打开 ↗」，文案进字典三语）；
- `loading="lazy"` + i18n `title`；
- 名片类轻量嵌入**不需要**「点击加载」按钮——折叠方案容易过度设计；该保留给重型 deck。

**反面**：宽度 + 高度双固定（多语言/多设备下卡片变形）；只换外链不换 iframe 源（简中用户仍打境外源）；无兜底链接。

## 13. Colophon 页模式（「这个网站咋做的」）

**何时用**：展示型站点都值得有——把书面设计规范与迭代日志公开化，让访客看到工艺。

**六节结构**：
```
01 Concept          概念与风格来源（引用唯一书面 Style Spec）
02 Tokens           色板（交互式）
03 Typography       字体标本行（交互式）
04 Motion           动效系统总述
05 Stack & Delivery 架构与交付（翻转卡）
06 Iteration Log    迭代日志（一轮一行）
```

**招牌交互组件**：
- **Strata 色板**：颜色竖排成「地质剖面」（基底白 → 深墨，强调色作斜插「矿脉」）；点击任一层复制 hex，该层显示 `COPIED ✓`，~900ms 后自动复位；
- **字体标本行**：每角色（display/body/mono）一行，hover 改字距/字重/颜色——「感受字体」胜过用文字描述规格；
- **fx 自演示词库**：Motion 节里每个术语演示自己命名的效果——wipe 自己给自己擦背景、count 自己计数、cursor 自己变箭头、parallax 自己漂移——术语表即演示，动效系统最有说服力的呈现方式；
- **Spec 翻转卡**：front = 术语标签，back = 详情文案；周期翻转（随机 9–16s，负延迟错峰起步）+ 点击手动翻；back 背景用强调色 ~82% 不透明度（降刺眼）；RM 静态；
- **Iteration Log**：轮号 + 日期 + 一句主题 + 条数徽标，hover 位移 + 编号变强调色；主题按「演进方向」措辞，不翻已推翻项。

**工程纪律**：
- **内容必须与实际实现同步**——站内退役的动效（页面转场、悬浮头像等）要从 colophon 描述里删掉，否则说明书与产品漂移；每次做减法轮，顺手做一次「colophon 同步」；
- 三语与详情页同机制（字典 + setLang）；
- 轮数 / 决策条数 / 版本标识三处联动更新。

**反面**：colophon 过时（描述已退役的效果）；全文字无交互；迭代日志写成流水账日记。

## 14. 其他小组件（速查）

| 组件 | 要点 |
|---|---|
| 灯箱 Lightbox | 点击图片放大；Esc/点击关闭；锁 body 滚动 |
| 章节标题视差 | 标题随滚动 ±14px 反向位移，rAF 节流 |
| 逐行遮罩 reveal | 长导语按渲染行拆 span 上滑；**字体加载完成后必须重排一次**（否则换行错乱出孤儿行）；次级段落不拆行 |
| 自定义光标 | 仅精确指针设备；10px 蓝点 lerp 跟随，hover 可交互目标放大并显示 `data-cursor` 标签 |
| 磁性按钮 | hover 时向指针偏移 ≤7px，离开弹回 |
| 滚动进度条 | 顶部 2px `scaleX`；passive scroll 监听 |
| 数字计数 | 进入视口触发，ease-out 1.2s，IntersectionObserver 一次性 |
| 页脚 | 两行结构：链接行（制作说明 + 回顶部）+ 居中版权行；链接**不带下划线**；字号分级（主链 11px / 版权 9.5px） |
