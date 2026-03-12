# R11. 命名切片 slice（1.11）
# ------------------------------------------------------------
# 用 slice 物件命名欄位位置，能讓程式可讀性更高。
# 比起直接寫 record[20:23]，寫成 record[SHARES] 更清楚。
# ------------------------------------------------------------

record = '....................100.......513.25..........'
print("原始 record =", record)
print("record 長度 =", len(record))

# 命名切片：股數在 [20:23)，價格在 [30:36)
SHARES = slice(20, 23)
PRICE = slice(30, 36)

print("\n=== 切片資訊 ===")
print("SHARES =", SHARES)
print("PRICE =", PRICE)
print("SHARES.start/stop/step =", SHARES.start, SHARES.stop, SHARES.step)
print("PRICE.start/stop/step =", PRICE.start, PRICE.stop, PRICE.step)

shares_text = record[SHARES]
price_text = record[PRICE]
print("\n擷取 shares_text =", shares_text)
print("擷取 price_text =", price_text)

shares = int(shares_text)
price = float(price_text)
cost = shares * price

print("轉型後 shares =", shares)
print("轉型後 price =", price)
print("總成本 cost = shares * price =", cost)
