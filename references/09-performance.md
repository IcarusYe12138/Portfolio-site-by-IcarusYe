# 09 · 性能手册

> 载荷思维：**页面层轻、媒体层外置、按需拉取**。字体是静态站最大的可控载荷，中文站尤甚——本手册的核心是「先子集、再分片」管线。

## 一、载荷分层

| 层 | 放什么 | 目标 |
|---|---|---|
| 页面层（直传托管） | HTML / CSS / JS / 字体分片 / 海报 webp / MP3 / og 图 | 单页初次载荷 < 1MB（不含懒加载媒体） |
| 对象存储直链 | 长视频、PDF、大文件 | 25 MiB 单文件上限绕开；按需流式 |
| 平台 iframe | 在线 deck / 协作页 | 点击加载或 loading=lazy |

HTML 本身也要「瘦」。**体量阈值（站点统一口径，用 `wc -c` 看字节）**：
- 单页正常 **50–100KB** 级；
- **>150KB** 警惕（查滚动轨道/重复节点）；
- **>300KB** 基本是污染（DOM 快照等，→ `07-pitfalls.md` 坑 #3）。

自动化检查在 `tools/audit.sh` 第 5 项（150KB WARN / 300KB FAIL）；其他文档涉及的体量标准以此为准。

## 二、字体：自托管 + 子集 + 分片（核心大项）

### 为什么
- 全字库中文字体 **~9MB/字重**，直接 @font-face 不可接受；
- **全字库分片也不行**：站内用字分散，每字命中自己的分片，请求数与总流量反升；
- 正确路线 = **先按「站内实际字符集」子集化、再分片**。

### 管线（一条命令可复现）
> **三个脚本的通用版随本 kit 提供**：`tools/collect_chars.py` → `tools/subset_fonts.py` → `tools/split_cjk.js`（依赖、配置与三坑备忘见 `tools/README.md`；拷到你的站点 tools/ 目录，改 JOBS 配置即可用）。

```bash
# ① 收集全站实际用字 → 字符清单
python3 tools/collect_chars.py /path/to/site   # 产出 cjk-set.txt（约 1–2 千字）

# ② 按字符集子集化（pyftsubset，产中间 OTF；先改脚本头部 JOBS 为你的字体）
python3 tools/subset_fonts.py                  # desubroutinize=True，防下游子集器卡死

# ③ 分片 + 自动生成 CSS
node tools/split_cjk.js                        # 产出 assets/fonts/split/** + assets/css/cjk.css
```

### 机制：unicode-range 按需拉取
生成的 `cjk.css` 每个 @font-face 声明 `unicode-range`：
```css
@font-face{
  font-family:'CJK-SC';
  src:url("../fonts/split/sc-45/xxxx.woff2") format("woff2");
  font-weight:300;font-display:swap;
  unicode-range:U+4E00,U+4E0A,U+4E0D, …;   /* 本片负责的码位 */
}
```
浏览器渲染时计算页面实际出现的码位 → **只拉命中的分片**：
- EN 页面：零 CJK 请求（虽然也挂着 cjk.css）；
- zh 页面：典型 ~50 片 / ~746KB；
- 全站 6 字重 × 24 片 ≈ 144 片共 ~2.3MB，任何单页只取子集。

### 实测收益基准
| 方案 | zh 首页字体载荷 |
|---|---|
| 全字库 woff2（固定） | ~1.5MB+ |
| 全字库分片（错误路线） | 更差（海量小请求） |
| **先子集再分片（本管线）** | **~50 片 / 746KB** |

### 西文字体
- 体积小，按字重静态 woff2 或单文件可变字体均可；
- 全部 `font-display:swap`（先用系统栈渲染，字体到了再换，永不白屏）；
- 字体栈末尾给系统中文回退（PingFang 等），分片未命中时兜底。

### 纪律与坑
- **新增文案含未收录字 → 该字静默回退系统字体**（不报错）。上线新内容前重跑管线，肉眼对比字重；
- 工具坑（woff2 输入 / chunkSize 死循环 / src:local 正则）详见 `07-pitfalls.md` #10–12；
- 中间产物（OTF）进 .gitignore；`cjk.css` 头部标注「自动生成，勿手改」与再生成命令。

