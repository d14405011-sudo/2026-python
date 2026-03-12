# R11. 命名切片 slice（1.11）

# 這是一筆固定欄位寬度的字串資料。
# 用 slice 先定義欄位位置，後續可重複使用且可讀性更好。
record = '....................100 .......513.25 ..........'
SHARES = slice(20, 23)
PRICE = slice(31, 37)

# 先切出股數與價格，再計算總成本。
cost = int(record[SHARES]) * float(record[PRICE])

print("原始資料字串：", record)
print("SHARES 切片範圍：", SHARES)
print("PRICE 切片範圍：", PRICE)
print("切出的股數：", record[SHARES])
print("切出的單價：", record[PRICE])
print("總成本 cost：", cost)
