# R1. 序列解包（1.1）

# 1) 基本解包：左邊變數數量要和右邊元素數量一致。
# p 有兩個元素，所以左邊要有兩個變數 x、y。
p = (4, 5)
x, y = p
print("元組 p：", p)
print("解包後 x、y：", x, y)

# 2) 對列表進行解包。
# data 共有 4 個元素：公司名、股數、價格、日期元組。
# 因此左邊也放 4 個變數接收。
data = ['ACME', 50, 91.1, (2012, 12, 21)]
name, shares, price, date = data
print("\n原始 data：", data)
print("一般解包 name、shares、price、date：", name, shares, price, date)

# 3) 巢狀解包：當某個元素本身也是序列時，可以再往下拆。
# 這裡把 date=(2012, 12, 21) 直接拆成年、月、日。
name, shares, price, (year, mon, day) = data
print("巢狀解包 year、mon、day：", year, mon, day)

# 丟棄不需要的值（占位）
# 4) 使用 _ 當作「我不需要這個值」的占位符。
# 慣例上 _ 代表這個變數不會被後續程式使用。
# 這行表示：只保留 shares 與 price，忽略第 1 和第 4 個元素。
_, shares, price, _ = data
print("使用 _ 丟棄後，保留 shares、price：", shares, price)
