# 08 · 无障碍与动效安全

> 原则：**移除的是「动」，保留的是「状态」**。任何动效降级后，内容必须完整可见、功能必须完整可用。
> 无障碍不是附加项——键盘可达、屏幕阅读器语义、光敏保护从第一行代码就写进去， retrofit 成本极高。

## 一、键盘可达性

### Skip 跳转链接
页面第一个可聚焦元素，跳过导航直达主内容：

```html
<a class="skip" href="#works">Skip to works</a>
```
```css
.skip{
  position:fixed;top:-64px;left:16px;z-index:1200;   /* 平时收在视口外 */
  background:var(--ink);color:#fff;padding:10px 16px;
  transition:top var(--t);
}
.skip:focus{top:12px}                                 /* Tab 聚焦时滑入 */
```
- 纯 CSS 实现，无需 JS；`href="#主内容锚点"`；
- 字典加 key，三语可用。

### 焦点环规范
全站统一一条规则，不用 `outline:none` 裸奔：
```css
:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
```
- 用 `:focus-visible` 而非 `:focus`——鼠标点击不显环、键盘 Tab 才显，两全；
- 焦点环用强调色 = 「行动信号」原则的自然延伸。

### 键盘操作覆盖面
- **全部可交互元素用原生 `<a>` / `<button>`**——自带键盘语义，别用 `<div onclick>`；
- 灯箱：`Esc` 关闭 + 点击遮罩关闭，关闭后焦点回到触发元素；
- 拖拽组件（seek 轨道、marquee）本质是 pointer 交互，**必须同时提供等价的非拖拽路径**（seek 支持单击定位；marquee 内容不是唯一信息源）；
- 弹层打开时锁 `body{overflow:hidden}`，关闭即恢复。

## 二、ARIA 模式速查

| 场景 | 写法 | 说明 |
|---|---|---|
| 语言切换组 | `role="group" aria-label="Language"`；激活项 `aria-current="true"` | 屏幕阅读器播报「当前语言」 |
| 开关型按钮（BGM） | `aria-pressed="false/true"` + 描述性 `aria-label` | 状态随播放切换 |
| 图标按钮（播放/下载） | `aria-label` 经 `data-i18n-aria` 随语言切换 | 无文字的按钮必须有可读名 |
| 当前案例（互链列表） | `aria-current="page"` | 与语言切换的 aria-current 同一语义 |
| 纯装饰层 | `aria-hidden="true"` | 磁贴场、自定义光标、进度条、滚动条装饰点全部标 |
| 事实侧栏 | `aria-label="Project facts"` | aside 需要可读名 |
| iframe | `title` 属性必填 | 播报器读 title 识别嵌入内容 |
| 图片 | `alt` 描述内容而非「图片」二字 | 装饰图 `alt=""` + aria-hidden |

**判断法**：写完每页，用 Tab 走一遍——焦点顺序 = 视觉顺序 = 语义顺序，三者不一致就是 bug。

## 三、prefers-reduced-motion 全站策略

### JS 侧：模块顶部一次性判定
```js
const RM = matchMedia('(prefers-reduced-motion: reduce)').matches;
const HOVER = matchMedia('(hover:hover)').matches;
```
所有动效模块读同一对常量，禁止各模块重复查询。

### 分支表（逐组件的 RM 行为）

| 组件 | RM 行为 | 状态保留 |
|---|---|---|
| 预加载器 | 立即 `remove()` | 照常触发标题解码（直出） |
| 文字解码 scramble | 直接 `el.textContent = final_` | 文本完整呈现 |
| 磁贴场 | 静态网格，不加 flip 磁贴 | 底纹仍在 |
| Marquee | 不启动 rAF 自动滚 | 车道保持可手动滚动（overflow 容器天然支持） |
| 数字计数 | 时长压到 ~60ms（近瞬时） | 终值照常显示 |
| 筛选错落动画 | 跳过 f-pre/f-run 类 | 卡片直接 display 切换 |
| 自定义光标 / 磁性按钮 | `if(RM \|\| !HOVER) return;` 整个模块跳过 | 原生光标 + 普通按钮 |
| 灯箱 / 视差 | 视差跳过 | 灯箱保留（功能性） |

