# R6. 多值字典 defaultdict / setdefault（1.6）
# ------------------------------------------------------------
# 多值字典意思：同一個 key 底下要放多個值。
# 1. defaultdict(list): 每個 key 自動有空 list。
# 2. defaultdict(set): 每個 key 自動有空 set（可去重）。
# 3. setdefault: 一般 dict 也能做到，但語法較冗長。
# ------------------------------------------------------------

from collections import defaultdict

print("=== 範例 1：defaultdict(list) ===")
d = defaultdict(list)
print("初始 d =", dict(d))

d['a'].append(1)
print("加入 d['a'].append(1) 後 =", dict(d))

d['a'].append(2)
print("加入 d['a'].append(2) 後 =", dict(d))

d['b'].append(10)
print("加入 d['b'].append(10) 後 =", dict(d))


print("\n=== 範例 2：defaultdict(set)（自動去重）===")
d = defaultdict(set)
print("初始 d =", {k: sorted(v) for k, v in d.items()})

d['a'].add(1)
print("加入 d['a'].add(1) 後 =", {k: sorted(v) for k, v in d.items()})

d['a'].add(2)
print("加入 d['a'].add(2) 後 =", {k: sorted(v) for k, v in d.items()})

d['a'].add(2)
print("再次加入重複值 d['a'].add(2) 後 =", {k: sorted(v) for k, v in d.items()})


print("\n=== 範例 3：一般 dict 搭配 setdefault ===")
d = {}
print("初始 d =", d)

d.setdefault('a', []).append(1)
print("setdefault 後 d =", d)

d.setdefault('a', []).append(2)
print("再次 setdefault 後 d =", d)
