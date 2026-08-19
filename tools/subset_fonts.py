# -*- coding: utf-8 -*-
"""按站点实际字符集（cjk-set.txt）子集化中文原字体，产出中间 OTF。

管线第 2 步：collect_chars.py → 【本脚本】 → split_cjk.js

用法：
    python3 subset_fonts.py                 # 使用下方 JOBS 配置
    python3 subset_fonts.py -c my-cjk-set.txt -s /path/to/font-src -o subset-ttf

依赖：pip install fonttools
输入：中文原字体（TTF/OTF —— cn-font-split 不吃 woff2 输入，必须 TTF/OTF）
输出：./subset-ttf/*.otf（中间产物，gitignore；随后交给 split_cjk.js 分片）

⚠ 三个已知的坑（都来自真实翻车，勿删注释）：
    1. 输入必须是 TTF/OTF —— woff2 输入会让下游分片器静默无产物；
    2. desubroutinize=True 必须保留 —— fonttools 重新子程序化的 CFF charstring
       会让 cn-font-split 的 harfbuzz 子集器卡死；
    3. 原字体放部署目录之外（font-src/），保持部署产物干净。
"""
import argparse
import os

from fontTools.subset import Options, Subsetter
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))

# ===== JOBS：改成你自己的字体 =====
# 每项 = (源字体路径, 输出文件名)
# 输出文件名与 split_cjk.js 的 JOBS 对应；建议命名 <family>-<weight>.otf
# 例：简体 3 字重 + 繁体 3 字重（数量随意，按需增删）
JOBS = [
    (os.path.join(HERE, 'font-src', 'sc-Light.otf'),   'sc-45.otf'),
    (os.path.join(HERE, 'font-src', 'sc-Regular.otf'), 'sc-55.otf'),
    (os.path.join(HERE, 'font-src', 'tc-Light.otf'),   'tc-45.otf'),
    (os.path.join(HERE, 'font-src', 'tc-Regular.otf'), 'tc-55.otf'),
]


def main():
    ap = argparse.ArgumentParser(description='Subset CJK fonts to the site charset')
    ap.add_argument('-c', '--charset', default=os.path.join(HERE, 'cjk-set.txt'))
    ap.add_argument('-s', '--src', default=None, help='font source dir (overrides JOBS paths prefix)')
    ap.add_argument('-o', '--out', default=os.path.join(HERE, 'subset-ttf'))
    args = ap.parse_args()

    chars = open(args.charset, encoding='utf-8').read()
    # 补 ASCII + 常用西文标点，避免中文标签里夹英文时回退
    extra = ''.join(chr(c) for c in range(0x20, 0x7F)) + '“”‘’–—…·'
    text = chars + extra

    os.makedirs(args.out, exist_ok=True)
    jobs = JOBS
    if args.src:
        jobs = [(os.path.join(args.src, os.path.basename(src)), name) for src, name in JOBS]

    for src, name in jobs:
        opt = Options()
        opt.layout_features = '*'
        opt.name_IDs = ['*']
        opt.hinting = False
        # flatten CFF subroutines —— 不加这行下游 harfbuzz 子集器会挂死（见头部注释）
        opt.desubroutinize = True
        ss = Subsetter(options=opt)
        font = TTFont(src)
        ss.populate(text=text)
        ss.subset(font)
        dst = os.path.join(args.out, name)
        font.save(dst)
        print(name, os.path.getsize(dst) // 1024, 'KB')
    print('output dir:', os.path.abspath(args.out))


if __name__ == '__main__':
    main()
