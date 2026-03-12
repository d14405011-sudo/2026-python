# R14. 物件排序 attrgetter（1.14）
# ------------------------------------------------------------
# attrgetter 與 itemgetter 類似，但它操作的是「物件屬性」。
# 當資料是 class instance 時，常用 attrgetter 做排序鍵。
# ------------------------------------------------------------

from operator import attrgetter


class User:
    def __init__(self, user_id):
        self.user_id = user_id

    def __repr__(self):
        # 讓 print 物件時顯示更清楚
        return f"User(user_id={self.user_id})"


users = [User(23), User(3), User(99), User(15)]
print("原始 users =", users)

users_sorted = sorted(users, key=attrgetter('user_id'))
print("依 user_id 排序後 =", users_sorted)

print("\n逐一查看排序結果：")
for idx, user in enumerate(users_sorted, start=1):
    print(f"第 {idx} 位 -> user_id = {user.user_id}")
