# R1. 序列解包（1.1）

p = (4, 5)
x, y = p
print("元組 p：", p)
print("解包後 x、y：", x, y)

data = ['ACME', 50, 91.1, (2012, 12, 21)]
name, shares, price, date = data
print("\n原始 data：", data)
print("一般解包 name、shares、price、date：", name, shares, price, date)
name, shares, price, (year, mon, day) = data
print("巢狀解包 year、mon、day：", year, mon, day)

# 丟棄不需要的值（占位）
_, shares, price, _ = data
print("使用 _ 丟棄後，保留 shares、price：", shares, price)
