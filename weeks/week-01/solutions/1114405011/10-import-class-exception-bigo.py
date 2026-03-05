# 10 模組、類別、例外與 Big-O（最低門檻）範例
# 這支程式示範四個核心概念：
# 1) 匯入模組（import）
# 2) 定義與使用類別（class）
# 3) 例外處理（try/except）
# 4) 時間複雜度 Big-O 的基本直覺

from collections import deque


class User:
    # __init__ 是建構子：建立物件時會自動執行
    def __init__(self, user_id):
        # 把傳入的 user_id 存到物件屬性 self.user_id
        self.user_id = user_id


def is_int(val):
    # 例外處理：檢查輸入是否能安全轉成整數
    try:
        int(val)
        return True
    except ValueError:
        return False


def demo_deque():
    # deque 是雙向佇列，設定 maxlen=2 代表最多保留 2 筆
    q = deque(maxlen=2)
    q.append(1)
    q.append(2)
    q.append(3)  # 超過長度時自動丟掉最舊的 1
    print("[deque] 目前內容:", list(q))


def demo_class():
    u = User(42)
    uid = u.user_id
    print("[class] User 的 user_id:", uid)


def demo_exception():
    samples = ["123", "3.14", "abc", "-7"]
    for value in samples:
        print(f"[try/except] {value!r} 可轉整數嗎? ->", is_int(value))


def demo_bigo_hint():
    print("[Big-O] list.append 通常是 O(1)")
    print("[Big-O] list 切片通常是 O(N)")


def main():
    print("=== 模組、類別、例外與 Big-O 範例 ===")
    demo_deque()
    demo_class()
    demo_exception()
    demo_bigo_hint()


if __name__ == "__main__":
    main()
