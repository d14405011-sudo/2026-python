# R7. OrderedDict（1.7）
# ------------------------------------------------------------
# OrderedDict 會記住插入順序。
# 在需要「輸出順序可預期」的場景（像報表、JSON 展示）很有用。
# ------------------------------------------------------------

from collections import OrderedDict
import json

print("=== OrderedDict 示範 ===")
d = OrderedDict()
print("初始 d =", d)

d['foo'] = 1
print("加入 foo 後 d =", d)

d['bar'] = 2
print("加入 bar 後 d =", d)

d['spam'] = 3
print("加入 spam 後 d =", d)

json_text = json.dumps(d, ensure_ascii=False)
print("\n轉成 JSON 字串 =", json_text)
print("keys() 順序 =", list(d.keys()))
