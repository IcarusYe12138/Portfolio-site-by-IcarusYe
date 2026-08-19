# tools/ —— 构建与审计脚本

字体管线（三步，顺序执行）+ 一致性审计 + 图片处理速查。脚本均为通用版：路径参数化或顶部 JOBS 配置，拷到任何站点目录改两行即可用。

## 字体管线

```
collect_chars.py ──► subset_fonts.py ──► split_cjk.js
  收集站内用字        按字符集子集化       cn-font-split 分片
  → cjk-set.txt      → subset-ttf/*.otf   → assets/fonts/split/** + assets/css/cjk.css
```

```bash
# 0) 依赖
pip install fonttools
npm i cn-font-split        # 在 tools/ 下执行，或全局安装

# 1) 收集你站点的实际用字（输出 cjk-set.txt）
python3 collect_chars.py /path/to/your-site

# 2) 子集化：先把中文原字体（TTF/OTF，不是 woff2）放进 tools/font-src/，
#    改 subset_fonts.py 顶部 JOBS 为你的字体清单，然后：
python3 subset_fonts.py

# 3) 分片：改 split_cjk.js 顶部 SITE 与 JOBS（与上一步一一对应），然后：
node split_cjk.js
#    产物进 <site>/assets/fonts/split/ + cjk.css，页面挂 <link cjk.css> 即用
```

**重跑时机**：站内新增任何中文文案之后（未收录字会静默回退系统字体，不报错——肉眼对比字重是唯一线索）。

### `JOBS` 字段 schema（改脚本顶部前先看）

`subset_fonts.py` 与 `split_cjk.js` 顶部各有一个 `JOBS` 数组，两者**必须一一对应**（文件名 / 输出目录 / 字族 / 字重都对齐）：

```js
// subset_fonts.py 的 jobs（按行）：
//   (原字体完整路径,        子集后输出文件名)
jobs = [
  (f'{SRC}/glow-sc/GlowSansSC-Normal-Light.otf',   'glow-sc-45.otf'),   // font-weight 300
  (f'{SRC}/glow-sc/GlowSansSC-Normal-Regular.otf', 'glow-sc-55.otf'),   // font-weight 400
  (f'{SRC}/glow-sc/GlowSansSC-Normal-Medium.otf',  'glow-sc-65.otf'),   // font-weight 500
];

// split_cjk.js 的 JOBS（与上面的输出文件一一对应，目录/字族/字重同步）：
//   [子集文件名,  输出子目录,      CSS 字族名,   CSS font-weight]
const JOBS = [
  ['glow-sc-45.otf', 'glow-sc-45', 'GlowSC', 300],
];
```

关键字：子集文件名 = split 输出的**目录名**；两边字重必须对应同一个实际字重（45=300 / 55=400 / 65=500）；西文可变字体不在此列（走单体量静态 woff2）。

**三坑备忘**（脚本头部注释也有，这里再喊一遍）：
1. cn-font-split 不吃 woff2 输入——原字体必须 TTF/OTF；
2. `chunkSize` 不要设小值（<~100 在小子集上分包死循环）——用默认；
3. `desubroutinize=True` 必须保留——否则下游 harfbuzz 子集器卡死；后处理正则只吞 `local(...)` 别连 `src:` 一起吞。

**单点依赖提示**：整条分片链路依赖 `cn-font-split`（Node 包）。它若停维/改 API，链路会断——兜底方案：仍用本管线产出的 `subset-ttf/*.otf` 中间产物 + `fonttools` 自带的 `woff2_compress`（`pip install brotli`）逐件压成 woff2，再按字符手动写 `unicode-range` @font-face；或用 `fontmin`（其内置子集器同源）。脚本本身也接受未来替换下游 splitter。

## audit.sh —— 一致性审计

```bash
sh audit.sh /path/to/your-site
```

六项体检（PASS/FAIL）：索引卡片数 vs `INDEX ×N` 宣称、HIGHLIGHT 徽标数 vs 首页精选数、三语「查看全部 N 件」文案、同名 CSS/JS 的 `?v=` 全站一致性、HTML 体量膨胀预警（防快照污染）、sitemap 对 works/ 的覆盖。对应 `references/10-content-ops.md` 与 `04-deploy-and-domain.md` 的纪律，发布前跑一遍。

## 图片处理速查（命令行）

**macOS 示例**（`sips` + `ffmpeg`；`sips` 是 macOS 系统自带）：
```bash
# 批量转 webp（质量 82 足够作品海报用）
for f in *.jpg *.png; do sips -s format webp -s formatOptions 82 "$f" --out "${f%.*}.webp"; done

# 视频抽 poster 帧（取第 1 秒，缩到 1280 宽）
ffmpeg -ss 1 -i input.mp4 -vframes 1 -vf scale=1280:-2 -q:v 3 poster.jpg

# og:image 裁成 1200×630（先缩到覆盖再居中裁）
sips -Z 1200 source.png --out tmp.png   # 长边缩到 1200
# 精确中心裁剪用 ffmpeg 更省事：
ffmpeg -i source.png -vf "scale=1200:630:force_original_aspect_ratio=increase,crop=1200:630" -q:v 3 og-cover.jpg
```

**Linux / Windows**：没有 `sips`，用 ImageMagick 的 `magick`/`convert`（`pip install` 或发行版安装）替代，命令几乎一一对应：
```bash
# 批量转 webp（Linux/Windows + ImageMagick）
for f in *.jpg *.png; do magick "$f" -quality 82 "${f%.*}.webp"; done
# 长边缩 + 中心裁剪 og 图
magick source.png -resize "1200x1200^" -gravity center -extent 1200x630 og-cover.jpg
# 视频抽帧仍用 ffmpeg（跨平台通用），命令同上例不变
```
精简做法：嫌脚本平台差异麻烦，可统一用 **ffmpeg** 处理全部（转 webp / 抽帧 / 裁剪，跨平台一致），只是批量转 webp 丢 `sips` 的便捷循环。

webp 大图注意托管平台单文件上限（CF Pages 25 MiB——webp 一般远不到，但 4K 原图直传前查一下）。
