import json
import os
import re
import sys

dist = sys.argv[1]
dict_path = sys.argv[2]

with open(dict_path, encoding='utf-8') as f:
    table = json.load(f)

PROPS = ('children', 'title', 'label', 'placeholder', 'tooltip', 'description', 'alt', 'header',
         'hint', 'message', 'text', 'summary', 'emptyState', 'confirmText', 'cancelText', 'okText',
         'subTitle', 'buttonText', '"aria-label"', 'aria-label')

files = []
for root, _dirs, names in os.walk(dist):
    for fn in names:
        if fn.endswith('.js'):
            files.append(os.path.join(root, fn))

report = {}
total = 0
for fp in files:
    s = open(fp, encoding='utf-8').read()
    orig = s
    cnt = 0
    for en, zh in table.items():
        for prop in PROPS:
            for q in ('"', "'"):
                pat = re.escape(prop) + r'\s*:\s*' + re.escape(q + en + q)
                new = prop + ':' + q + zh + q
                s, n = re.subn(pat, new, s)
                cnt += n
    if s != orig:
        open(fp, 'w', encoding='utf-8').write(s)
        report[os.path.basename(fp)] = cnt
        total += cnt

print(json.dumps({'total': total, 'files': report}, ensure_ascii=False))
