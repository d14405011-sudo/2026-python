# R14. 物件排序 attrgetter（1.14）

from operator import attrgetter

# 定義一個簡單類別，每個使用者有 user_id 屬性。
class User:
    def __init__(self, user_id):
        self.user_id = user_id

users = [User(23), User(3), User(99)]
print("原始 user_id 順序：", [u.user_id for u in users])
# attrgetter('user_id') 會抓物件屬性當排序鍵。
sorted_users = sorted(users, key=attrgetter('user_id'))
print("依 user_id 排序後：", [u.user_id for u in sorted_users])
