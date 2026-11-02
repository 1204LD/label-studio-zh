"""汉化覆盖率自检。

用法：
    python scripts/verify.py <dist 目录>

输出：
    - chunk 数量与总体积
    - 中文字符数（越多说明替换越充分）
    - 仍为英文的“显示位”字符串数量（children / title / label / placeholder ...）
"""
import json
import os
import re
import sys

DISPLAY_KEYS = (
    'children', 'title', 'label', 'placeholder', 'tooltip', 'description', 'alt',
    'header', 'hint', 'message', 'text', 'summary', 'emptyState', 'confirmText',
    'cancelText', 'okText', 'subTitle', 'buttonText',
)

def main(root):
    if not os.path.isdir(root):
        print('dist 目录不存在: %s' % root)
        return 2

    files = []
    for dirpath, _dirs, names in os.walk(root):
        for n in names:
            if n.endswith('.js') and not n.endswith('.map'):
                files.append(os.path.join(dirpath, n))

    cjk_re = re.compile(r'[\u4e00-\u9fff]')
    str_re = re.compile(r'"((?:[^"\\\n]|\\.)*)"')
    display_re = re.compile(
        r'(?:' + '|'.join(re.escape(k) for k in DISPLAY_KEYS) + r')\s*:\s*$'
    )

    total_cjk = 0
    residual = {}
    for fp in sorted(files):
        with open(fp, encoding='utf-8', errors='replace') as f:
            src = f.read()
        total_cjk += len(cjk_re.findall(src))
        for m in str_re.finditer(src):
            val = m.group(1)
            if len(val) < 2 or len(val) > 120:
                continue
            if not re.search(r'[A-Za-z]{2}', val):
                continue
            if cjk_re.search(val):
                continue
            if re.search(r'[{}<>$`\\]', val):
                continue
            before = src[max(0, m.index - 30):m.index]
            if not display_re.search(before):
                continue
            residual[val] = residual.get(val, 0) + 1

    print('chunks: %d' % len(files))
    print('CJK characters in bundles: %d' % total_cjk)
    print('residual english display strings: %d' % len(residual))
    top = sorted(residual.items(), key=lambda kv: -kv[1])[:15]
    if top:
        print('top residual:')
        for v, c in top:
            print('  %4d  %s' % (c, v))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else '/label-studio/web/dist'))
