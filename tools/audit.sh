#!/bin/sh
# ============================================================
# audit.sh —— 站点一致性审计（内容运维 + 部署纪律的快速体检）
# 对应 references/10-content-ops.md 的 grep 审计与 04 的缓存纪律。
# 用法：sh audit.sh <站点根目录>     （默认当前目录）
# 全部输出 PASS/FAIL，FAIL 需人工核对；非强制阻塞，是体检不是门禁。
# ============================================================
SITE="${1:-.}"
cd "$SITE" || exit 1

pass=0; fail=0
ok()   { printf '  \033[32mPASS\033[0m %s\n' "$1"; pass=$((pass+1)); }
bad()  { printf '  \033[31mFAIL\033[0m %s\n' "$1"; fail=$((fail+1)); }
head() { printf '\n== %s ==\n' "$1"; }

# ---- 1. 索引页：卡片实际数 vs 头部宣称数 ----
# 说明：works-index.html 的 INDEX ×N 由 JS 从 DOM 卡片实时填充（静态 HTML 里没有
#      这个字面量）。因此这里只断言「卡片数 > 0」（防止整块没渲染/清空）；
#      若静态 HTML 里硬编码了 INDEX ×N / 索引 ×N（旧式写法），则额外核对二者相等。
head "Works index: card count vs claimed"
if [ -f works.html ]; then
  cards=$(grep -c 'class="cell' works.html)
  [ "$cards" -gt 0 ] && ok "cards ($cards) > 0"
                    || bad "cards = 0 — works.html 没有可识别的 .cell 卡片?"
  claim=$(grep -o 'INDEX ×[0-9]*' works.html | head -1 | grep -o '[0-9]*')
  [ -z "$claim" ] && claim=$(grep -o '索引 ×[0-9]*' works.html | head -1 | grep -o '[0-9]*')
  if [ -n "$claim" ]; then
    [ "$cards" = "$claim" ] && ok "静态宣称 ×$claim == cards ($cards)" \
                            || bad "静态宣称 ×$claim != cards ($cards) — 删掉硬编码，改用 JS 填充"
  else
    ok "宣称计数由 JS 填充（INDEX ×N 非静态字面量），无需核对"
  fi
else
  printf '  (works.html 不存在，跳过)\n'
fi

# ---- 2. 索引页：HIGHLIGHT 徽标数 vs 首页精选卡数 ----
head "Highlight badges vs homepage rail"
if [ -f works.html ] && [ -f index.html ]; then
  badges=$(grep -c 'cell-hl' works.html)
  rail=$(grep -c 'hl-card' index.html)
  [ "$badges" = "$rail" ] && ok "badges ($badges) == rail cards ($rail)" \
                      || bad "badges ($badges) != rail cards ($rail)"
fi

# ---- 3. 首页「查看全部 N 件」文案 vs 实际卡数 ----
head "Homepage view-all copy vs actual count"
if [ -f index.html ] && [ -f works.html ]; then
  cards=$(grep -c 'class="cell' works.html)
  for re in 'View All [0-9]*' '查看全部 [0-9]* 件' '查看全部 [0-9]* 個'; do
    n=$(grep -o "$re" index.html | head -1 | grep -o '[0-9]*')
    [ -z "$n" ] && continue
    [ "$n" = "$cards" ] && ok "「$re」= $n == $cards" \
                       || bad "「$re」= $n != $cards（三语字典逐份核对）"
  done
fi

# ---- 4. CSS/JS 版本号一致性（同名资源不同页 ?v= 不一致 = 高危） ----
head "Asset ?v= consistency"
for f in $(find . -name '*.html' -not -path './node_modules/*' | xargs grep -oh 'assets/[a-z]*/[a-z.-]*\.\(css\|js\)?v=[0-9a-z]*' 2>/dev/null | sed 's/?v=.*//' | sort -u); do
  vs=$(find . -name '*.html' -not -path './node_modules/*' | xargs grep -oh "$f?v=[0-9a-z]*" 2>/dev/null | sed "s|.*?v=||" | sort -u | tr '\n' ' ')
  cnt=$(echo $vs | wc -w | tr -d ' ')
  [ "$cnt" = "1" ] && ok "$f → v=$vs" \
               || bad "$f → 多版本: $vs（改过内容未全站 bump？）"
done

# ---- 5. HTML 体量抽查（防快照污染膨胀） ----
head "HTML size sanity (>300KB 需警惕快照污染)"
find . -name '*.html' -not -path './node_modules/*' -not -path './archive/*' | while read -r h; do
  sz=$(wc -c < "$h" | tr -d ' ')
  if [ "$sz" -gt 300000 ]; then printf '  \033[31mFAIL\033[0m %s = %sKB\n' "$h" "$((sz/1024))"
  elif [ "$sz" -gt 150000 ]; then printf '  \033[33mWARN\033[0m %s = %sKB\n' "$h" "$((sz/1024))"; fi
done
ok "size scan done"

# ---- 6. sitemap 覆盖 works/ 详情页 ----
head "Sitemap coverage"
if [ -f sitemap.xml ]; then
  for p in works/*.html; do
    [ -e "$p" ] || continue
    grep -q "$p" sitemap.xml && ok "sitemap ∙ $p" || bad "sitemap 缺 $p"
  done
fi

printf '\n────────\n结果: %d pass / %d fail\n' "$pass" "$fail"
[ "$fail" = "0" ] || exit 1