## 三、懒加载与预载矩阵

| 资源 | 策略 |
|---|---|
| 首屏以下图片 | `loading="lazy"`（首屏图**不要** lazy，反而伤 LCP） |
| 视频海报 | 本地 webp `poster`，避免播放前黑屏与额外请求 |
| iframe（deck/平台页） | `loading="lazy"`；重型嵌入用**点击加载**（先放按钮，点击注入 iframe） |
| 作品音频 | `new Audio()` + `preload="metadata"`（只拉时长） |
| 背景音乐 | `preload="none"`，且**首次点击才创建** Audio 实例——未点击零流量 |
| 外链视频 | `<video preload="metadata">` + 直链（raw=1） |

图片处理（webp 批量转换、视频抽 poster 帧、og 图 1200×630 中心裁剪）的 macOS 命令速查见 `tools/README.md` 末节。

点击加载模式（省首屏、用户体验也更好——重型 iframe 不抢带宽）：
```js
btn.addEventListener('click', () => {
  shell.innerHTML = `<iframe src="${btn.dataset.embed}" loading="lazy" allowfullscreen></iframe>`;
});
```

## 四、IntersectionObserver 三种模式

### 模式 1：一次性触发（reveal / 计数）
```js
const io = new IntersectionObserver(es => es.forEach(e => {
  if(e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); }
}), {threshold:.08, rootMargin:'0px 0px -5% 0px'});
```
- 触发即 `unobserve`——不重复、不常驻监听；
- 错落用 `transitionDelay = (i%6)*40` 之类的小周期，别逐元素递增到秒级。

### 模式 2：footer 哨兵（iOS 惯性滚动兜底）
iOS Safari/Chrome 惯性滚动期间 scroll 事件可能停发，导致「滚动隐藏的顶栏到底部不回来」：
```js
const io = new IntersectionObserver(es => {
  if(es[0].isIntersecting) showChrome();     // footer 进视口 → 强制显示 chrome
}, {threshold:0.01});
io.observe(document.querySelector('footer'));
```

### 模式 3：2 秒安全网（reveal 漏触发兜底）
IO 偶发漏报（隐藏 tab、快速滚动）会让元素永远停在 opacity:0：
```js
setTimeout(() => {
  document.querySelectorAll('.rv:not(.in)').forEach(el => {
    const r = el.getBoundingClientRect();
    if(r.top < innerHeight && r.bottom > 0){        // 视口内还没显示的
      el.style.transitionDelay = '0s'; el.classList.add('in');
    }
  });
}, 2000);
```

threshold 经验值：reveal `.08`（早触发）、计数 `.5`（读得见才数）、哨兵 `.01`（贴边即报）。

## 五、滚动与动画性能

### 监听纪律
- 所有 scroll 监听一律 `{passive:true}`（不阻塞滚动线程）；
- 视差类用 rAF ticking 门控，一帧只算一次：
```js
let ticking = false;
addEventListener('scroll', () => {
  if(!ticking){ ticking = true; requestAnimationFrame(update); }
}, {passive:true});
function update(){ ticking = false; /* … */ }
```

### 循环纪律
- Marquee 用**单条 rAF 循环**驱动所有车道，`dt = Math.min(64, now - last)` 钳制——后台标签页回来不会跳帧狂奔；
- 自动滚写 `scrollLeft`，不监听 scroll 事件判 idle（→ 07 坑 #15）。

### 只动 transform / opacity
- 进度条 `scaleX`（非 width）、填充 `transform-origin:left`、磁贴 `rotateY` + `backface-visibility:hidden`；
- 触发布局的属性（width/top/left/margin）一律不进动画。

### will-change 与清理
- 只给确有复合层收益的元素加（翻转磁贴、磁性按钮），不是越多越好；
- **动画结束清场**：筛选动画结束后移除 `transitionDelay`，否则污染后续 hover 过渡；临时类（f-pre/f-run）一并撤掉。

### DOM 批量操作
- 批量插入用 `DocumentFragment`（磁贴场一次 append）；
- 占位判断用 `Uint8Array` 网格（磁贴场 cols×rows），不用对象数组；
- `resize` 重建一律防抖 ~220ms。

## 六、Resource Hints 与图片格式

### Resource Hints 速查

