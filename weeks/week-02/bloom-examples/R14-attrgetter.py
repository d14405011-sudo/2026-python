# R14. 物件排序 attrgetter（1.14）

from operator import attrgetter

class User:
    def __init__(self, user_id):
        self.user_id = user_id

users = [User(23), User(3), User(99)]
print("原始 user_id 順序：", [u.user_id for u in users])
sorted_users = sorted(users, key=attrgetter('user_id'))
print("依 user_id 排序後：", [u.user_id for u in sorted_users])
