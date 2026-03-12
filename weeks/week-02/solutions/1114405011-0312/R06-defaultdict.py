# R6. 多值字典 defaultdict / setdefault（1.6）

from collections import defaultdict

# 1) defaultdict(list)：當 key 不存在時，自動建立空 list。
d = defaultdict(list)
d['a'].append(1); d['a'].append(2)
print("defaultdict(list) 結果：", dict(d))

# 2) defaultdict(set)：不存在時自動建立空 set。
# set 會自動去重，適合收集「不重複值」。
d = defaultdict(set)
d['a'].add(1); d['a'].add(2)
print("defaultdict(set) 結果：", {key: sorted(value) for key, value in d.items()})

# 3) 一般 dict 可用 setdefault 達到類似效果。
# 若 key 不存在，就先放入預設值（這裡是空 list），再 append。
d = {}
d.setdefault('a', []).append(1)
print("setdefault 結果：", d)
