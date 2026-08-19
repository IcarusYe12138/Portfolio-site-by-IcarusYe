# -*- coding: utf-8 -*-
"""收集站点全部 HTML 中实际使用的 CJK 字符，产出字符集清单。

用法（在任意位置运行均可）：
    python3 collect_chars.py <站点根目录>            # 默认当前目录
    python3 collect_chars.py /path/to/site -o my-cjk-set.txt

行为：
    - 递归扫描 <站点根目录> 下全部 *.html
    - 排除 node_modules / .git / archive 等目录（可用 --include-archive 关闭排除）
    - 提取 CJK 统一表意文字（U+4E00–U+9FFF）与常用中文标点
    - 输出到 -o 指定文件（默认写入脚本同目录 cjk-set.txt），供 subset_fonts.py 使用

改完站点文案后重跑本脚本 → 再跑 subset_fonts.py → split_cjk.js。
新文案含未收录字时该字会静默回退系统字体（不报错），所以内容更新后必须重跑。
"""
import argparse
import glob
import os

# 常用中文标点（按需增删——只加你真正会用的，字符集越小字体越小）
PUNCT = set('，。、；：？！「」『』（）【】《》〈〉·—…')

EXCLUDE_DIRS = {'node_modules', '.git', 'font-src'}


def main():
    ap = argparse.ArgumentParser(description='Collect CJK chars used by site HTML files')
    ap.add_argument('site', nargs='?', default='.', help='site root (default: cwd)')
    ap.add_argument('-o', '--out', default=None, help='output charset file (default: cjk-set.txt beside this script)')
    args = ap.parse_args()

    here = os.path.dirname(os.path.abspath(__file__))
    site = os.path.abspath(args.site)
    dst = args.out or os.path.join(here, 'cjk-set.txt')

    chars = set()
    files = []
    for root, dirs, names in os.walk(site):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for n in names:
            if n.endswith('.html'):
                files.append(os.path.join(root, n))

    for f in files:
        with open(f, encoding='utf-8') as fh:
            t = fh.read()
        for ch in t:
            if '一' <= ch <= '鿿' or ch in PUNCT:
                chars.add(ch)

    with open(dst, 'w', encoding='utf-8') as fh:
        fh.write(''.join(sorted(chars)))
    print('unique CJK chars:', len(chars))
    print('files scanned   :', len(files))
    print('written         :', dst)


if __name__ == '__main__':
    main()
