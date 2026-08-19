# 11 · 上线前总检单（一页汇总）

> 汇总 04/07/08/09/10 五篇的 checklist 与硬约束，**收尾时只读这一页**；逐项展开看各源文档。
> 跑完 `tools/audit.sh`（内容一致性六项）再做本页人工部分，效率最高。

## A. 硬约束（违反 = 事故，逐条过）

| 项 | 约束 | 源 |
|---|---|---|
| 托管单文件上限 | CF Pages 25 MiB；大媒体放对象存储直链 | 04 |
| CSS/JS 缓存 | 改内容必 bump `?v=YYYYMMDD`；全站同名资源版本一致（audit.sh 自动查） | 04 |
| 字体 | 全部自托管 woff2；零外部字体 CDN | 04/09 |
| 大媒体直链 | `raw=1`（流式）非 `dl=0`（下载页）；服务端支持 Range | 03 |
| 可内嵌页面 | iframe 必须带 `?embed` | 03 |
| 音频 | 本地 MP3；`preload="metadata"`；BGM `preload="none"` 且点击才创建 | 03/09 |
| 语言切换 | 动画只做标题类（锁宽解码）；正文瞬时；无全页过渡 | 05/08 |
| localStorage / 事件名 | key `site-lang`、事件 `site:lang` 全站统一 | 05 |
| logo | 语言中立字标，不挂各语言小字 | 05 |

## B. 内容一致性（audit.sh + 人工）

- [ ] `INDEX ×N`、分类计数、「查看全部 N 件」三语文案 == 实际卡数
- [ ] HIGHLIGHT 徽标数 == 首页精选卡数；徽标三语随语言同步
- [ ] 详情页互链列表包含全部详情页；sitemap 覆盖全部可收录页
- [ ] 增删作品走完了 `10-content-ops.md` 的同步清单

## C. 无障碍与动效（08）

- [ ] Tab 全程可走：skip 链接 → 焦点顺序合理 → 无焦点黑洞
- [ ] 焦点环统一（`:focus-visible`）；图标按钮有 i18n `aria-label`
- [ ] 装饰层 `aria-hidden`；iframe 有 i18n `title`；marquee 有 sr-only 镜像
- [ ] landmarks 齐备（header/nav/main/footer）；视频有字幕、音频作品有 transcript
- [ ] 屏幕阅读器抽测一页（NVDA / VoiceOver）+ 200% 缩放不散架
- [ ] 系统开启「减弱动态效果」逐页过：解码直出、磁贴静止、marquee 可手动滚
- [ ] 转场 700ms 防抖生效；语言连点 1000ms 节流生效
- [ ] 触屏设备：图片非灰、无光标残留、拖拽区可原生滚动

## D. 性能（09）

- [ ] 字体走了「子集 → 分片」管线；新文案后管线已重跑（肉眼对比字重防缺字）
- [ ] EN 页 Network 面板：零 CJK 字体分片请求
- [ ] 首屏图无 `loading="lazy"`；首屏以下全 lazy；iframe lazy 或点击加载
- [ ] BGM 未点击时零音频请求
- [ ] 跨域媒体源有 preconnect（≤3）；首屏 LCP 图带 `fetchpriority="high"`
- [ ] Lighthouse 移动档 Performance ≥ 90 / Accessibility ≥ 95
- [ ] （上线后）Search Console CWV 报告无 Poor 页面（LCP ≤2.5s / INP ≤200ms / CLS ≤0.1）

## E. 部署与跨地域（04）

- [ ] `_headers` 在产物根目录；`curl -I` 验证安全头
- [ ] robots.txt（禁 404、指 sitemap 绝对 URL）+ sitemap 全 URL 可达
- [ ] og:image 绝对 URL；微信/Telegram/X 实测分享卡片
- [ ] JSON-LD 过 Rich Results Test；canonical 指裸 URL；存档页 noindex
- [ ] 404.html 就位、文案语义化、返回按钮带语言参数
- [ ] 自定义域名解析 + HTTPS；裸域/www 单一规范域
- [ ] 部署目录完整（直传 = 全量快照，勿只传改动文件）
- [ ] ITDOG（https://www.itdog.cn/http/ ）多地抽样全绿（海外+内地）
- [ ] 两地实测：海外直连 + 内地无梯子网络各过一遍全站（含每个媒体链接）

## F. 收尾（06/07）

- [ ] 控制台零报错；三语切换正常（含 href/iframe 源/渠道文案三层同步）
- [ ] `wc -c` 抽查核心 HTML 体量（>150KB 警惕、>300KB 查污染；口径见 09 性能节，audit.sh 第 5 项自动查）
- [ ] 轮次日志全部条目标状态；结论性变更已同步进站根活档与 colophon
- [ ] 线上（非本地）抽测至少一页
