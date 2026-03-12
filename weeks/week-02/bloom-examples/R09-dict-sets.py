# R9. 兩字典相同點：keys/items 集合運算（1.9）

a = {'x': 1, 'y': 2, 'z': 3}
b = {'w': 10, 'x': 11, 'y': 2}

print("字典 a：", a)
print("字典 b：", b)
print("共同的鍵：", a.keys() & b.keys())
print("a 有但 b 沒有的鍵：", a.keys() - b.keys())
print("共同的鍵值對：", a.items() & b.items())

c = {k: a[k] for k in a.keys() - {'z', 'w'}}
print("移除 z、w 後的新字典 c：", c)
