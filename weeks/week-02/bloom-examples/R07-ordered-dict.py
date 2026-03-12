# R7. OrderedDict（1.7）

from collections import OrderedDict
import json

d = OrderedDict()
d['foo'] = 1; d['bar'] = 2
print("建立 OrderedDict 後的內容：", d)
print("鍵的插入順序：", list(d.keys()))
print("值的順序：", list(d.values()))
print("轉成 JSON 字串後：", json.dumps(d, ensure_ascii=False))
