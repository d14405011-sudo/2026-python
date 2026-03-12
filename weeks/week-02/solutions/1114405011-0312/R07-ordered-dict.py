# R7. OrderedDict（1.7）

from collections import OrderedDict
import json

# OrderedDict 會保留鍵的插入順序。
# （Python 3.7+ 的一般 dict 也保序，但此範例示範明確語意。）
d = OrderedDict()
d['foo'] = 1; d['bar'] = 2
print("建立 OrderedDict 後的內容：", d)
# keys()/values() 會依插入順序輸出。
print("鍵的插入順序：", list(d.keys()))
print("值的順序：", list(d.values()))
# 轉成 JSON 時，欄位順序也會依目前字典順序輸出。
print("轉成 JSON 字串後：", json.dumps(d, ensure_ascii=False))
