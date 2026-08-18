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

## 9. 其他小组件（速查）

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
