# R6. 多值字典 defaultdict / setdefault（1.6）

from collections import defaultdict

d = defaultdict(list)
d['a'].append(1); d['a'].append(2)
print("defaultdict(list) 結果：", dict(d))

d = defaultdict(set)
d['a'].add(1); d['a'].add(2)
print("defaultdict(set) 結果：", {key: sorted(value) for key, value in d.items()})

d = {}
d.setdefault('a', []).append(1)
print("setdefault 結果：", d)
