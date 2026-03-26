# R07. 日期時間基本運算：時差計算與星期計算（Cookbook 第 3.12–3.13 節）
# 內容涵蓋：timedelta（時間差物件）的加減運算 / weekday() 計算特定星期的日期

from datetime import datetime, timedelta

# ── 第 3.12 節：timedelta（時間差物件）的基本運算 ────────
# timedelta 代表一個時間段（持續時間），支援加減運算
a = timedelta(days=2, hours=6)  # 2 天 6 小時
b = timedelta(hours=4.5)         # 4.5 小時
c = a + b                        # 時間差相加
print(c.days)  # 2（總天數部分）
print(c.total_seconds() / 3600)  # 58.5（轉換為總小時數）

# datetime 與 timedelta 的運算（日期 + 時間差 = 新日期）
dt = datetime(2012, 9, 23)      # 建立一個日期時間物件
print(dt + timedelta(days=10))  # 2012-10-03 00:00:00（向後推 10 天）

# 計算兩個日期時間之間的時間差
d1, d2 = datetime(2012, 9, 23), datetime(2012, 12, 21)
print((d2 - d1).days)  # 89（相差 89 天）

# Python 的日期計算會自動處理閏年（閏年有 2 月 29 日）
print((datetime(2012, 3, 1) - datetime(2012, 2, 28)).days)  # 2（2012 年是閏年）
print((datetime(2013, 3, 1) - datetime(2013, 2, 28)).days)  # 1（2013 年是平年）

# ── 第 3.13 節：計算最近的指定星期日期 ──────────────────
# 使用 weekday() 計算日期，然後找出最近的特定星期幾

WEEKDAYS = [
    "Monday",     # 0
    "Tuesday",    # 1
    "Wednesday",  # 2
    "Thursday",   # 3
    "Friday",     # 4
    "Saturday",   # 5
    "Sunday",     # 6
]


def get_previous_byday(dayname: str, start: datetime | None = None) -> datetime:
    """找出早於起始日期的最近指定星期幾的日期"""
    if start is None:
        start = datetime.today()  # 預設為今天
    
    day_num = start.weekday()  # 取得起始日期是星期幾（0=Monday，6=Sunday）
    target = WEEKDAYS.index(dayname)  # 取得目標星期幾的索引
    # 計算需要往回退多少天：
    # (7 + 當前星期 - 目標星期) % 7 給出向前要進幾天（環形）
    # or 7 確保如果結果是 0（今天就是目標星期），則返回 7（上一週的同一天）
    days_ago = (7 + day_num - target) % 7 or 7
    return start - timedelta(days=days_ago)


base = datetime(2012, 8, 28)  # 2012 年 8 月 28 日是週二
print(get_previous_byday("Monday", base))  # 2012-08-27（前一個週一）
print(get_previous_byday("Friday", base))  # 2012-08-24（前一個週五，往回 3 天）
