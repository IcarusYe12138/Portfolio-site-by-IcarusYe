# 03 · 音视频与图文（Web·Article）的跨地域兼容 ★专节

> 目标：一套站点，海外与中国内地用户**都能正常播放/阅读全部作品**。
> 核心思路：**自托管 + 双链路（海外直链 + 内地镜像/本地存档）**，用少量内置逻辑（data-langs、?embed、preload、raw=1）换取跨地域鲁棒性。

## 一、视频如何兼容（国际 + 内地双链路）

### 海外链路：`<video>` + 直链
```html
<video controls preload="metadata" poster="assets/works/xxx-poster.webp">
  <source src="https://<境外网盘>/file.mp4?rlkey=xxx&raw=1" type="video/mp4">
</video>
```
- 关键参数：**`raw=1`**（境外网盘通用约定）把「下载页」变成「可流式直链」；`dl=0` 是下载页地址，`<video>` 吃不到流；
- 直链托管方必须支持 **HTTP Range**（拖进度条、码率自适应的前提）；主流云存储/网盘 raw 链接都支持；
- `preload="metadata"` 只拉时长不拉全片；
- poster 用本地 webp，避免播放前黑屏。

### 内地链路：整块媒体源切换（不是只换文字）
同一视频在内地换**可内嵌的国内平台 iframe**：
```html
<!-- 海外版块 -->
<div class="block" data-langs="en tw">
  <video controls preload="metadata" poster="…">…</video>
  <a class="btn" href="https://<境外网盘>/file.mp4?rlkey=xxx&dl=0">Watch on <网盘></a>
</div>
<!-- 内地版块：同一作品，另一套媒体源 -->
<div class="block" data-langs="zh">
  <iframe src="https://<国内平台>/design/xxx/watch?embed" loading="lazy" allowfullscreen></iframe>
  <a class="btn" href="https://<国内平台>/design/xxx/watch">国内平台观看（内地可达）</a>
</div>
```
- `data-langs="en tw"` / `data-langs="zh"` 控制语言版块显隐——**把整块媒体源连同容器一起切换**，语言切换时视频/iframe 整体替换，绝不只换标题文字；
- 常见配对：境外网盘 MP4 直链 ↔ 国内在线设计平台/视频平台的 watch 页 iframe；
- **iframe 必须加 `?embed`**（平台约定）：裸 `/watch` URL 会被响应头（X-Frame-Options / CSP frame-ancestors）拒绝嵌入，控制台报 `ERR_BLOCKED_BY_RESPONSE`；`/watch?embed` 或 `/view?embed` 才可嵌入。

### 可内嵌 deck / 在线页面
- 同理用 iframe + `?embed`；
- 大而重的嵌入可做**点击加载**：先放一个「Load embed」按钮，点击后才注入 iframe（省首屏性能）：
```js
btn.addEventListener('click', () => {
  shell.innerHTML = `<iframe src="${btn.dataset.embed}" loading="lazy" allowfullscreen></iframe>`;
});
```

## 二、音频如何弄

- **全部本地 MP3 自托管**（放 `assets/audio/`），禁外部音频 CDN——内地可达 + 无跨域麻烦；
- 作品音频用**内嵌播放器**组件（播放/暂停 + 拖动 seek + 时间 + 下载 ↓），见 `../templates/audio-player.html`；三语可共用同一本地 MP3；
- 背景音乐用**独立单例**（默认不播、点击才播、循环、音量 ~70%、`preload='none'`），见 `../templates/bgm.html`；
- `preload="metadata"`（要显示时长）/ `"none"`（BGM，完全不预载）/ 慎用 `"auto"`；
- 注意托管平台单文件上限（如 25 MiB）：MP3 一般安全，长音频/视频一律放对象存储。

## 三、网页（Web·Article）如何搞 —— 本地 HTML 存档

对内地访问不了的外链文章（个人博客、媒体作品页），做「本地 HTML 存档」：

### 类型 A：CMS/博客整页（WordPress 类）
- 「另存为完整网页」后把 **CSS、字体、正文图片全部落本地**（修正所有引用路径为相对路径）；
- 删掉统计脚本、第三方跟踪、外链 JS；
- 存 `archive/<slug>/index.html`，从作品卡 `data-href-zh` 链过去，链接文案标注「本地存档」。

### 类型 B：高度 JS 驱动的交互故事（滚动叙事平台类）
- 整页存档不可行（JS 依赖运行时）——只把**图片/视频落本地**，正文重排为静态结构；
- 第三方数据可视化 iframe（图表平台）**保留外链**（无法本地化，内地用户看图表可能缺，可接受）；
- 优先保证「图文完整可读」，牺牲部分交互。

### 原则
- 存档页只是**fallback**：海外/繁中版本仍链原站（SEO 与原作者页面尊重），仅简中版链本地存档；
- 存档属于个人作品留存用途；如涉版权敏感内容不做存档。

## 四、限制（必须写清楚，否则必返工）

| 限制 | 说明 |
|---|---|
| 托管平台单文件上限 | 如 Cloudflare Pages 25 MiB → PDF/视频/长音频放对象存储，页面层直链 |
| 下载页 ≠ 直链 | 网盘「分享页 URL」和「raw 直链」是两回事，`<video>/<audio>` 只认直链 |
| 海外域名 ≠ 内地域名 | 同一产品两个域名（如某设计平台国际版/国内版）可嵌性与可达性都不同，分别配置 |
| 签名 URL 会过期 | 带签名参数的对象存储临时链接有 TTL，生产环境用长期有效配置或自定义域名 |
| 第三方可视化 iframe 无法本地化 | 只能外链，接受地域差异 |
| 本地开发服务器无 Range 支持 | 音视频 seek 报错/控制台 ERR_ABORTED 可能是本地环境问题，非代码 bug（见 07 坑 #7） |
| 平台内嵌政策随时变 | 上线前两地各实测一遍 |

## 五、为什么这么做更适用（设计依据）

1. **自托管 + 本地存档**去掉对境外 CDN/字体/媒体的强依赖 → 内地稳定可达；
2. **双链路**（海外直链 + 内地镜像）保证两边用户都能正常播放——不需要维护两套站点，只是每条外链配两个地址；
3. **少量内置逻辑**（`data-langs` 版块切换、`?embed`、`raw=1`、`preload` 控制）换来跨地域鲁棒性，维护成本极低；
4. 媒体「就近原则」：小而关键的（字体、海报、MP3、OG 图）本地；大而重的（长视频、PDF）对象存储直链；平台强绑定的（在线 deck）双平台 iframe。

## 六、落地清单（新站接媒体时逐项过）

- [ ] 每个视频：海外直链（`raw=1` + poster）+ 内地可嵌 iframe（`?embed`）两套？
- [ ] 每个 deck/在线页：`?embed` 可嵌？是否点击加载？
- [ ] 每条音频：本地 MP3？内嵌播放器？`preload` 设置？
- [ ] 每篇外链文章：内地能开吗？不能 → 本地存档（A/B 型选一）？
- [ ] 每个外链卡：`data-href-en` / `data-href-zh` 双地址 + 语言切换换 href 逻辑？
- [ ] 单文件全部 < 25 MiB？
- [ ] 上线后两地（无梯子环境）实测每个媒体链接？
