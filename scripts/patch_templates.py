import json
import os
import re
import sys

root = sys.argv[1]
dict_path = sys.argv[2]

with open(dict_path, encoding='utf-8') as f:
    table = json.load(f)

files = []
for dirpath, _dirs, names in os.walk(root):
    for n in names:
        if n.endswith(('.html', '.htm')):
            files.append(os.path.join(dirpath, n))

changed = {}
for fp in files:
    try:
        s = open(fp, encoding='utf-8').read()
    except Exception:
        continue
    orig = s
    cnt = 0
    for en, zh in table.items():
        pat = re.compile(r'(?<![A-Za-z0-9_\-])' + re.escape(en) + r'(?![A-Za-z0-9_\-])')
        s2, n = pat.subn(lambda m: zh, s)
        if n:
            s = s2
            cnt += n
    if s != orig:
        open(fp, 'w', encoding='utf-8').write(s)
        changed[os.path.relpath(fp, root)] = cnt

print(json.dumps({'files_changed': len(changed), 'replacements': sum(changed.values()), 'detail': changed}, ensure_ascii=False))
