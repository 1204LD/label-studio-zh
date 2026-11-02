import json
import os
import sys

dist = sys.argv[1]
dict_path = sys.argv[2]

with open(dict_path, encoding='utf-8') as f:
    table = json.load(f)

files = []
for root, _dirs, names in os.walk(dist):
    for fn in names:
        if fn.endswith('.js'):
            files.append(os.path.join(root, fn))

report = {}
total = 0
for fp in files:
    data = open(fp, 'rb').read()
    orig = data
    cnt = 0
    for en, zh in table.items():
        eb = en.encode('utf-8')
        zb = zh.encode('utf-8')
        for q in (b'"', b"'"):
            pat = q + eb + q
            if pat in data:
                c = data.count(pat)
                data = data.replace(pat, q + zb + q)
                cnt += c
    if data != orig:
        with open(fp, 'wb') as f:
            f.write(data)
        report[os.path.basename(fp)] = cnt
        total += cnt

print(json.dumps({'total': total, 'files': report}, ensure_ascii=False))