| Hint | 拉什么 | 成本 | 何时用 |
|---|---|---|---|
| `preload` | **当前页**关键资源 | 高（抢占带宽，用错反而拖慢 LCP） | 动态注入的 LCP 资源、CSS 内引用的关键字体 |
| `prefetch` | **未来页**资源 | 低 | 下一页大概率访问的图/字体分片 |
| `preconnect` | 跨域的 DNS + TCP + TLS | 中（占 socket/TLS） | 跨域字体 / 对象存储媒体源——**只给前 3 个关键域** |
| `dns-prefetch` | 仅 DNS 解析 | 几乎免费 | 其余第三方域兜底 |

```html
<!-- 跨域媒体源：preconnect 主力 + dns-prefetch 兜底（老浏览器回落） -->
<link rel="preconnect" href="https://cdn.example" crossorigin>
<link rel="dns-prefetch" href="https://cdn.example">
```

**决策要点**：
- 静态 HTML 里本来就有的 `<img>` / `<script>`——**直接加 `fetchpriority="high"`**，不要再用 preload 包一层（浏览器的 preload scanner 本来就能提前发现它们）；
- preload 用错是最常见的「加了提示反而 LCP 变差」事故——只 preload 当前页确定要用的，其余交给 prefetch；
- 第三方域超过 ~4 个：preconnect 前 3、其余 dns-prefetch，别全 preconnect。

```html
<!-- 首屏 LCP 大图：元素级优先级即可 -->
<img src="hero.webp" fetchpriority="high" alt="…">
```

### 图片格式：webp 为主，AVIF 可选

- **webp**：基线格式，全浏览器支持，海报/卡图批量转换管线见 `tools/README.md`；
- **AVIF**：比 webp 再省 30–50%，Safari 16+ 起完整支持——图片多、流量敏感的站值得上，用 `<picture>` 三级回落：

```html
<picture>
  <source type="image/avif" srcset="hero.avif">
  <source type="image/webp" srcset="hero.webp">
  <img src="hero.jpg" alt="…">          <!-- 最终兜底 -->
</picture>
```

- 个人站的正确顺序：先把所有图转 webp + lazy 矩阵做对，**再**考虑 AVIF 深化——不要跳级。

### Critical CSS：本方法论不强制

静态多页站的 HTML 本身就是「首屏文档」，CSS 单文件 + `?v=` 缓存纪律已够快；Critical CSS 内联（抽首屏样式进 `<style>`）适用于重单页应用，对本套「每页独立 HTML」架构收益小、维护成本高（改样式要同步两处）——**明确不做**，除非 Lighthouse 实测 FCP 不达标再个案处理。

### CWV：实验室数据 vs 字段数据

| | 实验室（Lighthouse） | 字段（CrUX / RUM） |
|---|---|---|
| 来源 | 固定网络/设备模拟 | 真实访客 |
| 用途 | 开发期回归、本地对比 | **Google 排名依据** |
| 看哪 | 每次 Lighthouse 移动档 | Search Console → Core Web Vitals 报告 |

阈值与通过判据（LCP ≤ 2.5s / INP ≤ 200ms / CLS ≤ 0.1，75% 访问达标）见 `04-deploy-and-domain.md` 第九节。上线后有真实流量后，以 Search Console 报告为准复盘。

## 七、上线前性能自查

- [ ] 字体全部自托管；中文走了「子集→分片」管线；新文案后管线已重跑
- [ ] EN 页 DevTools Network：零 CJK 字体分片请求
- [ ] 首屏图片无 `loading="lazy"`；首屏以下图片全 lazy
- [ ] iframe 全 lazy 或点击加载；BGM 未点击时零音频请求
- [ ] Lighthouse（移动档）Performance ≥ 90、Accessibility ≥ 95
- [ ] 跨域媒体源有 preconnect（≤3 个）；首屏 LCP 图带 `fetchpriority="high"`
- [ ] 上线后（有流量时）Search Console CWV 报告无 Poor 页面
- [ ] 长列表页滚动帧率稳定（Performance 面板无长期绿块/红条）
- [ ] HTML 单页体量正常（无快照污染膨胀）
- [ ] CSS/JS 改动已 bump `?v=`（→ `04-deploy-and-domain.md`）
