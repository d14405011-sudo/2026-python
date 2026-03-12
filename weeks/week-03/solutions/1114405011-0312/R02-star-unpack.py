# R2. 解包數量不固定：星號解包（1.2）
# ------------------------------------------------------------
# 星號解包（*）的重點：
# 1. 讓你接收「不固定數量」的元素。
# 2. 被 * 接到的部分，一定是 list。
# 3. 常見用法：忽略頭尾，只處理中間資料。
# ------------------------------------------------------------


def drop_first_last(grades):
    """忽略第一筆與最後一筆分數，只計算中間分數平均。"""
    print("\n[drop_first_last] 原始分數：", grades)

    # first 與 last 各接一個元素，middle 接中間所有元素
    first, *middle, last = grades
    print("[drop_first_last] first =", first)
    print("[drop_first_last] middle =", middle)
    print("[drop_first_last] last =", last)

    avg = sum(middle) / len(middle)
    print("[drop_first_last] 中間平均 =", avg)
    return avg


print("=== 範例 1：忽略頭尾，取中間 ===")
scores = [98, 92, 85, 88, 91, 95]
result = drop_first_last(scores)
print("回傳平均 =", result)


print("\n=== 範例 2：聯絡資料中的不固定電話數 ===")
record = ('Dave', 'dave@example.com', '773-555-1212', '847-555-1212')
print("原始 record =", record)

# 前兩欄固定拆給 name/email，其餘全交給 phone_numbers
name, email, *phone_numbers = record
print("name =", name)
print("email =", email)
print("phone_numbers =", phone_numbers)


print("\n=== 範例 3：取最後一筆 current，其餘放 trailing ===")
numbers = [10, 8, 7, 1, 9, 5, 10, 3]
print("原始 numbers =", numbers)

*trailing, current = numbers
print("trailing =", trailing)
print("current =", current)
