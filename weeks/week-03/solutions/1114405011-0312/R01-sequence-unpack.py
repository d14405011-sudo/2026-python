# R1. 序列解包（1.1）
# ------------------------------------------------------------
# 什麼是「序列解包」？
# 在 Python 中，像 tuple、list 這類「序列」可以一次拆成多個變數。
# 例如：x, y = (4, 5)
# 代表把第 1 個值給 x、第 2 個值給 y。
# ------------------------------------------------------------

print("=== 範例 1：基本 tuple 解包 ===")

# 建立一個二元素 tuple
p = (4, 5)
print("原始 tuple p =", p)

# 將 p 的兩個元素，依位置分別指定給 x、y
x, y = p
print("解包後：x =", x, ", y =", y)

print("\n=== 範例 2：list 的多欄位解包 ===")

# data 內容：公司名稱、股數、股價、日期(tuple)
data = ['ACME', 50, 91.1, (2012, 12, 21)]
print("原始 list data =", data)

# 第一次解包：先把日期整包放進 date（date 仍然是一個 tuple）
name, shares, price, date = data
print("第一次解包：")
print("name =", name)
print("shares =", shares)
print("price =", price)
print("date =", date)

# 第二次解包：進一步把日期 tuple 再拆成 year、mon、day
name, shares, price, (year, mon, day) = data
print("\n第二次解包（巢狀解包日期）：")
print("name =", name)
print("shares =", shares)
print("price =", price)
print("year =", year, ", mon =", mon, ", day =", day)

print("\n=== 範例 3：使用 _ 丟棄不需要的值 ===")

# 使用 _ 當作「我不需要這個值」的慣例占位符
# 這行表示：第 1 與第 4 欄我不使用，只保留 shares 與 price
_, shares, price, _ = data
print("只取需要欄位後：shares =", shares, ", price =", price)
