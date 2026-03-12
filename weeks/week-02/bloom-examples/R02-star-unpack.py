# R2. 解包數量不固定：星號解包（1.2）

def drop_first_last(grades):
    first, *middle, last = grades
    return sum(middle) / len(middle)


scores = [98, 92, 87, 95, 100]
print("原始分數：", scores)
print("去掉第一個與最後一個後的平均：", drop_first_last(scores))

record = ('Dave', 'dave@example.com', '773-555-1212', '847-555-1212')
name, email, *phone_numbers = record
print("\n姓名：", name)
print("Email：", email)
print("電話清單（星號解包）：", phone_numbers)

*trailing, current = [10, 8, 7, 1, 9, 5, 10, 3]
print("\ntrailing：", trailing)
print("current：", current)
