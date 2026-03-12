# R9. 兩字典相同點：keys/items 集合運算（1.9）
# ------------------------------------------------------------
# dict 的 keys() 與 items() 可以做集合運算：
# 1. & 交集
# 2. - 差集
# 這對找「共同欄位」與「要排除欄位」很有用。
# ------------------------------------------------------------

a = {'x': 1, 'y': 2, 'z': 3}
b = {'w': 10, 'x': 11, 'y': 2}

print("a =", a)
print("b =", b)

print("\n=== keys 集合運算 ===")
common_keys = a.keys() & b.keys()
only_in_a = a.keys() - b.keys()
print("a 與 b 共同 keys =", common_keys)
print("只在 a 的 keys =", only_in_a)


print("\n=== items 集合運算（key 與 value 都要相同）===")
common_items = a.items() & b.items()
print("a 與 b 共同 items =", common_items)


print("\n=== 字典推導：排除指定 keys ===")
excluded = {'z', 'w'}
print("要排除的 keys =", excluded)

# 從 a 建立新字典 c，排除 z 與 w（其中 w 本來就不在 a）
c = {k: a[k] for k in a.keys() - excluded}
print("過濾後 c =", c)
