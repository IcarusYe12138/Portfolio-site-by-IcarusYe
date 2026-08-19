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

**三坑备忘**（脚本头部注释也有，这里再喊一遍）：
1. cn-font-split 不吃 woff2 输入——原字体必须 TTF/OTF；
2. `chunkSize` 不要设小值（<~100 在小子集上分包死循环）——用默认；
3. `desubroutinize=True` 必须保留——否则下游 harfbuzz 子集器卡死；后处理正则只吞 `local(...)` 别连 `src:` 一起吞。

## audit.sh —— 一致性审计

```bash
sh audit.sh /path/to/your-site
```

六项体检（PASS/FAIL）：索引卡片数 vs `INDEX ×N` 宣称、HIGHLIGHT 徽标数 vs 首页精选数、三语「查看全部 N 件」文案、同名 CSS/JS 的 `?v=` 全站一致性、HTML 体量膨胀预警（防快照污染）、sitemap 对 works/ 的覆盖。对应 `references/10-content-ops.md` 与 `04-deploy-and-domain.md` 的纪律，发布前跑一遍。

## 图片处理速查（macOS 命令行）

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

webp 大图注意托管平台单文件上限（CF Pages 25 MiB——webp 一般远不到，但 4K 原图直传前查一下）。
