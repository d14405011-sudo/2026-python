# R11. 命名切片 slice（1.11）

record = '....................100 .......513.25 ..........'
SHARES = slice(20, 23)
PRICE = slice(31, 37)
cost = int(record[SHARES]) * float(record[PRICE])

print("原始資料字串：", record)
print("SHARES 切片範圍：", SHARES)
print("PRICE 切片範圍：", PRICE)
print("切出的股數：", record[SHARES])
print("切出的單價：", record[PRICE])
print("總成本 cost：", cost)
