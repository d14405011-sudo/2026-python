# R2. 解包數量不固定：星號解包（1.2）

# 1) 使用 *middle 接住中間「不固定數量」的元素。
# first 接第一個，last 接最後一個，剩下都放進 middle（型別是 list）。
def drop_first_last(grades):
    first, *middle, last = grades
    # 這裡示範常見情境：去頭去尾後，計算中間成績平均。
    return sum(middle) / len(middle)


# 範例資料：會丟掉 98 與 100，只算中間三筆。
scores = [98, 92, 87, 95, 100]
print("原始分數：", scores)
print("去掉第一個與最後一個後的平均：", drop_first_last(scores))

# 2) 星號解包也常用在「剩餘欄位收集」。
# 前兩個欄位固定是 name、email，其餘電話都收進 phone_numbers。
record = ('Dave', 'dave@example.com', '773-555-1212', '847-555-1212')
name, email, *phone_numbers = record
print("\n姓名：", name)
print("Email：", email)
print("電話清單（星號解包）：", phone_numbers)

# 3) 星號可以放左側，表示「最後一個以外」都收集起來。
*trailing, current = [10, 8, 7, 1, 9, 5, 10, 3]
print("\ntrailing：", trailing)
print("current：", current)
