# 10 · 内容运维：作品增删改的同步清单

> 灾区重灾区：作品增删之后，站内**计数与引用到处都是**，漏改一处就是数据不一致 bug（标题写 ×17、实际 18 张卡；分类计 5 个实际 6 个……）。
> 本文档把「动一件作品」拆成一张固定的同步点清单，照单执行。优先做成 **JS 从 DOM 自动计数**，能自动的绝不手写。

## 一、为什么容易翻车

一处作品的引用散布在 7~9 个位置：索引页卡片网格、索引页头部计数（`INDEX ×N`）、分类筛选计数、首页作品区 meta、首页「查看全部 N 件」按钮文案（×3 语字典）、HIGHLIGHT 徽标体系、精选轨（首页横滚）、详情页互链列表、sitemap。任何一处遗漏都不报错——只在用户眼里露馅。

## 二、新增一件作品（Checklist）

- [ ] **1. 索引页卡片网格**：插入卡片（编号角标、海报图、标题/分类 i18n key ×3 语、`data-cat`、外链卡补 `data-href-en` / `data-href-zh` + `target="_blank" rel="noopener"`）
- [ ] **2. 编号重排**：若插在中间，其后所有卡片编号角标 +1；编号必须连续无跳号
- [ ] **3. 索引页头部计数**：`INDEX ×N` 标题、分类 meta 行（`FILM ×6 / AUDIO ×3 / …`），三语字典同步
- [ ] **4. 分类筛选计数**：若计数是 JS 从 `data-cat` 自动算的（推荐做法）——跳过；若是硬编码 `<sup>N</sup>`——手改并全语言检查
- [ ] **5. 首页作品区 meta**：`worksMeta`（`HIGHLIGHT ×N · FULL INDEX ×N`）三语同步
- [ ] **6. 首页按钮文案**：「查看全部 N 件作品」在 en/zh/tw 三份字典里各有一份，全改
- [ ] **7. 若是精选作品**：首页精选轨加卡（顺序即叙事顺序，需用户确认）；索引页卡片加 HIGHLIGHT 徽标（三语文案）；徽标数量与首页精选数一致
- [ ] **8. 若建详情页**：`works/<slug>.html` 按 `templates/case-page.html` 骨架；**详情页互链列表的 CASES 数组**（或集中配置）加一条 + 三语名称；相邻详情页的「下一项目」链接链到新页
- [ ] **9. sitemap.xml**：新页面加 `<url>` 条目
- [ ] **10. 海报/缩略图**：webp 落 `assets/works/`，卡图与详情页 hero 共用一张即可；无图时用现有占位图，**不为此生成新图**

## 三、删除一件作品（反向 Checklist）

- [ ] 卡片 + 字典 key（t*/c* ×3 语）四处同步删（HTML 节点 / CSS 无残留 / JS 逻辑 / 字典）
- [ ] 编号重排补跳号；计数全部 -1（同上 3~6 点）
- [ ] 若是精选：精选轨撤卡、徽标撤、首页 worksMeta 的 `HIGHLIGHT ×N` 同步
- [ ] 详情页互链列表移除；若有详情页文件本身——删除或保留但移出导航（保留时加 noindex）
- [ ] 检查悬空引用：全站 grep 作品 slug，`sitemap`、`next-proj`、跨页链接清零

## 四、合并多个条目为一（常见模式）

多个子作品（如同一品牌的多个物料）合并为一张主卡时：
- 子条目全部按「删除」流程走；
- 主卡链到合并后的详情页，详情页内部用编号小节分列各子物料；
- 计数按「合并后 1 件」计，字典文案说明「全案」性质。

## 五、计数自动化（强烈推荐）

能从 DOM 算的计数不要写死。索引页筛选条的正确姿势：

```js
const cells = [...document.querySelectorAll('.cell')];
const counts = {ALL: cells.length};
cells.forEach(c => counts[c.dataset.cat] = (counts[c.dataset.cat] || 0) + 1);
/* 按钮渲染 `${label}<sup>${counts[cat]}</sup>` */
```

头部 `INDEX ×N` 与分类 meta 行也可以由 JS 生成（数据源 = 一个 WORKS 数组或直接数卡片），手写文案只留占位。**手写计数是事故之源**——每处手写的 N 都是未来的一个 bug。

## 六、增删后的一致性审计（5 分钟例行）

```bash
# 卡片实际数量 vs 头部宣称
grep -c 'class="cell"' works.html          # 实际卡数
grep -o 'INDEX ×[0-9]*' works.html          # 宣称数 —— 两边必须相等

# 分类实际 vs 宣称
grep -c 'data-cat="FILM"' works.html        # 每个分类都过一遍

# 首页按钮文案（三语字典里的 N）
grep -o 'View All [0-9]* Works' index.html
grep -o '查看全部 [0-9]* 件作品' index.html

# HIGHLIGHT 徽标数 vs 首页精选卡数
grep -c 'cell-hl' works.html
grep -c 'hl-card' index.html
```

任何一处对不上 → 回到对应 checklist 项修复。

## 七、内容源的唯一事实源

- 作品清单以用户维护的**载体**（飞书多维表格 / Markdown / Excel，见 `00-onboarding.md`）为准；
- 站点每次增删作品，先在载体里改，再照本清单同步站点——载体是账本，站点是投影；
- 大版本内容变动后，在迭代日志里记一条（`06-iteration.md`），注明「作品 N→M」。

## 八、周期性内容审计（上线后，防 link rot）

增删改是「动一次查一次」；上线后还有三类**按日历轮转**的审计——作品集外链多（网盘 / 平台 / 云文档），链接烂掉是时间问题，烂了还挂在首页就是硬伤。

### Link rot 检查工具

| 工具 | 类型 | 用途 |
|---|---|---|
| **[lychee](https://github.com/lycheeverse/lychee)**（Rust） | CLI | 支持整站 HTML/Markdown 批量、限速、重试——本地跑全站外链首选 |
| **[muffet](https://github.com/raviqqe/muffet)**（Go） | CLI | 并发快，适合 CI / 脚本化周期跑 |
| broken-link-checker（npm） | CLI | Node 生态，可递归爬渲染后页面 |
| [Dead Link Checker](https://www.deadlinkchecker.com/) 等 | 在线 | 不想装 CLI 时的轻量替代 |

```bash
# lychee 全站外链体检（跳过本地锚点，只查 http）
lychee --no-progress '*.html' 'works/*.html'
```

### 审计节奏

| 周期 | 动作 |
|---|---|
| **每次发布前** | `tools/audit.sh`（计数/版本号一致性六项） |
| **每月** | link checker 全站外链一遍；[ITDOG](https://www.itdog.cn/http/) 抽测主域名两地可达性 |
| **每季度** | 内容时效性复审：作品介绍里的「近期」「去年」类表述、署名/合作方链接是否变更、下架作品是否还挂着外链 |
| **有真实流量后** | Search Console 看 404 命中与 CWV 报告（见 `04-deploy-and-domain.md` 九） |

### 签名 URL 的 TTL 监控

对象存储**带签名的临时直链有过期时间**（07 坑 #9 的根源）。若站内用了签名 URL：
- 优先改用**公开读的桶 + 防盗链**，从根上消掉过期问题；
- 必须签名时（私有桶），把过期窗口设长（如 1 年）并在内容载体里记录**每个签名链接的到期日**，到期前一个月续签——月度 link rot 检查会顺带抓到已失效的（403），这就是兜底。