### CSS 侧：两种做法
**A. 逐组件覆盖**（站点实际做法，更精细）：
```css
@media (prefers-reduced-motion:reduce){
  .tile.flip{animation:none}
  #langVeil{display:none}
  .sp-flip{transition:none}
}
```
**B. 全局一揽子**（省心，适合组件多的站）：
```css
@media (prefers-reduced-motion:reduce){
  *,*::before,*::after{
    animation-duration:.01ms!important;
    animation-iteration-count:1!important;
    transition-duration:.01ms!important;
    scroll-behavior:auto!important;
  }
}
```
两法取一即可；混用时全局块会压过逐组件块，注意顺序。

## 四、光敏保护：转场节流

快速连续的全屏转场是光敏性癫痫的已知诱因。两个节流阀：

### 导航防抖（700ms）
```js
let navAt = 0;
function navGate(e){
  if(e.__navOK) return true;
  if(performance.now() - navAt < 700) return false;   // 两次转场至少间隔 700ms
  navAt = performance.now(); e.__navOK = true; return true;
}
```
- 两次页面转场至少间隔 700ms，第二次点击直接吞掉；
- 预加载器固定 720ms 编排（节奏提示，非真实加载进度）——与防抖窗口同量级，观感一致。

### 语言切换节流（1000ms）
```js
if(n - langAt < 1000) return;   // 一次只跑一轮解码动画
```
- 解码动画跑一半被打断会闪乱码——同一时刻只允许一轮；
- 语言按钮是全站最容易被连点的控件，必须有此保护。

### 常规动效纪律
- 过渡 ≤250ms、ease-out 曲线；无弹性、无弹跳、无无限循环的**内容性**动画；
- 装饰性无限循环（磁贴翻转、marquee）允许，但必须：① 缓慢（≥7s 周期）；② 可被 RM 关闭；③ 不承载信息。

### 先例：语言切换动画的否决史（真实五步）

语言切换是多语言站触发最频繁的操作之一，其动画极易过度设计。一次真实的五步迭代：

1. **宽度抖动 scramble（初版）**：随机字符宽度不一，每切一次布局抖一次 → 否；
2. **全页扫描线 / 磁贴矩阵**：对高频动作而言仪式感过重 → 否；
3. **字符滚轮**：本质上仍是高频动作上的花样 → 否；
4. **全效果移除（瞬时切换）**：干净了，但标题缺一点「交接感」；
5. **终版锁宽解码**：仅标题类元素跑随机字符收敛（冻结高度 + overflow:hidden 防重排），正文瞬时切换。

结论：**高频动作上的动画只允许做在标题类元素；正文永远瞬时；任何全页层面的过渡都是过度设计。** 新方案提语言切换动效前，先对照这份先例。

## 五、触屏与精确指针分治（ Recap ）

凡 hover 特效一律门控（详见 `02-components.md`）：
```css
@media (hover:hover) and (pointer:fine){ /* 灰度滤镜、放大等 */ }
```
- 触屏默认看到**完整状态**（彩色图、全部信息）；
- 自定义光标、磁性按钮在 `(hover:none)` 设备整模块跳过；
- 触屏滚动交互走原生（overflow 容器），不自己造轮子。

## 六、对比度底线

- 正文 ink on 白底；辅助文字不低于 ink50；
- 强调色底上的文字用纯白（`#2F2FE4` 类深饱和色可达标；浅强调色需验证 4.5:1）；
- 用 1px 发丝线分隔区域时，确保分隔线不只是**唯一**的语义标识（辅以间距/编号）。

## 七、上线前自查清单

- [ ] Tab 从头走到尾：skip 链接出现 → 焦点顺序合理 → 无焦点黑洞
- [ ] 焦点环全站统一且可见（`:focus-visible`）
- [ ] 所有图标按钮/开关有 aria-label 或 aria-pressed，且随语言切换
- [ ] 装饰层全部 aria-hidden；iframe 全部有 title；img alt 语义正确
- [ ] 系统开启「减弱动态效果」逐页过：解码直出、磁贴静止、marquee 可手动滚、计数瞬时
- [ ] 转场连点不闪屏（700ms 防抖生效）
- [ ] 语言连点不乱码（1000ms 节流生效）
- [ ] 触屏设备：图片非灰、无自定义光标残留、拖拽区可原生滚动
