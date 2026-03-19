# U2. 星號解包為何能處理「不定長」且結果固定是 list（1.2）
#
# 星號解包（*variable）的特性：
# - 可以在解包時吸收多個或零個元素
# - 星號變數的結果「永遠是 list」，即使只有一個或沒有元素
# - 這解決了普通解包必須精確匹配元素數量的限制

# 建立一個包含 2 個元素的 tuple：姓名與信箱
record = ('Dave', 'dave@example.com')

# 使用星號解包：*phones 會吸收所有「剩余」的元素
# - name 取得 'Dave'
# - email 取得 'dave@example.com'
# - *phones 吸收剩餘的元素（此處沒有剩餘），結果是空 list []
name, email, *phones = record

# 注意：即使沒有匹配到任何元素，phones 仍是 list 型態（不是 None 或其他）
# phones == []  仍是 list

# 輸出結果
print(name, email, phones)